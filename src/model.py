# Contains the functionality to send and receive the prompts and codebase responses from OpenAI
from json import loads
from openai import OpenAI

from os.path import join, dirname, isdir
from os import getenv, getcwd, mkdir
from dotenv import load_dotenv, find_dotenv
import json

from .logger import logger


class CodebaseModel(OpenAI):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initializes the translator object.
        
        Args:
            api_key (str): Your OpenAI API key
            model (str, optional): The OpenAI model to use. Defaults to "gpt-3.5-turbo".
        """
        super().__init__(api_key=api_key)
        self.model = model
    
    
    def _call_api(self, prompt: str, retries: int = 3) -> dict:
        """
        Handles the call to the OpenAI API ChatCompletions endpoint, and the parsing of the response.
        
        Args:
            prompt (str): The formatted prompt string
            retries (int): The number of times to retry if an error occurs. Default is 3.

        Returns:
            dict: The parsed response in the format of: {"success": bool, "message": str}
        """
        response = None
        try:
            response = self.chat.completions.create(model=self.model,
            messages=[{"role": "user", "content": prompt}])
                        
            return loads(response.choices[0].message.content.strip())

        except Exception as err:
            if retries > 0:
                return self._call_api(prompt, retries-1)
            else:
                logger.error(f"Received an error while parsing the response from the API: {str(err)}\nWith response: {response}\nFor prompt: {prompt}")
                return {"success": False, "message": f"API response could not be loaded (see logs): {str(err)}"}


    def generate_codebase(self, context: str) -> dict:
        """
        Generate the JSON response containing the subprocess calls for the desired codebase.

        Args:
            context (str): The complex for the low-complexity software architecture desired.

        Returns:
            dict: Returns the dict object from the self._call_api return
        """
        # Format the translate.txt prompt file to construct the detailed prompt for the translation task
        with open(join(dirname(__file__), 'resources', 'prompts', 'prompt.txt'), 'r') as f:
            prompt = f.read().format(context=context)
            
        print("PROMPT:", prompt)
            
        response = self._call_api(prompt)
        
        # Process response and return the JSON object
        
        
        print(f"\nRESPONSE:")
        print(json.dumps(response, indent=2))

        return response