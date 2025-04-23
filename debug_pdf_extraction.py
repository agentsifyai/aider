import sys


from app.infra.pdf.service import PdfReaderService
from docling.document_converter import DocumentConverter

def main(path):
    print(f"\n>>> Reading raw Markdown via PdfReaderService:\n")
    pdf_reader = PdfReaderService()
    raw_md = pdf_reader.read_pdf_text_as_markdown(path)
    print(raw_md[:1000] + ("\n…\n" if len(raw_md) > 1000 else "\n"))

    print(f"\n>>> Converting via DocumentConverter:\n")
    converter = DocumentConverter()
    doc = converter.convert(path).document
    print(f"Docling page count: {len(doc.pages)}\n")
    for i, page in enumerate(doc.pages, start=1):
        txt = getattr(page, "text", "") or ""
        snippet = txt.replace("\n", " ")[:200]
        print(f"--- page {i} ({len(txt)} chars) ---\n{snippet!r}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python debug_pdf_extraction.py /path/to/protocoleReport.pdf")
        sys.exit(1)
    main(sys.argv[1])
