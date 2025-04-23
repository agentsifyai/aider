
class Prompts:
    """A class to manage common prompts for the LLM."""

    ASSISTANT_SYSTEM_PROMPT = """
        You are a professional assistant that searches through documents and finds relevant information for the user. 
        You will be asked to find an information in a document or to infer an information based from the document content.
        Document will be delimited using <document> and </document> tags.
        Your answer should contain only the information that is relevant to the question.
        If there is no information in the document that can be used to answer the question, you should say "I don't know".
        All the contents of your answer must be in polish language.
    """

    @staticmethod
    def delimit(tag: str, text: str) -> str:
        """Delimit text with a given tag."""
        return f"<{tag}>{text}</{tag}>"
    
    @staticmethod
    def delimit_document(text: str) -> str:
        """Delimit text with a document tag."""
        return Prompts.delimit('document', text)