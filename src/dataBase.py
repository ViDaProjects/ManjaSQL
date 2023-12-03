from table import Table
from typing import List
import csv
import pandas as pd
import mysql.connector
from mysql.connector import Error
import re


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
        self.connection = None
        self.cursor = None

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
        upper_query = query.upper()
        command = upper_query.split()

        if command[0] == "CREATE TABLE":
            #Se create table: cria tabela
            self.create_table(upper_query)

        if command[0] == "INSERT INTO":
            #Se insert into:
            self.insert(upper_query)

        if command[0] == "UPDATE":
            #se update
            self.update(upper_query)

        if command[0] == "DELETE":
            #se delete
            self.delete(upper_query)

        if command[0] == "SELECT":
           #se select
            self.select(upper_query)
        
    def execute_query_on_connection(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_query_columns(self):
        return (['livro_id','titulo'])
    
    def create_table_by_json():
        pass

    def connect_to_database(self):
        print("TENTAR CONEXÃOOO")
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.db_name,
                raise_on_warnings=True
            )
            self.cursor = self.connection.cursor()
            return ("Conectado com sucesso!")

        except mysql.connector.Error as e:
            # Se ocorrer um erro, imprima a mensagem de erro
            return ("Erro de MySQL: " + str(e))
        except Exception as e:
            # Se ocorrer outro tipo de erro, imprima a mensagem de erro
            return ("Erro: " + str(e))    

    def get_table_names_from_connection(self):
        self.cursor.execute("SHOW TABLES")
        table_names = [table[0].decode('utf-8') for table in self.cursor.fetchall()]
        print("table_names - get table")
        print(table_names)
        #self.cursor.fetchall()  # Consumir os resultados antes de continuar
        return table_names

    def get_table_fields_from_connection(self, table: Table):
        self.cursor.execute(f"DESCRIBE "+ table.table_name)
        #get name and data type from field
        fields = [table.create_field(field[0], field[1]) for field in self.cursor.fetchall()]
        #self.cursor.fetchall()  # Consumir os resultados antes de continuar

    def create_table_instances_from_connection(self):
        table_names = self.get_table_names_from_connection()

        for table_name in table_names:
            print(str(table_name))
            print()
            table = self.create_table("CREATE TABLE "+ str(table_name))
            self.get_table_fields_from_connection(table)


    def get_data_from_connected_database(self):
        print("ENTROU NO DATABASEEEEE")
        message = self.connect_to_database()
        if message == "Conectado com sucesso!":
            self.create_table_instances_from_connection()
        return message
        #chamar função para colocar os dados
        #criar tabelas
        #class table and field
        #popular as tabelas
        #class data

    def read_query(query: str):
        pass

    def select(self, query: str):
        table_name = self.find_next_word(query, "FROM")
        for i, table in enumerate(self.tables_list):
            if table.table_name == table_name:
                self.tables_list[i].select_data(query)
                break

    def condition_check(self, comparison: list, main_comparator: str, table: Table):
        field_name = []
        value = []
        for i in len(comparison):
            field_name.append(comparison.split('=')[0].strip())
            value.append(comparison.split('=')[1].strip())
        
        for field in table.fields_list:
            if field == field:
                pass

    def update(self, query: str):
        
        # Sets the split query to be readable
        split_query = query.split()
        
        pattern = r'(\s*=\s*)'
        result = []
        for text in split_query:
            split_text = re.split(pattern, text)
            result.extend(filter(None, split_text))
        split_query = result
        
        # Table name to be checked later
        table_name = split_query[split_query.index("UPDATE") + 1]
        
        # Extracts what are the fields and the values that will be attributed to them
        where_index = len(split_query)
        if "WHERE" in split_query:
            where_index = split_query.index("WHERE")
        set_index = split_query.index("SET")

        field_name = []
        new_values = []
        i = 1
        while where_index - i > set_index:
            field_name.append(split_query[where_index - i - 2])
            new_values.append(split_query[where_index - i])
            i += 3

        conditions = []
        
        if where_index != len(split_query):
            i = 1
            while where_index + i < len(split_query):

                if where_index + i <= len(split_query):
                    condition = ''.join(split_query[where_index + i:where_index + i + 3])
                    
                    conditions.append(condition)
                i += 4
        
        condition_joiner = ""
        if len(conditions) >= 2:
            condition_joiner = split_query[where_index + 4]
        
        
        # Update the tables
        for table in self.tables_list:
            print(i.table_name)
            if table.table_name == table_name:
                for field in table.fields_list:
                    for k in range(len(field_name)):
                        if field.field_name == field_name[k]:
                            if self.condition_check(conditions, condition_joiner, table):
                                field.value = new_values[k]

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
    
if __name__ == "__main__":
    db = DataBase(1, "teste", "user", "password", "localhost")
    db.execute_query("update customers set ContactName = 'Alfred', city= 'Frankfurt' where customerID = 1 and bila = bilo")
