from os.path import join, dirname, isdir, abspath, exists
from os import getenv, getcwd, mkdir, listdir, remove
from dotenv import load_dotenv, find_dotenv

import tiktoken
    

def get_command_template(context: str) -> str:
    """
    Open the /resources directory relative to __file__ and read the help.txt file.

    Args:
        context (str): The template's filename without the extension

    Returns:
        str: The corresponding prompt template in Markdown to be formatted by the Telegram bot
    """
    with open(join(dirname(__file__), 'resources', 'templates', f'{context}.md'), 'r', encoding='utf8') as f:
        return f.read()


def handle_env():
    """Checks if the .env file exists in the current working dir, and imports the variables if so"""
    try:
        envpath = find_dotenv(raise_error_if_not_found=True, usecwd=True)
        load_dotenv(dotenv_path=envpath)
    except:
        pass
    finally:
        mandatory_vars = ['BOT_TOKEN', 'API_KEY']
        for var in mandatory_vars:
            val = getenv(var)
            if val is None:
                raise ValueError(f"Missing environment variable: {var}")
            
def get_logfile() -> str:
    log_dir = join(getcwd(), 'logs')
    if not isdir(log_dir):
        mkdir(log_dir)
    return join(log_dir, 'log.txt')


def get_commands() -> dict:
    """Fetches the commands from the templates for the help command"""
    commands = {}
    
    # Define the path to the commands.txt file
    file_path = join(dirname(abspath(__file__)), 'resources', 'commands.txt')
    
    with open(file_path, 'r') as f:
        for line in f.readlines():
            # Splitting at the first '-' to separate command and description
            command, description = line.strip().split(' - ', 1)
            commands[command.strip()] = description.strip()
            
    return commands


def get_temp_dir() -> str:
    """
    Returns the path to the tmp directory.
    """
    tmp_dir = join(getcwd(), 'tmp')
    if not exists(tmp_dir):
        mkdir(tmp_dir)
    return tmp_dir



def clean_temp_dir() -> str:
    """
    Clears the tmp directory.
    
    :return: The path to the tmp directory.
    """
    tmp_dir = get_temp_dir()
    for filename in listdir(tmp_dir):
        remove(join(tmp_dir, filename))
        
    return tmp_dir


def count_tokens(text, model_name):
    return len(tiktoken.encoding_for_model(model_name).encode(text))