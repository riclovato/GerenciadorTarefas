import argparse
from datetime import datetime
from models import Priority
from task_operations import create_task, get_task, update_task, delete_task, list_tasks

def main():
    parser = argparse.ArgumentParser(description="Gerenciador de Tarefas CLI")
    parser.add_argument('action', choices=['add', 'list', 'update', 'delete'], help="Ação a ser executada")
    parser.add_argument('--id', help="ID da tarefa (para update e delete)")
    parser.add_argument('--title', help="Título da tarefa")
    parser.add_argument('--description', help="Descrição da tarefa")
    parser.add_argument('--due-date', help="Data de vencimento (formato: YYYY-MM-DD)")
    parser.add_argument('--priority', choices=['LOW', 'MEDIUM', 'HIGH'], help="Prioridade da tarefa")
    parser.add_argument('--completed', action='store_true', help="Marcar como completada")

    args = parser.parse_args()

    if args.action == 'add':
        if not all([args.title, args.due_date, args.priority]):
            print("Erro: título, data de vencimento e prioridade são obrigatórios para adicionar uma tarefa.")
            return
        due_date = datetime.strptime(args.due_date, "%Y-%m-%d")
        priority = Priority[args.priority]
        task_data = create_task(args.title, args.description, due_date, priority)
        if task_data:
            print(f"Tarefa criada com ID: {task_data['id']}")
        else:
            print("Falha ao criar a tarefa.")

    elif args.action == 'list':
        tasks = list_tasks()
        for task in tasks:
            print(f"ID: {task.id}, Título: {task.title}, Vencimento: {task.due_date}, Prioridade: {task.priority.name}, Completada: {task.completed}")

    elif args.action == 'update':
        if not args.id:
            print("Erro: ID da tarefa é obrigatório para atualização.")
            return
        update_dict = {}
        if args.title:
            update_dict['title'] = args.title
        if args.description:
            update_dict['description'] = args.description
        if args.due_date:
            update_dict['due_date'] = datetime.strptime(args.due_date, "%Y-%m-%d")
        if args.priority:
            update_dict['priority'] = Priority[args.priority]
        update_dict['completed'] = args.completed
        if update_task(args.id, **update_dict):
            print("Tarefa atualizada com sucesso.")
        else:
            print("Falha ao atualizar a tarefa.")

    elif args.action == 'delete':
        if not args.id:
            print("Erro: ID da tarefa é obrigatório para exclusão.")
            return
        if delete_task(args.id):
            print("Tarefa excluída com sucesso.")
        else:
            print("Falha ao excluir a tarefa.")

if __name__ == "__main__":
    main()