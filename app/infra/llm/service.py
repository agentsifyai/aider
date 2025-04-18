from typing import Dict, List
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
import os

import logging

class LLMService:

    DEFAULT_MODEL = "gpt-4.1"

    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        print(f"Loading OpenAI API key: {'Found' if api_key else 'Not found'}")
        if not api_key:
            print("WARNING: OPENAI_API_KEY environment variable is not set")
            # We'll initialize without the key, but operations will fail
            self.client = None
            self.client_async = None
        else:
            self.client = OpenAI(api_key=api_key)
            self.client_async = AsyncOpenAI(api_key=api_key)

    #TODO should token limits be implemented here?

    def ask(self, messages: List[Dict[str, str]] | ChatCompletionMessageParam) -> str:
        """Ask llms questions about text using OpenAI's API."""
        if not self.client:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
            
        try:
            logging.info("Asking LLM")
            logging.debug(f"Messages: {messages}")
            response = self.client.chat.completions.create(
                model=self.DEFAULT_MODEL,
                messages=messages
            )
            logging.info("LLM response received")
            logging.debug(f"Response: {response}")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            return f"Error asking llm: {str(e)}"
        
    async def ask_async(self, messages: List[Dict[str, str]] | ChatCompletionMessageParam):
        """Ask llms questions about text using OpenAI's API."""
        if not self.client:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
            
        try:
            logging.info("Asking LLM asynchronously")
            logging.debug(f"Messages: {messages}")
            response = await self.client_async.chat.completions.create(
                model=self.DEFAULT_MODEL,
                messages=messages
            )
            logging.info("LLM response received")
            logging.debug(f"Response: {response}")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            return f"Error asking llm: {str(e)}"