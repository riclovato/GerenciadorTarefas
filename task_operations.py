from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from models import Task, Session, Priority, Category
from datetime import datetime, timedelta

def create_task(title: str, description: str, due_date: datetime, priority: Priority, categories: list = None, reminder: datetime = None) -> dict:
    session = Session()
    try:
        new_task = Task(title=title, description=description, due_date=due_date, priority=priority, reminder=reminder)
        if categories:
            for category_name in categories:
                category = session.query(Category).filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name)
                    session.add(category)
                new_task.categories.append(category)
        session.add(new_task)
        session.commit()
        return {
            'id': new_task.id,
            'title': new_task.title,
            'description': new_task.description,
            'due_date': new_task.due_date,
            'priority': new_task.priority.name,
            'completed': new_task.completed,
            'reminder': new_task.reminder,
            'categories': [cat.name for cat in new_task.categories]
        }
    except Exception as e:
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
            if key == 'categories':
                task.categories.clear()
                for category_name in value:
                    category = session.query(Category).filter_by(name=category_name).first()
                    if not category:
                        category = Category(name=category_name)
                        session.add(category)
                    task.categories.append(category)
            else:
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

def search_tasks(keyword: str) -> list:
    session = Session()
    try:
        return session.query(Task).filter(
            or_(
                Task.title.ilike(f"%{keyword}%"),
                Task.description.ilike(f"%{keyword}%")
            )
        ).all()
    finally:
        session.close()

def list_tasks_by_category(category_name: str) -> list:
    session = Session()
    try:
        category = session.query(Category).filter_by(name=category_name).first()
        if category:
            return category.tasks
        return []
    finally:
        session.close()

def get_tasks_with_upcoming_reminders() -> list:
    session = Session()
    try:
        now = datetime.now()
        return session.query(Task).filter(
            Task.reminder.isnot(None),
            Task.reminder > now,
            Task.reminder <= now + timedelta(days=1)  # Ajuste conforme necessário
        ).all()
    finally:
        session.close()

def list_categories():
    session = Session()
    try:
        return session.query(Category).all()
    finally:
        session.close()