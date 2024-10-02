import sqlite3
from typing import List, Tuple, Any

class Database:
    def __init__(self,db_name: str ="task.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Conectado ao banco de dados: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao bando de dados: {e}")


    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Desconectado do bando de dados")


    def executeQuery(self,query: str, params: Tuple[Any, ...] = None) -> None:
        if not self.connection:
            raise ConnectionError("Não há conexão com o banco de dados. Chame connect() primeiro.")


        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Erro ao executar a query: {e}")
            self.connection.rollback()

    def fetchResults(self) -> List[Tuple[Any, ...]]:
        if not self.cursor:
            raise ConnectionError("Não há cursor disponível. Execute uma query primeiro.")

        return self.cursor.fetchall()


    def initialize_database(self):
        self.connect()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            priority INTEGER NOT NULL,
            completed INTEGER NOT NULL
        )
        """
        self.executeQuery(create_table_query)
        self.disconect()

if __name__ == "__main__":
    db = Database()
    db.initialize_database()
    print("Banco de dados inicializado com sucesso.")



