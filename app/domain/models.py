
class MarkdownReport:
    content: str

    def __init__(self, content: str) -> None:
        self.content = content

    def __str__(self):
        return self.content


class MinimalDefect:
    """Minimal Defect model for API response."""

    name: str # name of the damage e.g. "crack in lantern"
    location: str # location of the damage e.g. "front left corner in room no. 15"


class PotentialDefect(MinimalDefect):
    """Potential Defect model for API response."""

    evidence: str # Evidence of the defect in the report e.g. citation
    confidence: float # 0.0 - 1.0
    confidence_reason: str # Reason for the confidence level e.g. "The defect is clearly visible in the document."

    def __str__(self):
        return f"PotentialDefect(name={self.name}, location={self.location}, evidence={self.evidence}, confidence={self.confidence}, confidence_reason={self.confidence_reason})\n"


class DetailedPotentialDefect(PotentialDefect):
    """Detailed Potential Defect model for API response."""

    description: str # Verbose description of the defect e.g. "The crack in the lantern is 5 cm long and 2 cm wide."
