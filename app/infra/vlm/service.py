import os
from openai import OpenAI, AsyncOpenAI

from app.infra.vlm.prompts import Prompts

import logging

class VlmService:
    """
    Vision Language Model Service for interaction with scanned reports.
    """
    # TODO: Consider making these values ENUMs that we can more easily reference elsewhere.
    DEFAULT_MODEL = "gpt-4.1"
    DEFAULT_TEMPERATURE = 0.7

    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        logging.info(f"Loading OpenAI API key: {'Found' if api_key else 'Not found'}")
        if not api_key:
            logging.warning("WARNING: OPENAI_API_KEY environment variable is not set")
            # We'll initialize without the key, but operations will fail
            self.client = None
            self.client_async = None
        else:
            self.client = OpenAI(api_key=api_key)
            self.client_async = AsyncOpenAI(api_key=api_key)
        self.prompts = Prompts()

    def _sanitize_markdown(self, markdown: str) -> str:
        logging.debug(f"Sanitizing markdown content: {markdown}")
        """
        Sanitize markdown content to ensure it is safe for display.
        :param markdown: Markdown content to sanitize.
        :return: Sanitized markdown content.
        """
        # Implement any necessary sanitization logic here
        return markdown.replace("```markdown", "").replace("```", "")

    def extract_scanned_report_as_markdown(self, file_path: str) -> str:
        """
        Get report as markdown text. Function design to handle scanned reports.
        :file_path: Path to the report file
        :return: Report as markdown
        """
        if not self.client:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
        try:
            logging.info("Asking LLM")
            logging.debug(f"Messages: {self.prompts.get_scanned_report_messages(file_path)}")
            response = self.client.chat.completions.create(
                model=self.DEFAULT_MODEL,
                messages=self.prompts.get_scanned_report_messages(file_path),
                temperature=self.DEFAULT_TEMPERATURE,
            )
            logging.info("LLM response received")
            logging.debug(f"Response: {response}")
            output = response.choices[0].message.content
            return self._sanitize_markdown(output)
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            return f"Error asking llm: {str(e)}"
    
    async def extract_scanned_report_as_markdown_async(self, file_path: str) -> str:
        """
        Get report as markdown text. Function design to handle scanned reports.
        :file_path: Path to the report file
        :return: Report as markdown
        """
        if not self.client:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
        try:
            logging.info("Asking LLM asynchronously")
            logging.debug(f"Messages: {self.prompts.get_scanned_report_messages(file_path)}")
            response = await self.client_async.chat.completions.create(
                model=self.DEFAULT_MODEL,
                messages=self.prompts.get_scanned_report_messages(file_path),
                temperature=self.DEFAULT_TEMPERATURE,
            )
            logging.info("LLM response received")
            logging.debug(f"Response: {response}")
            output = response.choices[0].message.content
            return self._sanitize_markdown(output)
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            return f"Error asking llm: {str(e)}"
