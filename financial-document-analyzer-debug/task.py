# task.py
from crewai import Task
from agents import financial_analyst, verifier
from tools import read_pdf_tool

analyze_financial_document_task = Task(
    description=(
        "User query: '{query}'. The PDF path is '{file_path}'. "
        "Use read_pdf_tool(file_path) to gather relevant content. "
        "Produce JSON with keys: "
        "executive_summary[], key_metrics[], guidance[], risks[], evidence[]. "
        "Each evidence item is {quote (<=25 words), page}. "
        "Only use facts present in the PDF; otherwise say 'Not specified in document.'"
    ),
    agent=financial_analyst,
    tools=[read_pdf_tool],
    expected_output=(
        "JSON with arrays executive_summary, key_metrics, guidance, risks, "
        "and evidence[{quote, page}]"
    ),
    async_execution=False,
)

verification_task = Task(
    description=(
        "Verify the previous analysis strictly against '{file_path}'. "
        "Use read_pdf_tool(file_path) as needed. "
        "Return JSON: {valid: bool, issues:[], corrections:[]}."
    ),
    agent=verifier,
    tools=[read_pdf_tool],
    expected_output="JSON with fields valid, issues[], corrections[].",
    async_execution=False,
)
