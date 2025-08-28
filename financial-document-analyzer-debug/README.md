#  Financial Document Analyzer (CrewAI) — Debugged & Fixed

This is a FastAPI service built with CrewAI that analyzes financial PDF documents.  
Users can upload a PDF (for example, a quarterly financial report) and ask questions like:

- "Summarize the key financial metrics."
- "What are the top 3 risks mentioned in this document?"

The system extracts text from the PDF, generates a structured analysis, and then verifies the analysis against the original file.

---

## Bugs Found and Fixes

1. LLM initialization was broken (`llm = llm`).  
   Fixed by properly creating a ChatOpenAI model with `ChatOpenAI(model="gpt-4o-mini", temperature=0.2)`.

2. Agents used the wrong argument (`tool=[...]`).  
   Fixed by changing to `tools=[...]` and attaching tools at the Task level.

3. PDF reader tool used a non-existent `Pdf` class and was not registered.  
   Fixed by creating a clean `read_pdf_tool` using `pypdf` and LangChain's `@tool`.

4. Task and FastAPI endpoint both used the name `analyze_financial_document`.  
   Fixed by renaming the Task to `analyze_financial_document_task` and the endpoint to `analyze_endpoint`.

5. Crew inputs were incomplete.  
   Fixed by passing both `{file_path}` and `{query}` into the tasks.

6. Prompts encouraged hallucinations, fake URLs, and ignoring queries.  
   Fixed by rewriting prompts to be evidence-based, structured, and to include short quotes with page numbers.

7. Dependencies were mismatched (FastAPI 0.110 with Pydantic v1).  
   Fixed by upgrading to Pydantic v2 and cleaning requirements.txt.

---

## Project Structure
financial-document-analyzer-fixed/
│
├── agents.py # Defines the financial analyst and verifier agents
├── tools.py # Provides read_pdf_tool (pypdf-based)
├── task.py # Defines the analysis and verification tasks
├── main.py # FastAPI app with endpoints
├── requirements.txt # Cleaned dependency list
├── README.md # Documentation
├── .env.example # Example environment variables (no real keys)
│
└── data/
└── TSLA-Q2-2025-Update.pdf # Example PDF for testing



---

##  Setup Instructions

1. Clone the repo:
   ```bash
   git clone <your_repo_url>
   cd financial-document-analyzer-fixed

# Create a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies:

pip install --upgrade pip
pip install -r requirements.txt

# Add environment variables by creating a .env file:

OPENAI_API_KEY=sk-your-key-here
MODEL_NAME=gpt-4o-mini

# Run the server:

uvicorn main:app --reload --port 8000

# Usage
# Health Check
curl http://localhost:8000/


# Response:

{"message": "Financial Document Analyzer API is running"}

# Analyze a PDF
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@data/TSLA-Q2-2025-Update.pdf" \
  -F "query=Summarize key metrics, guidance and top 3 risks"

# API Documentation

GET /
Health check endpoint.

POST /analyze
# Inputs:

file: PDF document (required)

query: text query (required)

# Output:

JSON with analysis and supporting evidence.