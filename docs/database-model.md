# Modelo de Dados - Gerenciador de Tarefas (SQLAlchemy)

## Tabela: tasks

| Coluna      | Tipo SQLAlchemy     | Tipo SQLite | Restrições                |
|-------------|---------------------|-------------|---------------------------|
| id          | String              | TEXT        | PRIMARY KEY               |
| title       | String              | TEXT        | NOT NULL                  |
| description | String              | TEXT        |                           |
| due_date    | DateTime            | DATETIME    | NOT NULL                  |
| priority    | Enum                | INTEGER     | NOT NULL                  |
| completed   | Boolean             | INTEGER     | DEFAULT False             |

## Notas

1. A coluna `id` é a chave primária e usa UUID como valor padrão.
2. `title` é obrigatório e não pode ser nulo.
3. `description` pode ser nulo.
4. `due_date` é obrigatório e armazena data e hora.
5. `priority` é um Enum com valores LOW (1), MEDIUM (2), HIGH (3).
6. `completed` é um booleano, com valor padrão falso.

## Implementação SQLAlchemy

```python
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Enum
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
```

## Notas sobre a Implementação

1. SQLAlchemy gerencia a criação de tabelas e índices automaticamente.
2. O tipo `Enum` do SQLAlchemy é mapeado para INTEGER no SQLite.
3. O tipo `Boolean` do SQLAlchemy é mapeado para INTEGER no SQLite (0 para False, 1 para True).
4. SQLAlchemy gerencia a conversão entre tipos Python e tipos SQLite.
5. A sessão do SQLAlchemy é usada para interagir com o banco de dados.

## Operações CRUD

As operações CRUD (Create, Read, Update, Delete) são implementadas em um arquivo separado `task_operations.py`. Aqui está um resumo das operações disponíveis:

1. `create_task(title, description, due_date, priority)`: Cria uma nova tarefa.
2. `get_task(task_id)`: Recupera uma tarefa específica pelo ID.
3. `update_task(task_id, **kwargs)`: Atualiza uma tarefa existente.
4. `delete_task(task_id)`: Exclui uma tarefa pelo ID.
5. `list_tasks()`: Lista todas as tarefas.

## Uso

Para usar este modelo de dados e as operações CRUD, importe as classes e funções necessárias:

```python
from models import Task, Priority, Session
from task_operations import create_task, get_task, update_task, delete_task, list_tasks
```

Exemplo de uso:

```python
from datetime import datetime

# Criar uma nova tarefa
new_task = create_task("Comprar leite", "Ir ao supermercado", datetime(2023, 6, 1), Priority.MEDIUM)

# Listar todas as tarefas
all_tasks = list_tasks()
for task in all_tasks:
    print(task)

# Atualizar uma tarefa
update_task(new_task.id, title="Comprar leite e pão", priority=Priority.HIGH)

# Deletar uma tarefa
delete_task(new_task.id)
```

Este modelo fornece uma estrutura robusta e flexível para o gerenciamento de tarefas, aproveitando os recursos do SQLAlchemy para uma interação eficiente com o banco de dados.