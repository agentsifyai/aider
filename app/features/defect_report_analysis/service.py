from typing import List

from app.features.defect_report_analysis.data.extractor import ReportDataExtractor

from app.features.defect_report_analysis.strategy.bullet_report.strategies import BulletReportDefectIdentificationStrategy
from app.features.defect_report_analysis.strategy.detailed_report.strategies import DetailedReportDefectIdentificationStrategy

from dotenv import load_dotenv
import json
import os

# Load environment variables
load_dotenv(override=True)  # Add override=True to force reload

# Viewmodel
class DefectList:
    """Model for the generated list of defects."""

    filename: str
    content: str
    defect_list: str
    defect_amount: int

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

    def __init__(self, filename: str, content: str, defect_list: str=None, amount: int=None):
        self.filename = filename
        self.content = content
        self.defect_list = defect_list
        self.defect_amount = amount


# Service
class DefectReportAnalysisService:
    """Service to analyze defect reports."""
    
    def __init__(self):
        self.extractor = ReportDataExtractor()


    async def process_report(self, file_path: str):
        """Process a defect report file"""
        filename = os.path.basename(file_path)

        self.strategies = [
            DetailedReportDefectIdentificationStrategy(),
            BulletReportDefectIdentificationStrategy(),
        ]

        content = await self.extractor.extract_markdown(file_path)
        defects_list = await self.strategies[0].identify_defects(content)

        return DefectList(
            filename,
            content,
            json.dumps(defects_list), # format into json string
            len(defects_list)
        )
