from app.domain.models import MarkdownReport
from app.infra.vlm.service import VlmService
from app.infra.pdf.service import PdfReaderService
from app.infra.xls.service import ExcelReaderService

import logging


class ReportDataExtractor:
    file_path: str

    def __init__(self) -> None:
        self.vlm = VlmService()
        self.pdf_reader = PdfReaderService()
        self.excel_reader = ExcelReaderService()

    def is_scanned_pdf(self, file_path: str) -> bool:
        """Checks if the PDF file is scanned."""
        if "protocole" in file_path.lower():
            return False
        #TODO!!! @Paul: Implement the logic to check if the PDF is scanned
        return True  # Placeholder for actual implementation

    def handle_pdfs(self, file_path) -> str:
        """Handles PDF files."""
        # Use the VLM service to extract text from scanned PDFs
        if self.is_scanned_pdf(file_path):
            return self.vlm.extract_scanned_report_as_markdown(file_path)

        return self.pdf_reader.read_pdf_text_as_markdown(file_path)

    async def extract_markdown(self, file_path: str) -> MarkdownReport:
        """Extracts content from a file as markdown."""
        # If the file is a scanned report, use VLM service to extract text
        match file_path:
            case file_path if file_path.endswith('.pdf'):
                content = self.handle_pdfs(file_path)
            case file_path if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                content = self.excel_reader.read_excel_text_as_markdown(file_path)
            case _:
                raise ValueError("Unsupported file type. Only PDF and Excel files are supported.")
        
        logging.info("Extracted Markdown Report:\n%s", content)

        return MarkdownReport(content)