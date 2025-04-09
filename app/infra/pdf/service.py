from PyPDF2 import PdfReader

class PdfAnalyzerService:

    def __init__(self):
        pass

    def read_pdf(self, file_path):
        """Read a PDF file and extract its text content."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:  # Only add if text was successfully extracted
                    text += page_text + "\n"
            
            if not text.strip():
                return "No readable text found in the PDF. The document might be scanned or contain only images."
                
            return text
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            return f"Error reading PDF: {str(e)}"