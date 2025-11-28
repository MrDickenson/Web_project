from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    task_list_id: int  # Зв'язок з TaskList
    title: str
    is_completed: bool
    description: Optional[str] = None
    due_date: Optional[str] = None