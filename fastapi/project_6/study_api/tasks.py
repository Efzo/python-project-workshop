from hmac import compare_digest
import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, StringConstraints

from .db import get_db


class TaskInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class Task(TaskInput):
    id: int
    done: bool


class Completion(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    done: bool


bearer = HTTPBearer(auto_error=False)


def verify_access(
    request: Request, credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]
):
    token = request.app.state.token
    if not token:
        raise HTTPException(status_code=503, detail="Access token is not configured")
    if credentials is None or not compare_digest(credentials.credentials.encode(), token.encode()):
        raise HTTPException(
            status_code=401, detail="Invalid bearer token", headers={"WWW-Authenticate": "Bearer"}
        )


router = APIRouter(prefix="/tasks", tags=["tasks"], dependencies=[Depends(verify_access)])
Database = Annotated[sqlite3.Connection, Depends(get_db)]


@router.post("", response_model=Task, status_code=201)
def add_task(task: TaskInput, db: Database):
    with db:
        result = db.execute("INSERT INTO tasks (title) VALUES (?)", (task.title,))
    return Task(id=result.lastrowid, title=task.title, done=False)


@router.get("", response_model=list[Task])
def list_tasks(
    db: Database,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0, le=1_000_000)] = 0,
):
    rows = db.execute("SELECT id, title, done FROM tasks ORDER BY id LIMIT ? OFFSET ?", (limit, offset))
    return [dict(row) for row in rows]


@router.patch("/{task_id}", response_model=Task)
def update_completion(task_id: int, completion: Completion, db: Database):
    if not 1 <= task_id <= 2**63 - 1:
        raise HTTPException(status_code=404, detail="Task not found")
    with db:
        rows = db.execute(
            "UPDATE tasks SET done = ? WHERE id = ? RETURNING id, title, done",
            (completion.done, task_id),
        ).fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="Task not found")
    return dict(rows[0])
