from dataclasses import dataclass

@dataclass
class TaskList:
    id: int
    title: str
    user_id: int  # Зв'язок з User