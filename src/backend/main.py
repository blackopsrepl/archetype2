from datetime import date
from pydantic import BaseModel, field_validator
from src.backend.factory.EssayComposerFactory import EssayComposerFactory
from src.backend.factory.TaskComposerFactory import TaskComposerFactory
from src.backend.factory.TaskEvaluatorFactory import TaskEvaluatorFactory
from fastapi import Depends, FastAPI
import uvicorn

app = FastAPI()


class SimpleTask(BaseModel):
    task_description: str
    llm: str


class DateRange(BaseModel):
    task_description: str
    start_date: str
    end_date: str

    @field_validator("end_date")
    @classmethod
    def check_dates(cls, v, values, **kwargs):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v


@app.get("/run/essay")
def run_essay(essay_composer_task: SimpleTask = Depends()):
    essay_composer = EssayComposerFactory().produce(essay_composer_task.llm)
    return essay_composer.run_chain(essay_composer_task.task_description)


@app.get("/run/task")
def run_task(task_composer_task: SimpleTask = Depends()):
    task_composer = TaskComposerFactory().produce(task_composer_task.llm)
    return task_composer.run_chain(task_composer_task.task_description)


@app.get("/run/evaluate")
def run_evaluate(task_evaluator_task: SimpleTask = Depends()):
    task_evaluator = TaskEvaluatorFactory().produce(task_evaluator_task.llm)
    return task_evaluator.run_chain(task_evaluator_task.task_description)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
