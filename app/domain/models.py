
class MarkdownReport:
    content: str

    def __init__(self, content: str) -> None:
        self.content = content


class MinimalDefect:
    """Minimal Defect model for API response."""

    name: str # name of the damage e.g. "crack in lantern"
    location: str # location of the damage e.g. "front left corner in room no. 15"


class PotentialDefect(MinimalDefect):
    """Potential Defect model for API response."""

    evidence: str # Evidence of the defect in the report e.g. citation
    confidence: float # 0.0 - 1.0


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