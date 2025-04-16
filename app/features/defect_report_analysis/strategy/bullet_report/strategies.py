from typing import List

from app.domain.models import PotentialDefect, DetailedPotentialDefect, MarkdownReport, MinimalDefect
from app.features.defect_report_analysis.strategy.base import DefectIdentificationStrategy, DefectDetailingStrategy
from app.features.defect_report_analysis.strategy.bullet_report.prompts import Prompts

from app.infra.llm.service import LLMService

import asyncio, json


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

    def __init__(self):
        super().__init__()
        self.llm: LLMService = LLMService()
        self.prompts: Prompts = Prompts()

    def selection_criteria() -> str:
        return NotImplementedError("Not overriden yet")
    
    def detailing_strategy(self) -> DefectDetailingStrategy:
        return BulletReportDefectDetailingStrategy(self)

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
    

    async def identify_defects(self, report: MarkdownReport) -> List[PotentialDefect]:
        location_prompt = self.generate_report_location(report.content)
        defects = await self.generate_defect_list(report.content, location_prompt)
        #TODO: potential defects here
        return defects