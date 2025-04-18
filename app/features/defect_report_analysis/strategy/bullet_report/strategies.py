from typing import List, Dict

from app.domain.models import PotentialDefect, DetailedPotentialDefect, MarkdownReport
from app.features.defect_report_analysis.strategy.base import DefectIdentificationStrategy, DefectDetailingStrategy
from app.features.defect_report_analysis.strategy.bullet_report.prompts import Prompts
from app.features.defect_report_analysis.strategy.bullet_report.chunker import LocationSectionChunker

from app.infra.llm.service import LLMService

import asyncio, json, logging

class BulletReportDefectDetailingStrategy(DefectDetailingStrategy):
    """
    Bullet Report Defect Detailing Strategy
    This strategy is used to detail defects in a bullet report type.
    It uses the bullet report's content and metadata to detail defects.
    """

    # We can move the state through the constructor if needed
    def __init__(self, defect_identification_strategy: "BulletReportDefectDetailingStrategy") -> None:
        super().__init__()


    async def detail_defect(self, defect: PotentialDefect) -> DetailedPotentialDefect:
        raise NotImplementedError("This method should be overridden by subclasses")


class BulletReportDefectIdentificationStrategy(DefectIdentificationStrategy):
    """
    Bullet Report Defect Identification Strategy
    This strategy is used to identify defects in a bullet report type.
    It uses the bullet report's content and metadata to identify defects.
    """

    metadata: Dict[str, str] = {}
    llm: LLMService = LLMService()
    prompts: Prompts = Prompts()
    chunker: LocationSectionChunker = LocationSectionChunker()

    def __init__(self):
        super().__init__()

    def selection_criteria() -> str:
        return NotImplementedError("Not overriden yet")
    
    def detailing_strategy(self) -> DefectDetailingStrategy:
        return BulletReportDefectDetailingStrategy(self)

    def generate_location_metadata(self, text) -> str:
        return self.llm.ask([
                    { "role": "system", "content": self.prompts.ASSISTANT_SYSTEM_PROMPT },
                    {"role": "user", "content": self.prompts.get_stored_prompt('defects_location_instructions') + Prompts.delimit_document(text)},
                ])
    
    def parse_flatten_raw_defect_lists(self, defect_lists_strings: List[str]) -> List[PotentialDefect]:
        """Parse the raw defect list JSONs into a List of Minimal Defects."""
        all_defects: List[PotentialDefect] = []

        for raw_defect_list in defect_lists_strings:
            sanitized_defect_list = raw_defect_list.replace("```", "").replace("json", '').replace("I don't know.", "").replace("I don't know", "")
            try:
                chunk_found_defects: List[PotentialDefect] = json.loads(sanitized_defect_list)
                if isinstance(chunk_found_defects, list):
                    logging.debug(f"Found {len(chunk_found_defects)} defects in chunk.")
                    all_defects.extend(chunk_found_defects)
                else:
                    logging.warning(f"Unexpected result: {raw_defect_list}")
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error: {str(e)}")
                logging.debug(f"Raw defect list: {raw_defect_list}")

        # Join results and return
        return all_defects

    async def process_chunk(self,chunk):
        """Asynchronously process a single chunk."""
        return await self.llm.ask_async([
            {"role": "system", "content": self.prompts.ASSISTANT_SYSTEM_PROMPT },
            {"role": "user", "content": self.prompts.get_defect_list_instructions(self.metadata["location"]) + Prompts.delimit_document(chunk)},
        ])

    async def generate_defect_list(self, text: str) -> List[PotentialDefect]:
        # Split text into chunks
        logging.info("Report chunking")
        chunks = await self.chunker.get_chunks(text)
        logging.debug(chunks)
        # Create asyncio tasks for each chunk
        tasks = [self.process_chunk(chunk) for chunk in chunks]
        logging.info("Defect list generation")
        # Run tasks concurrently and gather results
        raw_defect_lists_results = await asyncio.gather(*tasks)

        return self.parse_flatten_raw_defect_lists(raw_defect_lists_results)
    

    async def identify_defects(self, report: MarkdownReport) -> List[PotentialDefect]:
        logging.info("Identifying defects in bullet report...")
        logging.debug("Inferring location metadata...")
        self.metadata["location"] = self.generate_location_metadata(report.content)
        defects = await self.generate_defect_list(report.content)
        logging.debug(f"Defects identified: {defects}")
        return defects