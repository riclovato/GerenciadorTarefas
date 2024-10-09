
import argparse
from datetime import datetime
from models import Priority
from task_operations import create_task, get_task, update_task, delete_task, list_tasks, search_tasks, list_tasks_by_category, get_tasks_with_upcoming_reminders

def main():
    parser = argparse.ArgumentParser(description="Gerenciador de Tarefas CLI")
    parser.add_argument('action', choices=['add', 'list', 'update', 'delete', 'search', 'list_category', 'reminders'], help="Ação a ser executada")
    parser.add_argument('--id', help="ID da tarefa (para update e delete)")
    parser.add_argument('--title', help="Título da tarefa")
    parser.add_argument('--description', help="Descrição da tarefa")
    parser.add_argument('--due-date', help="Data de vencimento (formato: YYYY-MM-DD)")
    parser.add_argument('--priority', choices=['LOW', 'MEDIUM', 'HIGH'], help="Prioridade da tarefa")
    parser.add_argument('--completed', action='store_true', help="Marcar como completada")
    parser.add_argument('--categories', nargs='+', help="Categorias da tarefa")
    parser.add_argument('--reminder', help="Data e hora do lembrete (formato: YYYY-MM-DD HH:MM)")
    parser.add_argument('--keyword', help="Palavra-chave para pesquisa")
    parser.add_argument('--category', help="Nome da categoria para listar tarefas")

    args = parser.parse_args()

    if args.action == 'add':
        if not all([args.title, args.due_date, args.priority]):
            print("Erro: título, data de vencimento e prioridade são obrigatórios para adicionar uma tarefa.")
            return
        due_date = datetime.strptime(args.due_date, "%Y-%m-%d")
        priority = Priority[args.priority]
        reminder = datetime.strptime(args.reminder, "%Y-%m-%d %H:%M") if args.reminder else None
        task_data = create_task(args.title, args.description, due_date, priority, args.categories, reminder)
        if task_data:
            print("Tarefa criada com sucesso:")
            for key, value in task_data.items():
                print(f"{key.capitalize()}: {value}")
        else:
            print("Falha ao criar a tarefa.")

    elif args.action == 'search':
        if not args.keyword:
            print("Erro: palavra-chave é obrigatória para pesquisa.")
            return
        tasks = search_tasks(args.keyword)
        if tasks:
            print(f"Tarefas encontradas com a palavra-chave '{args.keyword}':")
            for task in tasks:
                print(f"ID: {task.id}, Título: {task.title}, Descrição: {task.description}")
        else:
            print(f"Nenhuma tarefa encontrada com a palavra-chave '{args.keyword}'.")

    elif args.action == 'list_category':
        if not args.category:
            print("Erro: nome da categoria é obrigatório para listar tarefas por categoria.")
            return
        tasks = list_tasks_by_category(args.category)
        if tasks:
            print(f"Tarefas na categoria '{args.category}':")
            for task in tasks:
                print(f"ID: {task.id}, Título: {task.title}, Vencimento: {task.due_date}")
        else:
            print(f"Nenhuma tarefa encontrada na categoria '{args.category}'.")

    elif args.action == 'reminders':
        tasks = get_tasks_with_upcoming_reminders()
        if tasks:
            print("Tarefas com lembretes próximos:")
            for task in tasks:
                print(f"ID: {task.id}, Título: {task.title}, Lembrete: {task.reminder}")
        else:
            print("Nenhuma tarefa com lembrete próximo.")


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