# main.py
import os, uuid, tempfile, shutil
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from crewai import Crew, Process
from task import analyze_financial_document_task, verification_task

app = FastAPI(title="Financial Document Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

def build_crew(file_path: str, query: str) -> Crew:
    # copy Tasks and inject inputs into their descriptions
    t1 = analyze_financial_document_task.copy()
    t1.description = t1.description.format(file_path=file_path, query=query)

    t2 = verification_task.copy()
    t2.description = t2.description.format(file_path=file_path, query=query)

    return Crew(
        agents=[t1.agent, t2.agent],
        tasks=[t1, t2],
        process=Process.sequential,
        verbose=True,
    )

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Summarize key metrics, guidance and top risks")
):
    tmp_dir = tempfile.mkdtemp(prefix="fin_doc_")
    local_path = os.path.join(tmp_dir, file.filename)

    try:
        with open(local_path, "wb") as f:
            f.write(await file.read())

        crew = build_crew(local_path, query.strip())
        result = crew.kickoff(inputs={"file_path": local_path, "query": query.strip()})
        return JSONResponse({"filename": file.filename, "result": str(result)})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {e}")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
