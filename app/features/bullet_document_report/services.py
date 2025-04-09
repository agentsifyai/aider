import os
from typing import List
from infra.llm.service import LLMService
from infra.pdf.service import PdfAnalyzerService
from dotenv import load_dotenv
from app.features.bullet_document_report.models import PDFDocument
from app.features.bullet_document_report.prompts import Prompts
from app.domain.models import MinimalDefect
import asyncio
import json

# Load environment variables
load_dotenv(override=True)  # Add override=True to force reload

class BulletDocumentReportAnalysisService:
    """Service for processing PDFs and generating summaries."""
    
    def __init__(self):
        self.llm: LLMService = LLMService()
        self.prompts: Prompts = Prompts()
        self.pdf_analyzer: PdfAnalyzerService = PdfAnalyzerService()

    # TODO extract this to separate file
    def get_document_delimited(self, text: str) -> str:
        return f"<document>{text}</document>"


    def generate_report_location(self, text) -> str:
        return self.ask_llm(text, [
                    { "role": "system", "content": self.prompts.get_stored_prompt('assistant_system_prompt')},
                    {"role": "user", "content": self.prompts.get_stored_prompt('defects_location_instructions') + self.get_document_delimited(text)},
                ]) + "\n\n"


    async def generate_defect_list(self, text: str, location_prompt: str) -> List[MinimalDefect]:
        lines = text.split("\n")
        chunk_size = 15

        async def process_chunk(chunk):
            """Asynchronously process a single chunk."""
            return await self.llm.ask_async([
                {"role": "system", "content": self.prompts.get_stored_prompt('assistant_system_prompt')},
                {"role": "user", "content": self.prompts.get_defect_list_instructions(location_prompt) + self.get_document_delimited(chunk)},
            ])

        # Split text into chunks
        chunks = ["\n".join(lines[i:i + chunk_size]) for i in range(0, len(lines), chunk_size)]

        # Create asyncio tasks for each chunk
        tasks = [process_chunk(chunk) for chunk in chunks]

        # Run tasks concurrently and gather results
        defect_lists_results = await asyncio.gather(*tasks)

        all_defects: List[MinimalDefect] = []

        for raw_defect_list in defect_lists_results:
            sanitized_defect_list = raw_defect_list.replace("```", "").replace("json", '').replace("I don't know.", "").replace("I don't know", "")
            try:
                chunk_found_defects: List[MinimalDefect] = json.loads(sanitized_defect_list)
                if isinstance(chunk_found_defects, list):
                    print(f"Found {len(chunk_found_defects)} defects in chunk.")
                    all_defects.extend(chunk_found_defects)
                else:
                    print(f"Unexpected result: {raw_defect_list}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                print(f"Raw defect list: {raw_defect_list}")

        # Join results and return
        return all_defects


    async def process_pdf(self, file_path):
        """Process a PDF file and return a PDFDocument with summary."""
        filename = os.path.basename(file_path)
        content = self.pdf_analyzer.read_pdf(file_path)
        location = self.generate_report_location(content)
        defects_lists = await self.generate_defect_list(content, location)

        return PDFDocument(
            filename, 
            content, 
            str(defects_lists).replace("\"", "\\\"").replace("'", '"') # format into json string
            )
