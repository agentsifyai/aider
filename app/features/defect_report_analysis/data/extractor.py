from app.domain.models import MarkdownReport
from app.infra.vlm.service import VlmService
from app.infra.pdf.service import PdfReaderService

class ReportDataExtractor:
    file_path: str

    def __init__(self) -> None:
        self.vlm = VlmService()
        self.pdf_reader = PdfReaderService()

    async def extract_markdown(self, file_path: str) -> MarkdownReport:
        """Extracts content from a file as markdown."""
        # If the file is a scanned report, use VLM service to extract text
        # content = await self.vlm.extract_scanned_report_as_markdown_async(file_path)
        content = self.pdf_reader.read_pdf_text_as_markdown(file_path)
        return MarkdownReport(content)