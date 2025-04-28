from typing import List
from dataclasses import dataclass
import re

@dataclass
class CommonChunk:
    chunk_content: str
    page_number: int


class PageChunker:
    """
    A class that chunks the text into sections based on the location section.
    """

    async def get_chunks(self, text: str) -> List[CommonChunk]:
        """Split the text into pages based on page markers."""
        # Split text into pages using regex (case-insensitive)
        pages = re.split(r'<!--\s*page\s*\d+\s*-->', text, flags=re.IGNORECASE)
        
        chunks = []
        page_number = 1

        # Skip first element if empty (in case text starts with page marker)
        if pages[0].strip() == '':
            pages = pages[1:]

        for page_content in pages:
            page_content = page_content.strip()
            if page_content:  # Only add non-empty pages
                chunks.append(CommonChunk(
                    chunk_content=page_content,
                    page_number=page_number
                ))
            page_number += 1

        return chunks