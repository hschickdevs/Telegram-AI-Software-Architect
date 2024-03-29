from .telegram import CodebaseArchitectBot
from .utils import handle_env, get_commands, clean_temp_dir
from .logger import logger
from .models import CodebaseModel

import threading
from os import getenv
from time import sleep
from telebot import types

RESTART_DELAY = 5  # The number of seconds to wait before restarting the bot after an error is thrown

def start_bot(bot_instance: CodebaseArchitectBot):
    try:
        bot_instance.polling()
    except Exception as err:
        logger.error(f"An error occurred while polling: {err}", exc_info=err)

if __name__ == "__main__":
    handle_env()
        
    model = CodebaseModel(getenv("API_KEY"), model=getenv("MODEL"), model_code=getenv("MODEL_CODE"))
    bot = CodebaseArchitectBot(getenv("BOT_TOKEN"), model=model)
    
    # Set the bot commands:
    user_commands = [types.BotCommand(command=command, description=description)
                     for command, description in get_commands(model=getenv("MODEL_CODE")).items()]
    bot.set_my_commands(user_commands)

    # Start the bot
    while True:
        logger.info(f"Bot started with token {getenv('BOT_TOKEN')} using {model.model} ...")

        # Start bot polling as a daemon thread (so that it can be stopped by KeyboardInterrupt in the main thread)
        polling_thread = threading.Thread(target=start_bot, args=(bot,), daemon=True)
        polling_thread.start()

        try:
            # Keep the main thread running to allow daemon threads to run
            while polling_thread.is_alive():
                sleep(1)
        except KeyboardInterrupt:
            logger.info("Bot stopped by the console.")
            break
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err}")

        logger.info(f"Restarting bot in {RESTART_DELAY} seconds...")
        sleep(RESTART_DELAY)