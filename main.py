from fastapi import FastAPI, BackgroundTasks
from celery.result import AsyncResult
from pydantic import BaseModel
from tasks import process_data_task
import uvicorn

app = FastAPI(title="FastAPI Celery Integration")


class DataInput(BaseModel):
    text: str


@app.get("/")
async def root():
    return {"message": "FastAPI with Celery Integration"}


@app.post("/process")
async def process_data(data: DataInput, background_tasks: BackgroundTasks):
    """
    Process data asynchronously using Celery
    """
    # Submit task to Celery
    task = process_data_task.delay(data.text)
    return {"task_id": task.id, "message": "Task submitted successfully"}


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """
    Get the status of a submitted task
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "status": task_result.status,
    }

    if task_result.status == "SUCCESS":
        result["result"] = task_result.get()

    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
