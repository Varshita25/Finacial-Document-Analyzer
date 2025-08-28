# tools.py
from typing import List
from pydantic import BaseModel, Field
from langchain.tools import tool
from pypdf import PdfReader

class PDFChunk(BaseModel):
    page: int = Field(..., description="1-indexed page number")
    text: str = Field(..., description="Raw text from that page")

@tool("read_pdf_tool", return_direct=False)
def read_pdf_tool(file_path: str) -> List[PDFChunk]:  # type: ignore[override]
    """
    Read a local PDF and return a list of {page, text}.
    Use short quotes (<=25 words) for evidence.
    """
    reader = PdfReader(file_path)
    out: List[PDFChunk] = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        out.append(PDFChunk(page=i + 1, text=text))
    return out
