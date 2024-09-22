# Modelo de Dados - Gerenciador de Tarefas

## Tabela: tasks

| Coluna      | Tipo         | Restrições                |
|-------------|--------------|---------------------------|
| id          | INTEGER      | PRIMARY KEY AUTOINCREMENT |
| title       | TEXT         | NOT NULL                  |
| description | TEXT         |                           |
| due_date    | DATE         |                           |
| priority    | TEXT         | CHECK(priority IN ('LOW', 'MEDIUM', 'HIGH')) |
| completed   | BOOLEAN      | DEFAULT 0                 |
| created_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| updated_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

## Índices

- Criar um índice na coluna `due_date` para otimizar consultas de filtragem por data.
- Criar um índice na coluna `priority` para otimizar consultas de filtragem por prioridade.

## Notas

1. A coluna `id` é a chave primária e será incrementada automaticamente.
2. `title` é obrigatório, mas `description` pode ser nulo.
3. `due_date` permite tarefas sem uma data de vencimento definida.
4. `priority` é restrito aos valores 'LOW', 'MEDIUM', 'HIGH'.
5. `completed` é um booleano, com valor padrão falso (0).
6. `created_at` e `updated_at` são timestamps para rastrear a criação e última atualização da tarefa.

## Script SQL para Criação da Tabela

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    priority TEXT CHECK(priority IN ('LOW', 'MEDIUM', 'HIGH')),
    completed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_due_date ON tasks(due_date);
CREATE INDEX idx_priority ON tasks(priority);
```
