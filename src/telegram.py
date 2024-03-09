from telebot import TeleBot, types
import threading
import itertools
import time
import os

from .utils import get_command_template, get_temp_dir, count_tokens
from .models import CodebaseModel
from .builder import CodebaseBuilder
from .config import WHITELIST, LIMIT


def limit_user(func):
    @wraps(func)
    def wrapper(self, message):
        user_id = message.from_user.id
        if user_id not in self.user_counts:
            self.user_counts[user_id] = {'ask_count': 0, 'generate_count': 0}
        if user_id not in WHITELIST:
            if func.__name__ == 'on_ask' and self.user_counts[user_id]['ask_count'] >= LIMIT:
                self.reply_to(message, f"Sorry, you have exceeded your limit ({LIMIT}) for the `/ask` command. Contact support for more access using `/contact`.", parse_mode='Markdown')
                return
            elif func.__name__ == 'on_generate' and self.user_counts[user_id]['generate_count'] >= LIMIT:
                self.reply_to(message, f"Sorry, you have exceeded your limit ({LIMIT}) for the `/generate` command. Contact support for more access using `/contact`.", parse_mode='Markdown')
                return
        return func(self, message)
    return wrapper


class CodebaseArchitectBot(TeleBot):
    def __init__(self, bot_token: str, model: CodebaseModel):
        super().__init__(token=bot_token)

        self.user_counts = {}  # {user_id: {'last_call': 12345678, 'to_lang': 'yy'}}
        self.model = model

        @self.message_handler(commands=['start'])
        def on_start(message):
            self.send_message(message.chat.id, get_command_template('help').format(bot_name=self.get_me().first_name), parse_mode='Markdown')

        @self.message_handler(commands=['help'])
        def on_help(message):
            self.reply_to(message, get_command_template('help').format(bot_name=self.get_me().first_name), parse_mode='Markdown')
            
        @self.message_handler(commands=['contact'])
        def on_contact(message):
            self.reply_to(message, get_command_template('contact').format(bot_name=self.get_me().first_name), parse_mode='Markdown')
            
        @self.message_handler(commands=['ask'])
        def on_ask(message):
            user_id = message.from_user.id
            if user_id not in self.user_counts:
                self.user_counts[user_id] = {'ask_count': 0, 'generate_count': 0}
            if user_id not in WHITELIST and self.user_counts[user_id]['ask_count'] >= LIMIT:
                self.reply_to(message, f"Sorry, you have exceeded your limit ({LIMIT}) for the `/ask` command. Contact support for more access using `/contact`.", parse_mode='Markdown')
                return
            
            try:
                context = message.text.split(' ', 1)[1]
            except IndexError:
                self.reply_to(message, "Please provide the context what you want to ask by sending `/ask <context>`", parse_mode='Markdown')
                return
            
            self.user_counts[user_id]['ask_count'] += 1
            
            sent_msg = self.reply_to(message, "_🧠 Thinking, please wait ..._", parse_mode="Markdown")
            
            response = self.model.generic_call(context)
            
            self.edit_message_text(response, chat_id=sent_msg.chat.id, message_id=sent_msg.message_id, parse_mode='Markdown')
            
            
        @self.message_handler(commands=['generate'])
        def on_generate(message):
            user_id = message.from_user.id
            if user_id not in self.user_counts:
                self.user_counts[user_id] = {'ask_count': 0, 'generate_count': 0}
            if user_id not in WHITELIST and self.user_counts[user_id]['generate_count'] >= LIMIT:
                self.reply_to(message, f"Sorry, you have exceeded your limit ({LIMIT}) for the `/generate` command. Contact support for more access using `/contact`.", parse_mode='Markdown')
                return
            
            try:
                context = message.text.split(' ', 1)[1]
            except IndexError:
                self.reply_to(message, "Please provide the context of the codebase you want to generate by sending `/generate <context>`", parse_mode='Markdown')
                return
            
            if len(context.strip()) > 0:
                # Increment user count
                self.user_counts[user_id]['generate_count'] += 1
                
                token_count = '{:,}'.format(count_tokens(context, "gpt-4"))
                progress_message = self.reply_to(message, f"Generating codebase with your provided context (Est. {token_count} tokens).\n\n_🚀 Operation started ..._", parse_mode='Markdown')
                
                def animate_progress():
                    animation = itertools.cycle(["🔄", "🔁", "🔃"])
                    loading = itertools.cycle([".", "..", "..."])
                    while self.is_generating:
                        self.edit_message_text(f"Generating codebase with your provided context (Est. {token_count} tokens).\n\n_{next(animation)} Building codebase {next(loading)}_", chat_id=progress_message.chat.id, message_id=progress_message.message_id, parse_mode='Markdown')
                        time.sleep(0.75)  # Adjust the animation speed as needed
                
                self.is_generating = True
                threading.Thread(target=animate_progress).start()
                
                response = self.model.generate_codebase(context)
                
                self.is_generating = False
                
                tmp = get_temp_dir()
                
                builder = CodebaseBuilder(project_folder=os.path.join(tmp, response['project']))
                builder.build_codebase(response)
                
                # Zip the project folder
                zip_path = os.path.join(tmp, f"{response['project']}.zip")
                builder.zip_project(zip_path)
                
                # Send the zip file to Telegram
                with open(zip_path, 'rb') as zip_file:
                    self.send_document(message.chat.id, zip_file)
                
                # Clean up the build and zip file
                builder.clean_up()
                os.remove(zip_path)
                
                # Send confirmation message
                self.edit_message_text(f"Generating codebase with your provided context (Est. {token_count} tokens).\n\n*✅ Done!*", chat_id=progress_message.chat.id, message_id=progress_message.message_id, parse_mode='Markdown')