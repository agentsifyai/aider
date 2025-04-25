from typing import List, Dict, Any

from app.domain.models import PotentialDefect, MarkdownReport
from app.features.defect_report_analysis.common.strategies import CommonDefectDetailingStrategy
from app.features.defect_report_analysis.strategy.base import DefectIdentificationStrategy, DefectDetailingStrategy
from app.features.defect_report_analysis.strategy.detailed_report.prompts import Prompts

from app.infra.llm.service import LLMService

import json, logging


class DetailedReportDefectIdentificationStrategy(DefectIdentificationStrategy):
    """
    Detailed Report Defect Identification Strategy
    This strategy is used to identify defects in a detailed report type.
    """

    metadata: Dict[str, Any] = {}
    llm: LLMService = LLMService()
    prompts: Prompts = Prompts()

    def __init__(self):
        super().__init__()

    def selection_criteria(self) -> str:
        return """
        - The report contains sections describing different aspects of the defects.
        - Report may contain defect doucumentation, such as screenshots, logs, or other artifacts.
        - Defects in the report are described in a single section, whereas other sections in the report contain other information about the defects.
        - The report may contain a summary of the defects, but the details are in the sections.
        """
    
    def detailing_strategy(self) -> DefectDetailingStrategy:
        return CommonDefectDetailingStrategy(self.metadata["report"])

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
        self.metadata["report"] = report
        defects = await self.generate_defect_list(report.content)
        logging.debug(f"Defects identified: {defects}")
        return defects