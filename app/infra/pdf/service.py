from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption, InputFormat
from docling.backend.docling_parse_v2_backend import DoclingParseV2DocumentBackend

class PdfAnalyzerService:
    def __init__(self):
        pass

    def read_pdf(self, file_path):
        """Read a PDF file and extract its text content."""
        try:
            # TODO: Consider a separate class for the chosen converter library
            # These options are meant to increase speed.
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = False
            pipeline_options.do_table_structure = False

            doc_converter = DocumentConverter(
                format_options={
                    InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options,
                                                     backend=DoclingParseV2DocumentBackend)
                }
            )
            converter_result = doc_converter.convert(file_path)
            text = converter_result.document.export_to_text()
            if not text.strip():
                return "No readable text found in the PDF. The document might be scanned or contain only images."

            return text
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            return f"Error reading PDF: {str(e)}"
