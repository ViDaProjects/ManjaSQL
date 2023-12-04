from table import Table
from typing import List
import csv
import pandas as pd
import mysql.connector
from mysql.connector import Error
import re
import os
import json

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
        self.db_default_path = ""


    def create_table(self, name: str):
        id = "table_" + str(self.current_table_id) + "_db_" + str(self.db_id)
        self.new_table_name = name
        new_table = Table(id, self.new_table_name)
        table_path = os.path.join(self.db_default_path, self.new_table_name) 
        print("table path")
        print(self.db_default_path)
        new_table.table_default_path = self.db_default_path
        self.current_table_id += 1
        self.tables_list.append(new_table)
        self.save_create_table_on_json(new_table)
        return new_table

    def save_create_table_on_json(self, table: Table):
        table_dict = {}
        current_path = os.getcwd()
        if self.db_default_path == "":
            self.db_default_path = current_path
        #db_path = os.path.join(current_path, self.db_name) 
        #print("ESSE DB_PATH "+ db_path)
        json_path = os.path.join(table.table_default_path, table.table_name + ".json")
        #os.chdir(db_path)
        print("path da table json "+ json_path)
        print(f'Diretório atual saving table on json: {os.getcwd()}')

        table_dict['TABLE_ID'] = table.table_id
        table_dict['TABLE_NAME'] = table.table_name
        table_dict['COLUMNS'] = {}
        table_dict['DATA'] = {}
        table_dict['KEY_DATA'] = {}
        table_dict['PRIMARY_KEY'] = []
        table_dict['FOREIGN_KEY'] = []
        table_dict['UNIQUE_KEY'] = []

        with open(json_path, 'w') as json_file:
            json.dump(table_dict, json_file)

  
    def load_saved_tables(self, tables_files: List, path_database: str):
        table_data = []
        field = {}
        #FAZER APENAS SE FOR JSON
        print(f'Diretório atual saved tables: {os.getcwd()}')
        self.db_default_path = str(os.getcwd())
        for table_json in tables_files:
            if table_json.endswith(".json"):
                with open(table_json, 'r') as json_file:
                    table_data = json.load(json_file)
                table_name = table_data['TABLE_NAME']
                table = self.create_table(table_name)
                print()
                for field_name in table_data['COLUMNS']:
                    field = table_data['COLUMNS'][field_name]
                    new_field = table.create_field(field['FIELD_NAME'], field['TYPE'], field['CONSTRAINTS'], self.db_name)
                    for key in table_data['KEY_DATA']:
                        if new_field.field_name == key['FIELD_NAME']:
                            table.define_key_type(new_field, key) 

                #ARRUMAR DATA DEPOIS DE GERAR O JSON
                
                #Não sei como arrumar isso, penser dps
                print()
                print("-------------- DATAAAAA------------")
                print()
                print(table_data['DATA'])
                for data in table_data['DATA']:
                    print(data)
                    indexes = list(field.field_name for field in table.fields_list)
                    table.insert_data(indexes, data, True, self.db_name)

    
    def import_database(self, table_name: str, csv_path: str):
        current_table = self.create_table(table_name)

        #Read csv file
        print(csv_path)
        dataframe = pd.read_csv(csv_path)

        fields = []
        #get name and data type from columns
        columns = list(dataframe.columns)
        fields = [current_table.create_field(name, str(dataframe[name].dtype), self.db_name, "") for name in columns]

        #create current table fields
        current_table.import_fields_from_csv(fields)

        print(dataframe.to_dict('records'))
        #Populate current table
        for data in dataframe.to_dict('records'):
            print(data)
            current_table.insert_data(columns, data, True, self.db_name)

 
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
        
    def inner_join(table_a: Table, table_b: Table, on_column: str):
        inner_join_table = []

        for row_a in table_a.data_dict_list:
            for row_b in table_b.data_dict_list:
                if row_a[on_column] == row_b[on_column]:
                    inner_join_table.append({**row_a, **row_b})  # Merge os dicionários

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

    def create_table_fields_from_connection(self, table: Table):
        self.cursor.execute(f"DESCRIBE "+ table.table_name)
        #get name and data type from field
        fields = [table.create_field(field[0], field[1], field[2], self.db_name) for field in self.cursor.fetchall()]

    def create_table_instances_from_connection(self):
        table_names = self.get_table_names_from_connection()

        for table_name in table_names:
            table = self.create_table(str(table_name))
            self.create_table_fields_from_connection(table)
            self.populate_table_data(table)

    def get_data_from_connected_database(self):
        message = self.connect_to_database()
        if message == "Conectado com sucesso!":
            self.create_table_instances_from_connection()

        return message

    def populate_table_data(self, table: Table):
        self.cursor.execute(f"SELECT * FROM " + table.table_name)
        all_table_data = self.cursor.fetchall() 
        for data in all_table_data:
            indexes = list(field.field_name for field in  table.fields_list)
            table.insert_data(indexes, data, False, self.db_name)

    def select(self, query: str):
        table_name = self.find_next_word(query, "FROM")
        for i, table in enumerate(self.tables_list):
            if table.table_name == table_name:
                self.tables_list[i].select_data(query)
                break


    def update(self, query: str):
        pass

    def delete(self, query: str):
       
        # Sets the split query to be readable
        split_query = query.split()
        
        pattern = r'(\s*=\s*)'
        result = []
        for text in split_query:
            split_text = re.split(pattern, text)
            result.extend(filter(None, split_text))
        split_query = result
        
        # Table name to be checked later
        table_name = split_query[split_query.index("FROM") + 1]
        
        # Extracts what are the fields and the values that will be attributed to them
        where_index = len(split_query)
        if "WHERE" in split_query:
            where_index = split_query.index("WHERE")
        set_index = split_query.index("SET")

        #nao preciso
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
                if where_index + 4 >= len(split_query):
                    condition = ' '.join(split_query[where_index + 1:where_index + 4])
                conditions.append(condition)
        
        # Delete table
        for table in self.tables_list:
            if table.table_name == table_name:
                for field in table.fields_list:
                    for k in range(len(field_name)):
                        if field.field_name == field_name[k]:
                            if condition is met:
                                field.value == new_values[k]      

    def insert(self, query: str):
        pass

    def save_data():
        pass

    def login(self, user: str, password: str):
        return (self.user == user and self.password == password)
       
    def translator(self, query: str):
        new_query = query.upper()
        
        new_query = new_query.replace("ou", "or")
        new_query = new_query.replace("transformar", "set")
        new_query = new_query.replace("juntar interno", "inner join")
        new_query = new_query.replace("inserir", "insert into")
        new_query = new_query.replace("e", "and")
        new_query = new_query.replace("organizar por", "order by")
        new_query = new_query.replace("donde", "where")
        new_query = new_query.replace("inserir", "insert into")
        new_query = new_query.replace("modificar", "update")
        new_query = new_query.replace("apagar", "delete from")
        new_query = new_query.replace("agarrar", "select") 
        new_query = new_query.replace("valores", "values")        

        return new_query


