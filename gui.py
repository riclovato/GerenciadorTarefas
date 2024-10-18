import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models import Priority
from task_operations import create_task, list_tasks, update_task, delete_task, search_tasks, list_categories

class TaskManagerGUI:
    def __init__(self,master):
        self.master = master
        self.master.title("Gerenciador de Tarefas")
        self.master.geometry("800x600")

        self.create_widgets()


    def create_widgets(self):
        #Frame principal
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        #Lista de tarefas
        self.task_tree = ttk.Treeview(main_frame, columns=("ID", "Título", "Vencimento", "Prioridade", "Concluída"))
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Título", text="Título")
        self.task_tree.heading("Vencimento", text="Vencimento")
        self.task_tree.heading("Prioridade", text="Prioridade")
        self.task_tree.heading("Concluída", text="Concluída")
        self.task_tree.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

        #Scrollbar lista tarefas
        scrollbar = tk.Scrollbar(main_frame,orient=tk.VERTICAL, command=self.task_tree.yview)
        scrollbar.grid(row=0, column=4, sticky=(tk.N, tk.S))
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        #Formulário adicionar/editar tarefas
        form_frame = ttk.LabelFrame(main_frame, text="Adicionar/Editar Tarefa", padding="10")
        form_frame.grid(row=1, column=0, columnspan=5, sticky=(tk.W, tk.E))

        ttk.Label(form_frame, text="Título:").grid(row=0, column=0, sticky=tk.W)
        self.title_entry = ttk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="Descrição:").grid(row=1, column=0, sticky=tk.W)
        self.description_entry = ttk.Entry(form_frame, width=40)
        self.description_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="Data de Vencimento:").grid(row=2, column=0, sticky=tk.W)
        self.due_date_entry = ttk.Entry(form_frame, width=20)
        self.due_date_entry.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="Prioridade:").grid(row=3, column=0, sticky=tk.W)
        self.priority_combobox = ttk.Combobox(form_frame, values=["LOW", "MEDIUM", "HIGH"])
        self.priority_combobox.grid(row=3, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="Categorias:").grid(row=4, column=0, sticky=tk.W)
        self.categories_entry = ttk.Entry(form_frame, width=40)
        self.categories_entry.grid(row=4, column=1, sticky=tk.W)

        #Botões
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.grid(row=2, column=0, columnspan=5, sticky=(tk.W, tk.E))

        ttk.Button(button_frame, text="Adicionar Tarefa", command=self.add_task).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Atualizar Tarefa", command=self.update_task).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Excluir Tarefa", command=self.delete_task).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Pesquisar", command=self.search_tasks).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text ="Atualizar Lista", command=self.refresh_task_list).grid(row=0, column=4, padx=5)


        #inicializar lista de tarefas
        self.refresh_task_list()



    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        due_date = datetime.strptime(self.due_date_entry.get(), "%Y-%m-%d")
        priority = Priority[self.priority_combobox.get()]
        categories = [cat.strip() for cat in self.categories_entry.get().split(',') if cat.strip()]

        task = create_task(title, description, due_date, priority, categories)
        if task:
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
            self.refresh_task_list()
        else:
            messagebox.showerror("Erro", "Falha ao adicionar tarefa.")


    def update_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para atualizar.")
            return

        task_id = self.task_tree.item(selected_item)['values'][0]
        title = self.title_entry.get()
        description = self.description_entry.get()
        due_date = datetime.strptime(self.due_date_entry.get(), "%Y-%m-%d")
        priority = Priority[self.priority_combobox.get()]
        categories = [cat.strip() for cat in self.categories_entry.get().split(',') if cat.strip()]

        if update_task(task_id, title=title, description=description, due_date=due_date, priority=priority, categories=categories):
            messagebox.showinfo("Sucesso", "Tarefa atualizada com sucesso!")
        else:
            messagebox.showerror("Erro","Falha ao atualizar tarefa.")


    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para excluir.")
            return

        task_id = self.task_tree.item(selected_item)['values'][0]
        if delete_task(task_id):
            messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso")
            self.refresh_task_list()
        else:
            messagebox.showerror("Erro", "Falha ao excluir tarefa.")

    def search_tasks(self):
        keyword = self.title_entry.get()
        tasks = search_tasks(keyword)
        self.update_task_list(tasks)


    def refresh_task_list(self):
        tasks =list_tasks()
        self.update_task_list(tasks)


    def update_task_list(self, tasks):
        self.task_tree.delete(*self.task_tree.get_children())
        for task in tasks:
            self.task_tree.insert("", "end", values=(task.id, task.title, task.due_date.strftime("%Y-%m-%d"), task.priority.name, "Sim" if task.completed else "Não"))


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()