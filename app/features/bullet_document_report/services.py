from typing import List

from app.infra.llm.service import LLMService
from app.infra.output.models import DefectList
from app.infra.pdf.service import PdfAnalyzerService
from app.features.bullet_document_report.prompts import Prompts
from app.domain.models import MinimalDefect

from dotenv import load_dotenv
import asyncio
import json
import os

# Load environment variables
load_dotenv(override=True)  # Add override=True to force reload

class BulletDocumentReportAnalysisService:
    """Service for processing PDFs and generating summaries."""
    
    def __init__(self):
        self.llm: LLMService = LLMService()
        self.prompts: Prompts = Prompts()
        self.pdf_analyzer: PdfAnalyzerService = PdfAnalyzerService()


    def generate_report_location(self, text) -> str:
        return self.llm.ask([
                    { "role": "system", "content": self.prompts.get_stored_prompt('assistant_system_prompt')},
                    {"role": "user", "content": self.prompts.get_stored_prompt('defects_location_instructions') + Prompts.delimit_document(text)},
                ]) + "\n\n"
    

    def parse_flatten_raw_defect_lists(self, defect_lists_strings: List[str]) -> List[MinimalDefect]:
        """Parse the raw defect list JSONs into a List of Minimal Defects."""
        all_defects: List[MinimalDefect] = []

        for raw_defect_list in defect_lists_strings:
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


    async def generate_defect_list(self, text: str, location_prompt: str) -> List[MinimalDefect]:
        lines = text.split("\n")
        chunk_size = 15

        async def process_chunk(chunk):
            """Asynchronously process a single chunk."""
            return await self.llm.ask_async([
                {"role": "system", "content": self.prompts.get_stored_prompt('assistant_system_prompt')},
                {"role": "user", "content": self.prompts.get_defect_list_instructions(location_prompt) + Prompts.delimit_document(chunk)},
            ])

        # Split text into chunks
        chunks = ["\n".join(lines[i:i + chunk_size]) for i in range(0, len(lines), chunk_size)]

        # Create asyncio tasks for each chunk
        tasks = [process_chunk(chunk) for chunk in chunks]

        # Run tasks concurrently and gather results
        raw_defect_lists_results = await asyncio.gather(*tasks)

        return self.parse_flatten_raw_defect_lists(raw_defect_lists_results)


    async def process_report(self, file_path):
        """Process a PDF file and return a PDFDocument with summary."""
        filename = os.path.basename(file_path)
        content = self.pdf_analyzer.read_pdf_as_text(file_path)
        location = self.generate_report_location(content)
        defects_list = await self.generate_defect_list(content, location)

        return DefectList(
            filename,
            content,
            json.dumps(defects_list) # format into json string
        )
