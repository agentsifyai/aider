from enum import Enum

from app.domain.models import MarkdownReport
from app.infra.vlm.service import VlmService
from app.infra.pdf.service import PdfReaderService
from app.infra.xls.service import ExcelReaderService

import re
import logging
from PyPDF2 import PdfReader

class DocumentType(Enum):
    SCANNED = "scanned"
    MIXED = "mixed"
    TEXT = "text"

class ReportDataExtractor:
    file_path: str

    def __init__(self) -> None:
        self.vlm = VlmService()
        self.pdf_reader = PdfReaderService()
        self.excel_reader = ExcelReaderService()

    def _document_type(self, pdf_metrics: dict) -> DocumentType:
        """Determines the type of document based on its metrics."""
        if pdf_metrics['num_chars'] < 20 and pdf_metrics['num_images'] > 0:
            return DocumentType.SCANNED
        elif pdf_metrics['num_chars'] >= 20 and pdf_metrics['num_images'] > 0:
            return DocumentType.MIXED
        else:
            return DocumentType.TEXT
    
    def _handle_text_pdfs(self, file_path: str) -> str:
# 1) Try splitting into pages
        try:
            content = self._export_text_with_page_breaks(file_path)
            total_chars = sum(len(p) for p in content.split("<!-- Page"))
            if total_chars > 20:
                return content
            logging.warning("PyPDF2 saw almost no text, falling back to PdfReaderService.")
        except Exception as e:
            logging.warning(f"PyPDF2 split failed: {e}")

        # 2) Fallback: PdfReaderService (might return 'No readable text' - we fall back to VLM)
        try:
            raw = self.pdf_reader.read_pdf_text_as_markdown(file_path)
            if "No readable text" in raw:
                return self.vlm.extract_scanned_report_as_markdown(file_path)
            return raw
        except Exception as e:
            logging.error(f"PdfReaderService failed: {e}")
            return self.vlm.extract_scanned_report_as_markdown(file_path)

    def handle_pdfs(self, file_path: str) -> str:
        """Handles PDF files."""
        # Attempt to read the text from the PDF. If the first pass has no text, use the VLM to read it.
        # pdf_res = self.pdf_reader.read_pdf_text_as_markdown(file_path)
        # Use the VLM service to extract text from scanned PDFs
        pdf_metrics = self.pdf_reader.get_pdf_metrics(file_path)

        match self._document_type(pdf_metrics):
            case DocumentType.SCANNED:
                logging.warning(f"Extracting scanned PDF content using VLM: {file_path}")
                return self.vlm.extract_scanned_report_as_markdown(file_path)
            case DocumentType.MIXED:
                logging.warning(f"Extracting mixed PDF content using PyPDF2: {file_path}")
                return self.pdf_reader.read_pdf_mixed_as_markdown(file_path)
            case DocumentType.TEXT:
                logging.warning(f"Extracting text PDF content using PyPDF2: {file_path}")
                return self._handle_text_pdfs(file_path)
        
    def _export_text_with_page_breaks(self, file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            chunks = []
            for i, page in enumerate(reader.pages):
            # page.extract_text() returns the raw Unicode text on that page
                text = page.extract_text() or ""
                chunks.append(f"<!-- Page {i+1} -->\n{text.strip()}")

            return "\n\n".join(chunks)

        except Exception as e:
            import traceback
            logging.error("Error adding page breaks:\n%s", traceback.format_exc())
            return f"Error adding page breaks: {str(e)}"

    def _flatten_tables(self, markdown: str) -> str:
        logging.debug("Flattening tables in markdown content...")
        def table_to_list(match):
            table = match.group(0)
            lines = table.strip().split('\n')
            headers = [h.strip() for h in lines[0].strip('|').split('|')]
            rows = [line.strip('|').split('|') for line in lines[2:]]

            flattened = ""
            for row in rows:
                items = [f"{k}: {v.strip()}" for k, v in zip(headers, row)]
                flattened += "- " + ", ".join(items) + "\n"
            return flattened.strip()

        pattern = r'\|.*\|\n\|[-\s|]+\|\n(?:\|.*\|\n?)+'
        return re.sub(pattern, table_to_list, markdown)    

    async def extract_markdown(self, file_path: str) -> MarkdownReport:
        """Extracts content from a file as markdown."""
        # If the file is a scanned report, use VLM service to extract text
        match file_path:
            case file_path if file_path.endswith('.pdf'):
                content = self.handle_pdfs(file_path)
            case file_path if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                content = self.excel_reader.read_excel_as_markdown(file_path)
            case _:
                raise ValueError("Unsupported file type. Only PDF and Excel files are supported.")

        # Page breaks and flatten tables
        if not content or len(content.strip()) < 10:
            raise ValueError("Empty or invalid content extracted from file.")
        
        final_markdown = self._flatten_tables(content)
        logging.info("Extracted Markdown Report:\n%s", final_markdown)
        return MarkdownReport(final_markdown)
