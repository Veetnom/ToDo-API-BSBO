from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from datetime import datetime

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)

tasks_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Сдать проект по FastAPI",
        "description": "Завершить разработку API и написать документацию",
        "is_important": True,
        "is_urgent": True,
        "quadrant": "Q1",
        "completed": False,
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "title": "Изучить SQLAlchemy",
        "description": "Прочитать документацию и попробовать примеры",
        "is_important": True,
        "is_urgent": False,
        "quadrant": "Q2",
        "completed": False,
        "created_at": datetime.now()
    },
    {
        "id": 3,
        "title": "Сходить на лекцию",
        "description": None,
        "is_important": False,
        "is_urgent": True,
        "quadrant": "Q3",
        "completed": False,
        "created_at": datetime.now()
    },
    {
        "id": 4,
        "title": "Посмотреть сериал",
        "description": "Новый сезон любимого сериала",
        "is_important": False,
        "is_urgent": False,
        "quadrant": "Q4",
        "completed": True,
        "created_at": datetime.now()
    },
]

@router.get("/")
async def get_all_tasks() -> dict:
    return {
        "count": len(tasks_db), 
        "tasks": tasks_db 
        }

@router.get("/quadrant/{quadrant}")
async def get_tasks_by_quadrant(quadrant: str) -> dict:
    if quadrant not in ["Q1", "Q2", "Q3", "Q4"]:
        raise HTTPException( 
            status_code=400,
            detail="Неверный квадрант. Используйте: Q1, Q2, Q3, Q4" 
        )
    filtered_tasks = [
        task 
        for task in tasks_db 
        if task["quadrant"] == quadrant 
    ]
    return {
        "quadrant": quadrant,
        "count": len(filtered_tasks),
        "tasks": filtered_tasks
    }

@router.get("/task/{task_id}")
async def get_tasks_by_id(task_id: int) -> dict:
    if not any(task["id"] == task_id for task in tasks_db):
        raise HTTPException( 
            status_code=404,
            detail="Несуществующий ID задачи" 
        )
    filtered_tasks = [
        task 
        for task in tasks_db 
        if task["id"] == task_id 
    ]
    return {
        "tasks": filtered_tasks
    }

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

@router.get("/status/{status}")
async def get_tasks_stats(status: str) -> dict:
    if status == "completed":
        status_completed = True
    elif status == "pending":
        status_completed = False
    else:
        raise HTTPException( 
            status_code=404,
            detail="Несуществующий статус" 
        )
    filtered_tasks = [
        task 
        for task in tasks_db 
        if task["completed"] == status_completed
    ]
    return {
        "status": status,
        "count": len(filtered_tasks),
        "tasks": filtered_tasks
    }

@router.get("/search")
async def search_tasks(q: str) -> dict:
    if len(q) < 2:
        raise HTTPException( 
            status_code=400,
            detail="Слово должно содержать не менее 2-х символов" 
        )
    filtered_tasks = []
    for task in tasks_db:
        if q in (task.get("title") or "") or q in (task.get("description") or ""):
            filtered_tasks.append(task)
    return {
        "query": q,
        "count": len(filtered_tasks),
        "tasks": filtered_tasks
    }