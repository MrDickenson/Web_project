import uuid
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Task:
    title: str
    priority: str = 'normal'
    id: str = field(default_factory=lambda: f"t-{str(uuid.uuid4())[:8]}")
    is_completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "is_completed": self.is_completed,
            "created_at": self.created_at
        }