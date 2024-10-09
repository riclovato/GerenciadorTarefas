from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Enum, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import uuid

engine = create_engine('sqlite:///tasks.db', echo=True)
Base = declarative_base()

class Priority(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# Nova tabela para categorias
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

# Tabela de associação entre Task e Category
task_categories = Table('task_categories', Base.metadata,
    Column('task_id', String, ForeignKey('tasks.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime, nullable=False)
    priority = Column(Enum(Priority), nullable=False)
    completed = Column(Boolean, default=False)
    reminder = Column(DateTime)  # Nova coluna para lembretes
    categories = relationship('Category', secondary=task_categories, backref='tasks')

    def __init__(self, title, description, due_date, priority, completed=False, reminder=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
        self.reminder = reminder

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', due_date={self.due_date}, priority={self.priority}, completed={self.completed}, reminder={self.reminder})>"

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)