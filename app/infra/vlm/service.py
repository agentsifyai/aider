import os
from openai import OpenAI, AsyncOpenAI

from app.infra.vlm.prompts import get_scanned_report_messages

class VlmService:
    """
    Vision Language Model Service for interaction with scanned reports.
    """

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

    def extract_scanned_report_as_markdown(self, file_path: str) -> str:
        """
        Get report as markdown text. Function design to handle scanned reports.
        :file_path: Path to the report file
        :return: Report as markdown
        """
        if not self.client:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=get_scanned_report_messages(file_path),
                temperature=0.8,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return f"Error asking llm: {str(e)}"
    
    async def extract_scanned_report_as_markdown(self, file_path: str) -> str:
        """
        Get report as markdown text. Function design to handle scanned reports.
        :file_path: Path to the report file
        :return: Report as markdown
        """
        if not self.client:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=get_scanned_report_messages(file_path),
                temperature=0.8,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return f"Error asking llm: {str(e)}"
        