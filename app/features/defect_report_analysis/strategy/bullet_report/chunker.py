from typing import List
import json
from app.features.defect_report_analysis.strategy.bullet_report.prompts import Prompts
from app.infra.llm.service import LLMService

class LocationSectionChunker:
    """
    A class that chunks the text into sections based on the location section.
    """

    prompts = Prompts()
    llm = LLMService()


    async def get_chunks(self, text: str) -> List[str]:
        """Get chunks of text from the report."""
        # This method should be implemented to return the chunks of text from the report.
        result: str = await self.llm.ask_async([
                {"role": "system", "content": self.prompts.ASSISSTANT_SYSTEM_PROMPT },
                {"role": "user", "content": self.prompts.CHUNKING_INSTRUCTIONS + Prompts.delimit_document(text)},
        ])

        chunks: List[str] = json.loads(result)
        return chunks
