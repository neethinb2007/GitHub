from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task Manager API")


class Task(BaseModel):
    title: str
    completed: bool = False


tasks = {}
next_id = 1


@app.get("/")
def HOME():
    return {"message": "Welcome to Task Manager API"}


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    global next_id

    task_data = {
        "id": next_id,
        "title": task.title,
        "completed": task.completed
    }

    tasks[next_id] = task_data
    next_id += 1

    return task_data


@app.get("/tasks")
def get_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return tasks[task_id]


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    tasks[task_id] = {
        "id": task_id,
        "title": task.title,
        "completed": task.completed
    }

    return tasks[task_id]


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    del tasks[task_id]

    return {"message": "Task deleted successfully"}