from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.pipeline_options import PictureDescriptionBaseOptions
from docling.document_converter import DocumentConverter, PdfFormatOption, InputFormat
from docling.backend.docling_parse_v2_backend import DoclingParseV2DocumentBackend

import base64
import os

class PdfAnalyzerService:
    def __init__(self):
        pass

    def read_pdf_as_text(self, file_path):
        """
        Read a PDF file and extract its text content. This function 
        extracts the text from the PDF using the Docling library.
        It omits any images and non-text elements, focusing solely on the text content.
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
            text = converter_result.document.export_to_text()
            if not text.strip():
                return "No readable text found in the PDF. The document might be scanned or contain only images."

            return text
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            return f"Error reading PDF: {str(e)}"

    #TODO this does not work for scans
    #TODO: refine the purpose of this function and add more such as excel?
    def read_pdf_as_markdown_full(self, file_path):
        """
        Read pdf file and extract its text content as markdown. This function
        extracts the contents from the pdf using the Docling library.
        It includes all elements, including images and non-text elements.
        """
        try:
            # TODO: Consider a separate class for the chosen converter library
            # These options are meant to increase speed.
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = True
            pipeline_options.do_table_structure = True


            doc_converter = DocumentConverter(
                format_options={
                    InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options,
                                                     backend=DoclingParseV2DocumentBackend)
                }
            )
            converter_result = doc_converter.convert(file_path)
            text = converter_result.document.export_to_markdown()
            if not text.strip():
                return "No content found in the PDF. The document content might be empty or undreadable."

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
    

