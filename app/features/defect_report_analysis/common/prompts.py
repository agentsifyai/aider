
class Prompts:
    
    def delimit(tag: str, text: str) -> str:
        """Delimit text with a given tag."""
        return f"<{tag}>{text}</{tag}>"
    
    def delimit_document(text: str) -> str:
        """Delimit text with a document tag."""
        return Prompts.delimit('document', text)