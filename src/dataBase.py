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
        self.tables_list: List[Table] = [] #class Table
        self.new_table_name = "" #create table
        self.current_table_id = 0 #create table
        #database data
        self.db_id = id
        self.db_name = name
        #database connection
        self.user = user
        self.password = password
        self.host = host
        self.connection = None
        self.cursor = None


    def create_table(self, query: str):
        id = "table_" + str(self.current_table_id) + "_db_" + str(self.db_id)
        self.new_table_name = self.find_next_word(query, "TABLE")
        new_table = Table(id, self.new_table_name)
        self.current_table_id += 1
        self.tables_list.append(new_table)

        return new_table

    def import_database(self, table_name: str, csv_path: str):
        query_csv = "CREATE TABLE " + table_name 
        current_table = self.create_table(query_csv)

        #Read csv file
        print(csv_path)
        dataframe = pd.read_csv(csv_path)

        #get name and data type from columns
        columns = dataframe.columns
        fields = [current_table.create_field(name, str(dataframe[name].dtype)) for name in columns]

        #create current table fields
        current_table.import_fields_from_csv(fields)

        #Populate current table
        for data in dataframe.to_dict('records'):
            current_table.insert_data(data)

 
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
        
    def inner_join(table_a: Table, table_b: Table, on_column: str):
        inner_join_table = []

        table_a.data[0].fields_data
        for row_a in table_a.data:
            for row_b in table_b.data:
                if row_a.fields_data[on_column] == row_b.fields_data[on_column]:
                    inner_join_table.append({**row_a.fields_data, **row_b.fields_data})  # Merge os dicionários

        return inner_join_table
    
    def execute_query_on_connection(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    #EXCLUSIVAMENTE PRA TESTE NA QUERY DE CONEXÃO, APAGAR DEPOIS
    def get_query_columns(self):
        return (['livro_id','titulo'])
    
    def create_table_by_json():
        pass

    def connect_to_database(self):
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
            return ("Erro de MySQL: " + str(e))
        except Exception as e:
            return ("Erro: " + str(e))    

    def get_table_names_from_connection(self):
        self.cursor.execute("SHOW TABLES")
        table_names = [table[0].decode('utf-8') for table in self.cursor.fetchall()]
        return table_names

    def get_table_fields_from_connection(self, table: Table):
        self.cursor.execute(f"DESCRIBE "+ table.table_name)
        #get name and data type from field
        fields = [table.create_field(field[0], field[1]) for field in self.cursor.fetchall()]

    def create_table_instances_from_connection(self):
        table_names = self.get_table_names_from_connection()

        for table_name in table_names:
            print(str(table_name))
            print()
            table = self.create_table("CREATE TABLE "+ str(table_name))
            self.get_table_fields_from_connection(table)
            self.populate_table_data(table)
            print()
            print("show table at create table instances")
            print(table.data_list)

    def get_data_from_connected_database(self):
        message = self.connect_to_database()
        if message == "Conectado com sucesso!":
            self.create_table_instances_from_connection()

        return message

    def populate_table_data(self, table: Table):
        self.cursor.execute(f"SELECT * FROM " + table.table_name)
        all_table_data = self.cursor.fetchall()
        print("dentro do populate")
        for data in all_table_data:
            print(data)
            print()
            table.insert_data(data)

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
