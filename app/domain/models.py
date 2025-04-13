

class MinimalDefect:
    """Minimal Defect model for API response."""

    name: str
    location: str


#TODO: Perhaps make Viewmodels.py file later?
class DefectList:
    """Model for the generated list of defects."""
    def __init__(self, filename: str, content: str, defect_list: str=None):
        self.filename = filename
        self.content = content
        self.defect_list = defect_list

    def get_filename(self) -> str:
        return self.filename

    def get_content(self) -> str:
        return self.content

    def get_defect_list(self) -> str:
        return self.defect_list

    def set_filename(self, filename: str) -> None:
        self.filename = filename

    def set_content(self, content: str) -> None:
        self.content = content

    def set_defect_list(self, defect_list) -> None:
        self.defect_list = defect_list