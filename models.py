from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
import uuid

# Criar engine e Base
engine = create_engine('sqlite:///tasks.db', echo=True)
Base = declarative_base()

# Definir Enum para Prioridade
class Priority(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# Definir modelo Task
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime, nullable=False)
    priority = Column(Enum(Priority), nullable=False)
    completed = Column(Boolean, default=False)

    def __init__(self, title, description, due_date, priority, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', due_date={self.due_date}, priority={self.priority}, completed={self.completed})>"

# Criar tabelas
Base.metadata.create_all(engine)

# Criar Session
Session = sessionmaker(bind=engine)