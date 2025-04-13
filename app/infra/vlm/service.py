import os
from openai import OpenAI, AsyncOpenAI

from app.infra.vlm.prompts import Prompts

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
        self.prompts = Prompts()

    def _sanitize_markdown(self, markdown: str) -> str:
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
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.prompts.get_scanned_report_messages(file_path),
                temperature=0.8,
            )
            output = response.choices[0].message.content
            return self._sanitize_markdown(output)
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
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
            response = await self.client_async.chat.completions.create(
                model="gpt-4o",
                messages=self.prompts.get_scanned_report_messages(file_path),
                temperature=0.8,
            )
            output = response.choices[0].message.content
            return self._sanitize_markdown(output)
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return f"Error asking llm: {str(e)}"
        