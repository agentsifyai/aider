from typing import List, Dict, Any

from app.features.defect_report_analysis.common.prompts import COMMON_DETAILING_SYSTEM_PROMPT, get_common_detailing_user_prompt
from app.features.defect_report_analysis.common.schemas import COMMON_DETAILING_SCHEMA, response_format_from_schema

from app.domain.models import PotentialDefect, DetailedPotentialDefect, MarkdownReport
from app.features.defect_report_analysis.strategy.base import DefectDetailingStrategy
from app.infra.llm.service import LLMService

import json, logging, asyncio

# This class essentially does not work as intended, because the defect details are stored as dictionaries in the JSON response.
# TODO The class is used to convert the dictionaries to objects, but it does not work as expected.
class CommonDefectDetails:
    defect_id: str
    verbose_description: str
    defect_cause: str

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class CommonDefectDetailingStrategy(DefectDetailingStrategy):

    llm: LLMService = LLMService()
    report: MarkdownReport
    metadata: Dict[str, Any] = {}

    def __init__(self, report: MarkdownReport) -> None:
        super().__init__()
        self.report = report

    async def detail_defect_group(self, defect_group: List[PotentialDefect]) -> List[DetailedPotentialDefect]:
        result = await self.llm.ask_async([
            {"role": "system", "content": COMMON_DETAILING_SYSTEM_PROMPT},
            {"role": "user", "content": get_common_detailing_user_prompt(defect_group, self.report.content)},
            ], response_format_from_schema(COMMON_DETAILING_SCHEMA))
        try:
            defect_details: List[CommonDefectDetails] = json.loads(result)["defects"]
            logging.debug(f"Defect details: {defect_details}")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
            defect_details = []
        
        detailed_defects = []

        defect_mapping = {d_details["defect_id"]:d_details for d_details in defect_details}
        defect_ids = set(defect_mapping.keys())

        for defect in defect_group:
            d = DetailedPotentialDefect(**defect.__dict__)
            if defect.id in defect_ids:
                d.verbose_description = defect_mapping[defect.id]["verbose_description"]
                d.defect_cause = defect_mapping[defect.id]["defect_cause"]
            detailed_defects.append(d)

        return detailed_defects

    async def detail_defects(self, defects: List[PotentialDefect]) -> List[DetailedPotentialDefect]:
        # Group defects into groups of 10
        grouped = [defects[i:i+10] for i in range(0, len(defects), 10)]
        # Process each group asynchronously
        tasks = [self.detail_defect_group(group) for group in grouped]
        results = await asyncio.gather(*tasks)
        # Flatten the list of lists into a single list
        detailed_defects = [item for sublist in results for item in sublist]
        return detailed_defects