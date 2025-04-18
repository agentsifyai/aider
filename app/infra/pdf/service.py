from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.pipeline_options import PictureDescriptionBaseOptions
from docling.document_converter import DocumentConverter, PdfFormatOption, InputFormat
from docling.backend.docling_parse_v2_backend import DoclingParseV2DocumentBackend

import base64

class PdfReaderService:

    page_break_number = 0

    def get_page_break_value(self) -> str:
        self.page_break_number += 1
        return f'--- Page {self.page_break_number} ---'

    def read_pdf_text_as_markdown(self, file_path):
        """
        Read text from a PDF file and convert it to markdown.
        """
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
            text = converter_result.document.export_to_markdown(page_break_placeholder=self.get_page_break_value())
            if not text.strip():
                return "No readable text found in the PDF. The document might be scanned or contain only images."

            return text
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            return f"Error reading PDF: {str(e)}"

    @staticmethod
    def pdf_to_base64(file_path: str):
        """
        Convert a PDF file to base64 string.
        :param file_path: Path to the PDF file.
        :return: Base64 encoded string of the PDF file.
        """
        with open(file_path, "rb") as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
        return base64_pdf
