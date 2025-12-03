from src.domain.models import Task
from src.service.db import get_db_connection


class TodoService:
    def get_all_tasks(self):
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM tasks').fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def create_task(self, title, priority='normal'):
        new_task = Task(title=title, priority=priority)

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO tasks (id, title, priority, is_completed, created_at) VALUES (?, ?, ?, ?, ?)',
            (new_task.id, new_task.title, new_task.priority, new_task.is_completed, new_task.created_at)
        )
        conn.commit()
        conn.close()

        return new_task.to_dict()

    def delete_task(self, task_id):
        conn = get_db_connection()
        cursor = conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()

        return deleted_count > 0


todo_service = TodoService()