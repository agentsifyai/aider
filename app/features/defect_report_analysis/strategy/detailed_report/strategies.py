from typing import List, Dict

from app.domain.models import PotentialDefect, DetailedPotentialDefect, MarkdownReport
from app.features.defect_report_analysis.strategy.base import DefectIdentificationStrategy, DefectDetailingStrategy
from app.features.defect_report_analysis.strategy.detailed_report.prompts import Prompts

from app.infra.llm.service import LLMService

import asyncio, json, logging


class DetailedReportDefectDetailingStrategy(DefectDetailingStrategy):
    """
    Bullet Report Defect Detailing Strategy
    This strategy is used to detail defects in a bullet report type.
    It uses the bullet report's content and metadata to detail defects.
    """

    # We can move the state through the constructor if needed
    def __init__(self, defect_identification_strategy: "DetailedReportDefectIdentificationStrategy") -> None:
        super().__init__()


    async def detail_defect(self, defect: PotentialDefect) -> DetailedPotentialDefect:
        raise NotImplementedError("This method should be overridden by subclasses")


class DetailedReportDefectIdentificationStrategy(DefectIdentificationStrategy):
    """
    Bullet Report Defect Identification Strategy
    This strategy is used to identify defects in a bullet report type.
    It uses the bullet report's content and metadata to identify defects.
    """

    metadata: Dict[str, str] = {}
    llm: LLMService = LLMService()
    prompts: Prompts = Prompts()

    def __init__(self):
        super().__init__()

    def selection_criteria() -> str:
        return NotImplementedError("Not overriden yet")
    
    def detailing_strategy(self) -> DefectDetailingStrategy:
        return DetailedReportDefectDetailingStrategy(self)

    async def generate_defect_list(self, text: str) -> List[PotentialDefect]:
        # Split text into chunks
        # Create asyncio tasks for each chunk
        logging.info("Generating defect list...")
        result = await self.llm.ask_async([
            {"role": "system", "content": self.prompts.ASSISSTANT_SYSTEM_PROMPT },
            {"role": "user", "content": self.prompts.DEFECT_LIST_INTRUCTIONS + Prompts.delimit_document(text)},
        ])
        

        return json.loads(result)
    

    async def identify_defects(self, report: MarkdownReport) -> List[PotentialDefect]:
        logging.info("Identifying defects with Detailed Report Id strategy...")
        defects = await self.generate_defect_list(report.content)
        logging.debug(f"Defects identified: {defects}")
        return defects