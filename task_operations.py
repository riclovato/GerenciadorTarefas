from sqlalchemy.exc import SQLAlchemyError
from models import Task, Session, Priority
from datetime import datetime

def create_task(title: str, description: str, due_date: datetime, priority: Priority) -> dict:
    session = Session()
    try:
        new_task = Task(title=title, description=description, due_date=due_date, priority=priority)
        session.add(new_task)
        session.commit()
        # Retorna um dicionário com os dados da tarefa
        return {
            'id': new_task.id,
            'title': new_task.title,
            'description': new_task.description,
            'due_date': new_task.due_date,
            'priority': new_task.priority,
            'completed': new_task.completed
        }
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao criar a tarefa: {e}")
        return None
    finally:
        session.close()
def get_task(task_id: str) -> Task:
    session = Session()
    try:
        return session.query(Task).filter(Task.id == task_id).first()
    finally:
        session.close()

def update_task(task_id: str, **kwargs) -> bool:
    session = Session()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            print(f"Tarefa com id {task_id} não encontrada")
            return False
        for key, value in kwargs.items():
            setattr(task, key, value)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao atualizar a tarefa: {e}")
        return False
    finally:
        session.close()

def delete_task(task_id: str) -> bool:
    session = Session()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            print(f"Tarefa com id {task_id} não encontrada")
            return False
        session.delete(task)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao deletar a tarefa: {e}")
        return False
    finally:
        session.close()

def list_tasks():
    session = Session()
    try:
        return session.query(Task).all()
    finally:
        session.close()