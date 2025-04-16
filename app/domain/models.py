
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


class DetailedPotentialDefect(PotentialDefect):
    """Detailed Potential Defect model for API response."""

    description: str # Verbose description of the defect e.g. "The crack in the lantern is 5 cm long and 2 cm wide."
