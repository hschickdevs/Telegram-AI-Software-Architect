from telebot import TeleBot, types

from .utils import get_command_template, get_temp_dir, count_tokens
from .models import CodebaseModelOpenAI
from .builder import CodebaseBuilder

import os


class CodebaseArchitectBot(TeleBot):
    def __init__(self, bot_token: str, model: CodebaseModelOpenAI):
        super().__init__(token=bot_token)

        self.user_sessions = {}  # {user_id: {'last_call': 12345678, 'to_lang': 'yy'}}
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
            
        @self.message_handler(commands=['generate'])
        def on_generate(message):
            try:
                context = message.text.split(' ', 1)[1]
            except IndexError:
                self.reply_to(message, "Please provide the context of the codebase you want to generate by sending `/generate <context>`", parse_mode='Markdown')
                return
            
            if len(context.strip()) > 0:
                token_count = '{:,}'.format(count_tokens(context, "gpt-4"))
                self.reply_to(message, f"Generating codebase with your provided context (Est. {token_count} tokens).\n\n_⚙️ Please wait, this may take a while ..._", parse_mode='Markdown')
                
                response = self.model.generate_codebase(context)
                
                tmp = get_temp_dir()
                
                builder = CodebaseBuilder(project_folder=os.path.join(tmp, response['project']))
                builder.build_codebase(response)
                
                # Send the folder to telegram
                
                # Clean up the build
                