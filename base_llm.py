from abc import ABC, abstractmethod
import asyncio, os, yaml, requests, json, logging
from openai import AzureOpenAI
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LanguageModelInterface(ABC):
    """
    An abstract base class for language model interfaces.

    This class defines the basic structure and necessary methods that any language model interface should implement.
    """        
    @abstractmethod
    def generate_response(self, prompt) -> str:
        """
        Generates a response to the given prompt synchronously.

        Args:
            prompt (str): The input prompt to which the language model should respond.

        Returns:
            str: The generated response from the language model.
        """
        pass
                
    @abstractmethod
    async def async_generate_response(self, prompt) -> str:
        """
        Generates a response to the given prompt asynchronously.

        Args:
            prompt (str): The input prompt to which the language model should respond.

        Returns:
            str: The generated response from the language model.
        """
        pass
    
    @abstractmethod
    def setup_config(self):
        """
        Sets up the configuration for the language model interface.

        This method should handle the initialization of necessary configurations required by the language model.
        """
        pass
    
    @abstractmethod
    def initialize_conversation_history(self):
        """
        Initializes the conversation history.

        This method should set up an initial state or history for the conversation, if the model maintains one.
        """
        pass

    @abstractmethod
    def delete_conversation_history(self):
        """
        Deletes or resets the conversation history.

        This method is responsible for clearing or resetting the conversation history maintained by the model.
        """
        pass
    

class openai(LanguageModelInterface):
    """
    A concrete implementation of the LanguageModelInterface for the OpenAI GPT models.

    This class handles interactions with OpenAI's GPT models, including configuration setup, conversation history management, and response generation.

    Attributes:
        config (dict): Configuration settings for the OpenAI model.
        client: The client instance for interacting with OpenAI's API.
        model_key (str): The model key for the specific GPT model.
        api_type (str): Type of API being used ('openai_api' or others).
        conversation (list): A list of conversation history.
    """
    
    def __init__(self, config=None):
        """
        Initializes the openai class with the given configuration.

        Args:
            config (dict): Configuration settings for the OpenAI model.
        """
        self.config = config
        self.setup_config()
        self.initialize_conversation_history()

    def setup_config(self):
        provider = os.environ.get('LLM_PROVIDER')
        self.temperature = 0.5
        print(provider)

        if provider.lower() == 'openai':
            api_key = os.environ.get('OPENAI_API_KEY')
            if api_key is None:
                raise Exception('OpenAI API Key is not set.')
            # self.client = OpenAI(api_key=api_key)
            self.model_key = os.environ.get('OPENAI_MODEL')
            self.api_type = 'openai_api'

        elif provider.lower() == 'azure':
            api_key = os.environ.get('AZURE_API_KEY')
            azure_endpoint = os.environ.get('AZURE_API_BASE')
            print(azure_endpoint)
            api_version = os.environ.get('AZURE_API_VERSION')
            if not all([api_key, azure_endpoint, api_version]):
                raise Exception('Missing configuration for Azure OpenAI API.')
            self.client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)
            self.model_key = os.environ.get('AZURE_DEPLOYMENT_NAME')


    def initialize_conversation_history(self):
        self.conversation = []
        self.append_to_conversation_history("system", "You are a cyber security expert.")
        
    def delete_conversation_history(self):
        self.initialize_conversation_history()
        
    def append_to_conversation_history(self, role, content):
        self.conversation.append({"role": role, "content": content})

    def generate_response(self, prompt):
        temperature = self.temperature 
        
        response = self.client.chat.completions.create(
            model=self.model_key, messages=prompt, temperature=temperature)   

        reply = response.choices[0].message.content
        #sprint(f'Total token used for this call: {response.usage.total_tokens}\n')
        #print(reply)
        return reply

    async def async_generate_response(self, prompt):
        return await asyncio.to_thread(self.generate_response, prompt)


class mistral(LanguageModelInterface):
    """
    A concrete implementation of the LanguageModelInterface for the Mistral language model.

    This class is responsible for managing interactions with the Mistral language model, including configuration, response generation, and conversation history.

    Attributes:
        config (dict): Configuration settings for the Mistral model.
        endpoint (str): The endpoint URL for the Mistral model API.
        conversation (list): A list of conversation history.
    """
    
    def __init__(self, config=None):
        """
        Initializes the mistral class with the given configuration.

        Args:
            config (dict): Configuration settings for the Mistral model.
        """
        self.config = config
        self.setup_config()
        self.initialize_conversation_history()
        
    def setup_config(self):
        self.temperature = 0.5

        self.api_key = os.environ.get('API_KEY_MISTRAL')
        if self.api_key is None:
            raise Exception('Mistral api key is not set.') 
        
        self.model_key = os.environ.get('MISTRAL_MODEL')
        self.client = Groq(api_key= self.api_key)

    def initialize_conversation_history(self):
        self.conversation = []
        self.append_to_conversation_history("system", "You are a cyber security expert.")
        
    def delete_conversation_history(self):
        self.initialize_conversation_history()

    def append_to_conversation_history(self, role, content):
        self.conversation.append({"role": role, "content": content})
                
    def generate_response(self, prompt):
        #conversation_append(self.conversation, "user", prompt)

        chat_completion = self.client.chat.completions.create(
            messages=prompt,
            model= self.model_key,
            temperature= self.temperature
        )

        return chat_completion
        

    async def async_generate_response(self, prompt):
        #conversation_append(self.conversation, "user", prompt)
        reply = await asyncio.to_thread(self.generate_response, prompt)
        return reply   

