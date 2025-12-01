from fastapi import APIRouter, HTTPException, Query, Response, status
from datetime import datetime
from schemas import TaskBase, TaskCreate, TaskUpdate, TaskResponse
from database import tasks_db

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    responses={404: {"description": "Stats not found"}},
)

@router.get("/stats")
async def get_tasks_stats() -> dict:
    tasks_by_quadrant = [0]*4
    tasks_completed = 0
    tasks_uncompleted = 0
    for task in tasks_db:
        if task["quadrant"] == "Q1":
            tasks_by_quadrant[0] += 1
        if task["quadrant"] == "Q2":
            tasks_by_quadrant[1] += 1
        if task["quadrant"] == "Q3":
            tasks_by_quadrant[2] += 1
        if task["quadrant"] == "Q4":
            tasks_by_quadrant[3] += 1

        if task["completed"]:
            tasks_completed+=1
        else:
            tasks_uncompleted+=1
    return {
        "total_tasks": len(tasks_db),
        "by_quadrant": {
            "Q1": tasks_by_quadrant[0],
            "Q2": tasks_by_quadrant[1],
            "Q3": tasks_by_quadrant[2],
            "Q4": tasks_by_quadrant[3]
        },
        "by_status": {
            "completed": tasks_completed,
            "pending": tasks_uncompleted
        }
    }