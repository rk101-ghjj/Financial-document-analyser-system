from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document as analyze_financial_task
from db import init_db, get_session, AnalysisResult
from worker import analyze_task
from service import run_crew

app = FastAPI(title="Financial Document Analyzer")
init_db()

# run_crew is imported from service

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query == "" or query is None:
            query = "Analyze this financial document for investment insights"
            
        # Process the financial document with all analysts
        response = run_crew(query=query.strip(), file_path=file_path)

        session = get_session()
        try:
            record = AnalysisResult(
                task_id=None,
                file_name=file.filename,
                query=query.strip(),
                result_text=str(response),
                status="completed",
            )
            session.add(record)
            session.commit()
        finally:
            session.close()

        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

@app.post("/analyze/async")
async def analyze_async(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        if not query:
            query = "Analyze this financial document for investment insights"
        task = analyze_task.delay(file_path=file_path, query=query.strip(), file_name=file.filename)
        return {"task_id": task.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Queueing failed: {str(e)}")

@app.get("/results/{task_id}")
async def get_result(task_id: str):
    session = get_session()
    try:
        record = session.query(AnalysisResult).filter(AnalysisResult.task_id == task_id).first()
        if not record:
            return JSONResponse(status_code=404, content={"detail": "Result not found"})
        return {
            "task_id": record.task_id,
            "status": record.status,
            "file_name": record.file_name,
            "query": record.query,
            "result": record.result_text,
            "created_at": record.created_at.isoformat() + "Z",
        }
    finally:
        session.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)