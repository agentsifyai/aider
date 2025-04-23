from typing import List

from app.features.defect_report_analysis.data.extractor import ReportDataExtractor

from app.features.defect_report_analysis.strategy.bullet_report.strategies import BulletReportDefectIdentificationStrategy
from app.features.defect_report_analysis.strategy.detailed_report.strategies import DetailedReportDefectIdentificationStrategy
from app.features.defect_report_analysis.strategy.router import StrategyRouter

from dotenv import load_dotenv
import json, logging, os

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

        logging.info(f"Processing file: {filename}")
        content = await self.extractor.extract_markdown(file_path)

        logging.info(f"Choosing strategy...")
        strategy = await StrategyRouter(self.strategies).choose_strategy(content)

        logging.info("Generating defect list...")
        defects_list = await strategy.identify_defects(content)
        
        logging.info("Processing finished. Returning processed data to view...")
        return DefectList(
            filename,
            content,
            json.dumps(defects_list), # format into json string
            len(defects_list)
        )
