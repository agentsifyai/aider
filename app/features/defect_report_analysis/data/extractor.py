from app.domain.models import MarkdownReport
from app.infra.vlm.service import VlmService
from app.infra.pdf.service import PdfReaderService
from app.infra.xls.service import ExcelReaderService
from docling.document_converter import DocumentConverter
import re
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
        # TODO: Find out a faster way to get a count of images and actual text.
        return True  # Placeholder for actual implementation

    def handle_pdfs(self, file_path) -> str:
        """Handles PDF files."""
        # Attempt to read the text from the PDF. If the first pass has no text, use the VLM to read it.
        # pdf_res = self.pdf_reader.read_pdf_text_as_markdown(file_path)
        # Use the VLM service to extract text from scanned PDFs

        try:
            content = self._add_page_breaks(file_path)
            has_substantial_text = any(len(getattr(p, "text", "").strip()) > 30
                                   for p in DocumentConverter().convert(file_path).document.pages)
            if has_substantial_text:
                return content
            else:
                logging.warning("Docling returned mostly empty content, falling back to PdfReaderService.")

        except Exception as e:
            logging.warning(f"Docling failed, trying fallback: {str(e)}")        
        # If the PDF is scanned, use the VLM service to extract text

        try:
            raw = self.pdf_reader.read_pdf_text_as_markdown(file_path)
            if 'No readable text' in raw:
                return self.vlm.extract_scanned_report_as_markdown(file_path)
            return raw
        except Exception as e:
            logging.error(f"PDF fallback failed: {str(e)}")
            return self.vlm.extract_scanned_report_as_markdown(file_path)
        
    def _add_page_breaks(self, file_path: str) -> str:
        try:
            converter = DocumentConverter()
            result = converter.convert(file_path)

            chunks = []
            for i, page in enumerate(result.document.pages):
                text = getattr(page, "text", "")
                logging.info(f"Page {i+1} content:\n{text}")
                chunks.append(f"<!-- Page {i + 1} -->\n{text.strip()}")

            return "\n\n".join(chunks)

        except Exception as e:
            import traceback
            logging.error("Error adding page breaks:\n%s", traceback.format_exc())
            return f"Error adding page breaks: {str(e)}"

    def _flatten_tables(self, markdown: str) -> str:
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
                content = self.excel_reader.read_excel_text_as_markdown(file_path)
            case _:
                raise ValueError("Unsupported file type. Only PDF and Excel files are supported.")

        # Page breaks and flatten tables
        if not content or len(content.strip()) < 10:
            raise ValueError("Empty or invalid content extracted from file.")
        
        final_markdown = self._flatten_tables(content)
        logging.info("Extracted Markdown Report:\n%s", final_markdown)
        return MarkdownReport(final_markdown)
