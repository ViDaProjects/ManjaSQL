from table import Table
from typing import List
import csv
import pandas as pd

#atributo privado: __nome__
class DataBase:

    def __init__(self, id: int, name: str, host: str, user: str, password: str) -> None:
        self.fields_list = [] #talvez class fields
        self.tables_list: List[Table] = [] #class Table
        self.tables_name_list = [] #str
        self.new_table_name = ""
        self.db_id = id
        self.db_name = name
        self.user = user
        self.password = password
        self.host = host
        self.current_table_id = 0

    def create_table(self, query: str):
        #Cria um json com esse nome
        id = "table_" + str(self.current_table_id) + "_db_" + str(self.db_id)
        self.new_table_name = self.find_next_word(query, "TABLE")
        print("new table name - db - " + self.new_table_name)
        new_table = Table(id, self.new_table_name)
        self.tables_name_list.append(self.new_table_name)
        self.tables_list.append(new_table)
        #passa por todos os fields
        #new_table.create_field()
        return new_table

    def drop_table():
        pass

    def import_database(self, table_name: str, csv_path: str):
        query_csv = "CREATE TABLE " + table_name 
        current_table = self.create_table(query_csv)

        #LOGICA PARA IMPORTAR CSV PARA TABELA ESPECIFICA
        # Leitura do arquivo CSV usando pandas
        print(csv_path)
        dataframe = pd.read_csv(csv_path)

        # Obtendo os nomes e tipos de dados das colunas
        columns = dataframe.columns
        fields = [current_table.create_field(name, str(dataframe[name].dtype)) for name in columns]

        # Criando a instância da classe Table
        current_table.import_fields_from_csv(fields)

        # Criando a instância da classe 
        for data in dataframe.to_dict('records'):
            current_table.insert_data(data)
            print(data)
            print()
        #dados = Data(table=tabela, data=dataframe.to_dict('records'))

        print()
        #for i in enumerate(current_table.data):
        #    print(current_table.data[i])
        #    print()
        #return dados_tabela

        print("apenas printando cada data")
        for data in current_table.data:
            print(data.fields_data['livro_id'])
            print(data.fields_data['titulo'])
            print()
    
    #Só funciona com uma palavra
    def execute_query(self, query: str):
        #passa por toda a query
        command = query.upper().split()

        if command == "CREATE TABLE":
            #Se create table: cria tabela
            self.create_table(query)

        if command == "INSERT INTO":
            #Se insert into:
            self.insert(query)

        if command == "UPDATE":
            #se update
            self.update(query)

        if command == "DELETE":
            #se delete
            self.delete(query)

        if command == "SELECT":
           #se select
            self.select(query)
        

    def create_table_by_json():
        pass

    def connect_to_database():
        pass

    def read_query(query: str):
        pass

    def select(self, query: str):
        table_name = self.find_next_word(query, "FROM")
        for i, table in enumerate(self.tables_list):
            if table.table_name == table_name:
                self.tables_list[i].select_data(query)
                break


    def update(self, query: str):
        pass

    def delete(self, query: str):
        pass

    def insert(self, query: str):
        pass

    def save_data():
        pass

    def login(self, user: str, password: str):
        return (self.user == user and self.password == password)
       

    #TA FUNCIONANDO SO COM UMA PALAVRA
    def find_next_word(self, query:str, searched_word: str) -> str:  # Update the function signature to specify the return type
        query_words = query.split()
        print(query_words)
        for i, word in enumerate(query_words):
            if searched_word.upper() == word:
                next_word = query_words[i + 1] if i + 1 < len(query_words) else ""
                print(f"Encontrou '{searched_word}' na palavra '{word}'. Próxima palavra: {next_word}")
                return next_word
        return ""  # Ensure the function always returns a value of type "str"
    
# if __name__ == "__main__":
#     db = DataBase(1, "teste", "user", "password", "localhost")
#     db.create_table(1, "CREATE TABLE IF NOT EXISTS table_name (id INTEGER PRIMARY KEY, name TEXT)")
#     db.create_table(2, "CREATE TABLE IF NOT EXISTS table_name (id INTEGER PRIMARY KEY, name TEXT)")
#     db.create_table(3, "CREATE
