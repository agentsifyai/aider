from typing import List

from app.domain.models import MarkdownReport
from app.features.defect_report_analysis.strategy.base import DefectIdentificationStrategy
from app.infra.llm.service import LLMService

from app.features.defect_report_analysis.common.prompts import Prompts

import logging

ROUTER_SYSTEM_PROMPT = """
You will be provided a defect report document and a list of strategies for defect identification.
The defect report document will be provided in a markdown format and delimited by <document> tags.
The strategies criteria will be presented using a strategy name followed by its selection criteria.
Your task is to choose the most appropriate strategy based on the content of the report and the selection criteria.
"""


class StrategyRouter:
    """
    Strategy Router for defect report analysis.
    """

    registered_strategies: List[DefectIdentificationStrategy]
    llm: LLMService

    def __init__(self, strategies: List[DefectIdentificationStrategy]):
        self.registered_strategies = strategies
        self.llm = LLMService()

    def _strategies_criteria_prompt(self) -> str:
        """
        Returns the criteria string for all registered strategies.
        """
        return "\n\n".join([strategy.strategy_name() + "\n" + strategy.selection_criteria() 
                            for strategy in self.registered_strategies])

    def _user_prompt(self, report: MarkdownReport) -> str:
        return f"""
        Here are the strategies and their selection criteria:
        {self._strategies_criteria_prompt()}

        Here is the defect report:
        {Prompts.delimit_document(report.content)}

        Please select the appropriate strategy for defect identification based on the content of the report.
        Your answer should be the name of the strategy only.
        """

    async def choose_strategy(self, report: MarkdownReport) -> DefectIdentificationStrategy:
        """
        Chooses the appropriate strategy based on the report type.
        """
        logging.info("Choosing strategy in router...")
        response = await self.llm.ask_async([
            { "role": "system", "content": ROUTER_SYSTEM_PROMPT},
            { "role": "user", "content": self._user_prompt(report) },
            ])
        logging.debug("Router response: %s", response)

        for strategy in self.registered_strategies:
            if strategy.strategy_name() in response:
                logging.warning("Selected strategy: %s", strategy.strategy_name())
                return strategy
            
        raise ValueError(f"Strategy not found in response: {response}") # replace with a default strategy
