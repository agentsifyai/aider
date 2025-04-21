from typing import List
from app.domain.models import PotentialDefect, DetailedPotentialDefect, MarkdownReport

class DefectDetailingStrategy:

    async def detail_defect(self, defect: PotentialDefect) -> DetailedPotentialDefect:
        raise NotImplementedError("This method should be overridden by subclasses")


class DefectIdentificationStrategy:

    def strategy_name(self):
        print(type(self).__name__)
    
    def __str__(self):
        return self.strategy_name()

    def selection_criteria() -> str:
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def detailing_strategy(self) -> DefectDetailingStrategy:
        raise NotImplementedError("This method should be overridden by subclasses")

    async def identify_defects(self, report: MarkdownReport) -> List[PotentialDefect]:
        raise NotImplementedError("This method should be overridden by subclasses")
    