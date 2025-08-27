import os
from celery import Celery
from service import run_crew
from db import get_session, AnalysisResult, init_db

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("financial_analyzer", broker=redis_url, backend=redis_url)

init_db()

@celery_app.task(bind=True)
def analyze_task(self, file_path: str, query: str, file_name: str):
    session = get_session()
    try:
        result_text = str(run_crew(query=query, file_path=file_path))
        record = AnalysisResult(
            task_id=self.request.id,
            file_name=file_name,
            query=query,
            result_text=result_text,
            status="completed",
        )
        session.add(record)
        session.commit()
        return {"task_id": self.request.id, "status": "completed"}
    except Exception as e:
        record = AnalysisResult(
            task_id=self.request.id,
            file_name=file_name,
            query=query,
            result_text=str(e),
            status="failed",
        )
        session.add(record)
        session.commit()
        raise
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass
        session.close()

