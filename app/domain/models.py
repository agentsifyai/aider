import uuid

class MarkdownReport:
    content: str

    def __init__(self, content: str) -> None:
        self.content = content

    def __str__(self):
        return self.content


class MinimalDefect:
    """Minimal Defect model for API response."""

    id: str  # Automatically assigned UUID
    name: str # name of the damage e.g. "crack in lantern"
    location: str # location of the damage e.g. "front left corner in room no. 15"

    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        # Assign other attributes if provided
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f"MinimalDefect(id={self.id}, name={self.name}, location={self.location})"


class PotentialDefect(MinimalDefect):
    """Potential Defect model for API response."""

    evidence: str # Evidence of the defect in the report e.g. citation
    evidence_page: int # Page number where the defect evidence is mentioned
    confidence: float # 0.0 - 1.0
    confidence_reason: str # Reason for the confidence level e.g. "The defect is clearly visible in the document."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"PotentialDefect(name={self.name}, location={self.location}, evidence={self.evidence}, confidence={self.confidence}, confidence_reason={self.confidence_reason})\n"


class DetailedPotentialDefect(PotentialDefect):
    """Detailed Potential Defect model for API response."""

    verbose_description: str # Verbose description of the defect e.g. "The crack in the lantern is 5 cm long and 2 cm wide."
    defect_cause: str # Cause of the defect e.g. "The crack was caused by a heavy object falling on the lantern."
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)