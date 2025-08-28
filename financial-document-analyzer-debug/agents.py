# agents.py
import os
from langchain_openai import ChatOpenAI
from crewai.agents import Agent
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
llm = ChatOpenAI(model=MODEL_NAME, temperature=0.2)

financial_analyst = Agent(
    role="Financial Analyst",
    goal=(
        "Extract factual insights from the uploaded financial PDF and the user query. "
        "When you state a fact, include a short quote (<=25 words) with page number in an Evidence section."
    ),
    backstory=(
        "You are a conservative equity analyst who relies on primary documents. "
        "No speculation; if the PDF doesn't contain it, say 'Not specified in document.'"
    ),
    llm=llm,
    tools=[],           # tools are attached on the Task side
    allow_delegation=False,
    verbose=True,
    memory=False,
)

verifier = Agent(
    role="Document Verifier",
    goal=(
        "Cross-check the analyst's claims strictly against the PDF text. "
        "Flag any statement that lacks evidence or mismatches numbers/wording."
    ),
    backstory="A meticulous fact-checker who trusts only the PDF.",
    llm=llm,
    tools=[],
    allow_delegation=False,
    verbose=True,
    memory=False,
)
