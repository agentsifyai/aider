from typing import List, Dict, Any

from app.domain.models import PotentialDefect, DetailedPotentialDefect, MarkdownReport
from app.features.defect_report_analysis.common.strategies import CommonDefectDetailingStrategy
from app.features.defect_report_analysis.common.schemas import POTENTIAL_DEFECT_LIST_SCHEMA, response_format_from_schema
from app.features.defect_report_analysis.strategy.base import DefectIdentificationStrategy, DefectDetailingStrategy
from app.features.defect_report_analysis.strategy.bullet_report.prompts import Prompts
from app.features.defect_report_analysis.strategy.bullet_report.chunker import Chunker, Chunk

from app.infra.llm.service import LLMService

import asyncio, json, logging


class BulletReportDefectIdentificationStrategy(DefectIdentificationStrategy):
    """
    Bullet Report Defect Identification Strategy
    This strategy is used to identify defects in a bullet report type.
    It uses the bullet report's content and metadata to identify defects.
    """

    metadata: Dict[str, Any] = {}
    llm: LLMService = LLMService()
    prompts: Prompts = Prompts()
    chunker: Chunker = Chunker()

    def __init__(self):
        super().__init__()

    def selection_criteria(self) -> str:
        return f"""
        - The report contains a list of defects in bullet format.
        - The bullet-listed defects may be grouped in sections by their location.
        - For each listed defect there is no much information aside from the name and the appropriate location.
        - Aside from the list of the defects, report may contain other information, but the defect list is the main content of the document.
        """
    
    def detailing_strategy(self) -> DefectDetailingStrategy:
        return CommonDefectDetailingStrategy(self.metadata["report"])

    def generate_location_metadata(self, text) -> str:
        return self.llm.ask([
                    { "role": "system", "content": self.prompts.ASSISTANT_SYSTEM_PROMPT },
                    {"role": "user", "content": self.prompts.get_stored_prompt('defects_location_instructions') + Prompts.delimit_document(text)},
                ])

    async def process_chunk(self,chunk: Chunk) -> List[PotentialDefect]:
        """Asynchronously process a single chunk to retrieve its potential defects."""
        chunk_defects: List[PotentialDefect] = []

        response = await self.llm.ask_async([
            {"role": "system", "content": self.prompts.ASSISTANT_SYSTEM_PROMPT },
            {"role": "user", "content": self.prompts.get_defect_list_instructions(self.metadata["location"]) 
             + Prompts.delimit_document(f"Page {chunk.page_number}\n" + chunk.chunk_content) },
        ], response_format_from_schema(POTENTIAL_DEFECT_LIST_SCHEMA))
        logging.debug(f"Raw defect list: {response}")

        try:
            chunk_defects = json.loads(response)["defects"]
            logging.debug(f"Chunk defects: {chunk_defects}")
            logging.info(f"Found {len(chunk_defects)} defects in chunk.")
            chunk_defects = [PotentialDefect(**defect, evidence_page=chunk.page_number) for defect in chunk_defects]
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {str(e)}")
            

        return chunk_defects

    async def generate_defect_list(self, text: str) -> List[PotentialDefect]:
        # Split text into chunks
        logging.info("Report chunking")
        chunks = await self.chunker.get_chunks(text)
        logging.debug(chunks)
        # Create asyncio tasks for each chunk
        tasks = [self.process_chunk(chunk) for chunk in chunks]
        logging.info("Defect list generation")
        # Run tasks concurrently and gather results
        defect_lists_by_chunks = await asyncio.gather(*tasks)

        # Flatten the list of lists into a single list
        all_defects = [defect for chunk_defects in defect_lists_by_chunks for defect in chunk_defects]
        return all_defects
    

    async def identify_defects(self, report: MarkdownReport) -> List[PotentialDefect]:
        logging.info("Identifying defects in bullet report...")
        self.metadata["report"] = report
        logging.debug("Inferring location metadata...")
        self.metadata["location"] = self.generate_location_metadata(report.content)
        defects = await self.generate_defect_list(report.content)
        logging.debug(f"Defects identified: {defects}")
        return defects