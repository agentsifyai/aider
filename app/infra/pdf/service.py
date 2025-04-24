from docling.datamodel.pipeline_options import PdfPipelineOptions, PictureDescriptionApiOptions
from docling.document_converter import DocumentConverter, PdfFormatOption, InputFormat
from docling.backend.docling_parse_v2_backend import DoclingParseV2DocumentBackend
from docling_core.types.doc.document import PictureDescriptionData
from pydantic import AnyUrl
from typing import Dict

import base64
import logging
import os
import pymupdf

class PdfReaderService:

    page_break_number = 0

    def get_page_break_value(self) -> str:
        self.page_break_number += 1
        return f'--- Page {self.page_break_number} ---'

    def get_pdf_metrics(self, file_path: str) -> Dict[str, int]:
        # Gather counts of characters and images of a PDF.
        pdf_doc = pymupdf.open(file_path)
        pdf_metrics = {'filepath': file_path, 'num_chars': 0, 'num_images': 0}
        for page in pdf_doc.pages():
            pdf_metrics['num_chars'] += len(page.get_text())
            pdf_metrics['num_images'] += len(page.get_images())
        pdf_doc.close()

        return pdf_metrics

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
            logging.error(f"Error reading PDF: {str(e)}")
            return f"Error reading PDF: {str(e)}"

    def read_pdf_mixed_as_markdown(self, file_path) -> str:
        """
        Read text and images from a PDF file and convert it to markdown.
        """
        try:
            # TODO: Consider a separate class for the chosen converter library
            pipeline_options = PdfPipelineOptions()
            pipeline_options.enable_remote_services=True
            pipeline_options.do_ocr = False
            pipeline_options.do_table_structure = True
            pipeline_options.do_code_enrichment = False
            pipeline_options.do_formula_enrichment = False
            pipeline_options.do_picture_classification = True
            pipeline_options.do_picture_description = True
            pipeline_options.force_backend_text = False
            pipeline_options.table_structure_options.do_cell_matching = True
            pipeline_options.generate_page_images = True
            pipeline_options.generate_picture_images = True

            # TODO: Consider making this value ENUMs that we can more easily reference elsewhere.
            default_value = 'gpt-4.1'

            # Docling's api model only supports the completions endpoint, not the newer responses endpoint
            openai_url = 'https://api.openai.com/v1/chat/completions'

            prompt_val = 'Use the Polish language to describe the image. Be concise and accurate.'

            pic_desc_options = PictureDescriptionApiOptions(
                url=AnyUrl(openai_url),
                params=dict(
                    model=default_value,
                ),
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                },
                prompt=prompt_val,
                timeout=60,
            )

            pipeline_options.picture_description_options = pic_desc_options

            doc_converter = DocumentConverter(
                format_options={
                    InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options,
                                                     backend=DoclingParseV2DocumentBackend,
                                                     )
                }
            )

            converter_result = doc_converter.convert(file_path)

            # TODO: Review docling after they release more features that make this easier.
            pictures_in_file = converter_result.document.pictures
            picture_descs = {}
            for p in pictures_in_file:
                for a in p.annotations:
                    if type(a) == PictureDescriptionData:
                        picture_descs[p.self_ref] = a.text
                        break

            # This is currently the same as the default.
            image_placeholder = '<!-- image -->'

            md_text = converter_result.document.export_to_markdown(page_break_placeholder=self.get_page_break_value())

            # Do a replacement of each image placeholder with the descriptions of the pictures in order.
            for k in sorted(picture_descs.keys()):
                md_text = md_text.replace(image_placeholder, picture_descs[k], 1)

            return md_text
        except Exception as e:
            logging.error(f"Error reading PDF: {str(e)}")
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
