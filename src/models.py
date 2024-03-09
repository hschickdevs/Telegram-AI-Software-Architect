# Contains the functionality to send and receive the prompts and codebase responses from OpenAI
from json import loads
from openai import OpenAI
from anthropic import Anthropic

from os.path import join, dirname, isdir
from os import getenv, getcwd, mkdir
from dotenv import load_dotenv, find_dotenv
import json

from .logger import logger


class CodebaseModel:
    def __init__(self, api_key: str, model: str, model_code: str = None):
        """
        Initializes the translator object.
        
        Args:
            api_key (str): Your OpenAI API key
            model (str): claude or openai are the current available models
            model_code (str): The Claude or OpenAI model to use.
        """
        models = {"claude": "claude-3-opus-20240229", "openai": "gpt-4-0125-preview"}  # contains the available models and the default model codes
        assert model in models.keys(), f"'{model}' model not supported."
        
        self.model = model
        self.model_code = model_code if model_code else models[model]
        
        # Create model connectors
        self.openai = OpenAI(api_key=api_key) if model == "openai" else None
        self.claude = Anthropic(api_key=api_key) if model == "claude" else None
    
    
    def _call_openai(self, prompt: str, fmt: str = "json", retries: int = 1) -> dict:
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
            response = self.openai.chat.completions.create(model=self.model_code,
            messages=[{"role": "user", "content": prompt}])
            
            logger.debug(f"OpenAPI Response: {response}")
            
            if fmt == "json": 
                return loads(response.choices[0].message.content.strip())
            elif fmt == "str":
                return response.choices[0].message.content.strip()
            else:
                raise NotImplementedError("Invalid format (str or json)")

        except Exception as err:
            if retries > 0:
                return self._call_openai(prompt, fmt, retries-1)
            else:
                logger.error(f"Received an error while parsing the response from the OpenAI API: {str(err)}\nWith response: {response}\nFor prompt: {prompt}")
                return {"error": True, "message": f"API response could not be loaded (see logs): {str(err)}"}


    def _call_claude(self, prompt: str, fmt: str = "json", retries: int = 1) -> dict:
        """
        Handles the call to the Claude Messages endpoint, and the parsing of the response.
        
        Args:
            prompt (str): The formatted prompt string
            retries (int): The number of times to retry if an error occurs. Default is 3.

        Returns:
            dict: The parsed response in the format of: {"success": bool, "message": str}
        """
        response = None
        try:
            message = self.claude.messages.create(
                model=self.model_code,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            logger.debug(f"Claude Response: {message}")
            
            if fmt == "json":
                return loads(message.content[0].text.strip())
            elif fmt == "str":
                return message.content[0].text.strip()
            else:
                raise NotImplementedError("Invalid format (str or json)")

        except Exception as err:
            if retries > 0:
                return self._call_claude(prompt, fmt, retries-1)
            else:
                logger.error(f"Received an error while parsing the response from the Anthropic (Claude) API: {str(err)}\nWith response: {response}\nFor prompt: {prompt}")
                return {"error": True, "message": f"API response could not be loaded (see logs): {str(err)}"}


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
        
        if self.model == "openai":
            response = self._call_openai(prompt)
        else:
            response = self._call_claude(prompt)
        
        # Process response and return the JSON object
        
        
        print(f"\nRESPONSE:")
        print(json.dumps(response, indent=2))

        return response
    
    def generic_call(self, context: str) -> str:
        """
        Used by the /ask command to generate generic responses instead of JSON formatted codebases.
        
        Args:
            context (str): The context of what to ask.

        Returns:
            str: Returns a string object representing the API response.
        """
        with open(join(dirname(__file__), 'resources', 'prompts', 'prompt_ask.txt'), 'r') as f:
            prompt = f.read().format(context=context)
        
        # Format the translate.txt prompt file to construct the detailed prompt for the translation task 
        print("PROMPT:", context)
        
        if self.model == "openai":
            response = self._call_openai(prompt, "str")
        else:
            response = self._call_claude(prompt, "str")
    
        return response