classDiagram
    class Task {
        -int id
        -string title
        -string description
        -Date dueDate
        -Priority priority
        -bool completed
        +create()
        +update()
        +delete()
        +markAsCompleted()
    }

    class TaskManager {
        -List~Task~ tasks
        +addTask(Task)
        +getTasks()
        +updateTask(Task)
        +deleteTask(int)
        +filterTasks(filter)
    }

    class Database {
        +connect()
        +disconnect()
        +executeQuery(string)
        +fetchResults()
    }

    class GUI {
        +showTaskList()
        +showTaskForm()
        +showFilterOptions()
    }

    TaskManager "1" -- "*" Task : manages
    TaskManager -- Database : uses
    GUI -- TaskManager : interacts with

    enum Priority {
        LOW
        MEDIUM
        HIGH
    }

    Task -- Priority : has