from enum import Enum
from database import Database
import uuid
from datetime import datetime

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task:
    def __init__(self, title, description, due_date, priority, completed=False, id=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
        self.id = id or self._generate_uuid()

    def create(self):
        # Verificar se os campos necessáro estão preenchidos
        if not self.title or not self.due_date or not self.priority:
            raise ValueError("Todos os campos devem ser preenchidos")

        try:
            db = Database()
            db.connect()
            query = """
                       INSERT INTO tasks (id, title, description, due_date, priority, completed)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """
            params = (str(self.id), self.title, self.description, self.due_date.isoformat(),
                      self.priority.value, int(self.completed))
            db.executeQuery(query, params)
            db.disconnect()
            return True
        except Exception as e:
            print(f"Erro ao criar tarefa:    {e}")
            return False


    def update(self):
        # Implemente o método update

    def delete(self):
        # Implemente o método delete

    def mark_as_completed(self):
        # Implemente o método mark_as_completed
    @staticmethod
    def _generate_uuid():
        return uuid.uuid4()


    def __str__(self):
        # Implemente a representação em string da tarefa