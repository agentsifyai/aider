from dataclasses import dataclass
from typing import List

from app.features.defect_report_analysis.strategy.bullet_report.prompts import Prompts
from app.infra.llm.service import LLMService

@dataclass
class Chunk:
    chunk_content: str
    page_number: int


class LocationSectionChunker:
    """
    A class that chunks the text into sections based on the location section.
    """

    prompts = Prompts()
    llm = LLMService()

    async def get_chunks(self, text: str) -> List[Chunk]:
        """Split the text into chunks of 30 lines with an overlap of 10 lines."""
        lines = text.splitlines()  # Split the text into individual lines
        chunk_size = 24
        overlap = 8

        chunks = []
        for i in range(0, len(lines), chunk_size - overlap):
            chunk = lines[i:i + chunk_size]
            chunks.append("\n".join(chunk))  # Combine lines back into a single string

        return [Chunk(chunk_content=chunk, page_number=i // chunk_size + 1) for i, chunk in enumerate(chunks)]
