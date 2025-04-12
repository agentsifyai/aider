from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import OutputFormat
from docling.document_converter import ExcelFormatOption

class ExcelReaderService:
    def __init__(self):
        pass

    def read_pdf_text_as_markdown(self, file_path: str) -> str:
        """
        Read text from an XLS file and convert it to markdown.
        """
        try:
            converter = DocumentConverter(
                format_options={
                    # Configure Excel-specific options if needed
                    "excel": ExcelFormatOption(
                        # Set any Excel-specific options here
                        sheet_names=None,  # Process all sheets (default)
                        # sheet_names=["Sheet1", "Sheet2"]  # Or specify sheets to process
                    )
                }
            )
            converter_result = converter.convert(file_path)
            text = converter_result.document.export_to_markdown()
            if not text.strip():
                return "No readable text found in the XLS. The document might be scanned or contain only images."

            return text
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            return f"Error reading PDF: {str(e)}"