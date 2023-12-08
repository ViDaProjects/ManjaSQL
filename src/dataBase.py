from table import Table
from typing import List
import csv
import pandas as pd
import mysql.connector
from mysql.connector import Error
import re
import os
import json
from field import Field

class DataBase:

    def __init__(self, id: int, name: str, host: str, user: str, password: str) -> None:
        self.tables_list: List[Table] = [] #class Table
        self.new_table_name = "" #create table
        self.current_table_id = 0 #create table
        self.db_default_path = "" #manage json
        self.field_names_from_select = []
        #database data
        self.db_id = id
        self.db_name = name
        #database connection
        self.user = user
        self.password = password
        self.host = host
        self.connection = None
        self.cursor = None

    def create_table(self, name: str):
        id = "table_" + str(self.current_table_id) + "_db_" + str(self.db_id)
        self.new_table_name = name
        new_table = Table(id, self.new_table_name)
        new_table.table_default_path = self.db_default_path
        self.current_table_id += 1
        self.tables_list.append(new_table)
        self.save_create_table_on_json(new_table)
        return new_table

    def save_create_table_on_json(self, table: Table):
        table_dict = {}
        current_path = os.getcwd()
        print(self.db_default_path)
        if self.db_default_path == "":
            self.db_default_path = current_path
        json_path = os.path.join(table.table_default_path, table.table_name + ".json")
        
        print("Caminho do banco de dados")
        print(json_path)

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
        self.db_default_path = str(os.getcwd())
        
        for table_json in tables_files:
            if table_json.endswith(".json"):
                #Read all table data saved on .json
                with open(table_json, 'r') as json_file:
                    table_data = json.load(json_file)
                
                #Initialize on classes 
                table_name = table_data['TABLE_NAME']
                table = self.create_table(table_name)
                
                for field_name in table_data['COLUMNS']:
                    field = table_data['COLUMNS'][field_name]
                    new_field = table.create_field(field['FIELD_NAME'], field['TYPE'], field['CONSTRAINTS'], self.db_name)
                    
                    for key in table_data['KEY_DATA']:
                        if new_field.field_name == key['FIELD_NAME']:
                            table.define_key_type(new_field, key) 

                for data in table_data['DATA']:
                    indexes = list(field.field_name for field in table.fields_list)
                    table.insert_data(indexes, data, True, self.db_name)

    
    def import_database(self, table_name: str, csv_path: str):
        current_table = self.create_table(table_name)

        #Read csv file
        dataframe = pd.read_csv(csv_path)

        fields = []
        #get name and data type from columns
        columns = list(dataframe.columns)

        #UPPER AQUIIII
        fields = [current_table.create_field(name.upper(), str(dataframe[name].dtype), self.db_name, "") for name in columns]

        #create current table fields
        current_table.import_fields_from_csv(fields)

        #Populate current table
        #for data in dataframe.to_dict('records'):
            #NOVO INSERT DATA 
        data = dataframe.to_dict('records')
        current_table.insert_data_from_existent_db(columns, data, True, self.db_name)

 
    #Só funciona com uma palavra
    def execute_query(self, query: str):
        #passa por toda a query
        upper_query = query.upper()
        command = upper_query.split()
        result = False
    #Viviane confia nessas modificações
        if command[0] == "CREATE":
            #Se create table: cria tabela
            self.create_table(upper_query)
            result = "Query executada com sucesso!"

        if command[0] == "INSERT":
            #Se insert into:
            self.insert(upper_query)
            result = "Query executada com sucesso!"

        if command[0] == "UPDATE":
            #se update
            self.update(upper_query)
            result = "Query executada com sucesso!"

        if command[0] == "DELETE":
            #se delete
            self.delete(upper_query)
            result = "Query executada com sucesso!"

        if command[0] == "SELECT":
           #se select
            result = self.select(upper_query)
        print(result)
        return result
        
    def inner_join(self, table_a: Table, table_b: Table, on_column: str):
        merged_data = {"data": []}

        for entry_1 in table_a["data"]:
            for entry_2 in table_b["data"]:
                if entry_1["id"] == entry_2["id"]:
                    merged_entry = {**entry_1, **entry_2}  # Merge dictionaries
                    merged_data["data"].append(merged_entry)
                    break  # Stop iterating over entries in data_2 if matched

        # Convert merged data to JSON
        merged_json = json.dumps(merged_data, indent=2)
        return merged_json#

    
    def execute_query_on_connection(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

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

        #UPPER AQUI
        fields = [table.create_field(field[0].upper(), field[1], field[2], self.db_name) for field in self.cursor.fetchall()]
        return fields

    def create_table_instances_from_connection(self):
        table_names = self.get_table_names_from_connection()

        for table_name in table_names:
            table = self.create_table(str(table_name))
            fields = self.create_table_fields_from_connection(table)
            self.populate_table_data(table)

    def get_data_from_connected_database(self):
        message = self.connect_to_database()
        if message == "Conectado com sucesso!":
            self.create_table_instances_from_connection()

        return message

    def populate_table_data(self, table: Table):
        self.cursor.execute(f"SELECT * FROM " + table.table_name)
        all_table_data = self.cursor.fetchall() 
        indexes = list(field.field_name for field in  table.fields_list)

        table.insert_data_from_existent_db(indexes, all_table_data, False, self.db_name)

    def select(self, query: str):
        split_query = self.query_splitter(query)
        
        key_words = ["SELECT", "DISTINCT", "FROM",  "WHERE", "GROUP", "BY", "HAVING", "ORDER", "BY", "INNER", "JOIN"]
        
        # Get field names
        field_names = []
        select_index = split_query.index(key_words[0])
        distance = 1
        if key_words[1] in split_query:
            distance = 2
        for i in range(select_index + distance, len(split_query)):
            if split_query[i] in key_words:
                break
            field_names.append(split_query[i])
        
        # Get table names
        table_names = []
        from_index = split_query.index(key_words[2])
        for i in range(from_index + 1, len(split_query)):
            if split_query[i] in key_words:
                break
            table_names.append(split_query[i])


        selected = []
        # if inner join was called than perform inner join
        if "INNER" in split_query:
            inner_index = split_query.index(key_words[9])
            for table in self.tables_list: # Só está extraindo de uma tabela
                if table_names[0] == table.table_name.upper():
                #print(table.data_dict_list)
                    table1 = table
                elif table_names[1] == table.table_name.upper():
                    table2 = table
            joint_table = self.inner_join(table1, table2, split_query[inner_index + 2])
            selected = [{field: entry[field] for field in field_names} for entry in table.data_dict_list]
            
        else:
            # Perform the select process
            for table in self.tables_list: # Só está extraindo de uma tabela
                if table_names[0] == table.table_name.upper():
                    #print(table.data_dict_list)
                    selected = [{field: entry[field] for field in field_names} for entry in table.data_dict_list]
                    
        # Deals with conditions declared by WHERE
        conditions = []
        if "WHERE" in split_query:
            where_index = split_query.index(key_words[3])
            for i in range(where_index + 1, len(split_query)):
                if split_query[i] in key_words:
                    break
                conditions.append(split_query[i])
        
        # Check for multiple table conditions and remove them from conditions

        condition_selected = []
        for table in self.tables_list:
            if table.table_name.upper() == table_names[0]:
                for i, data in enumerate(selected):
                    if conditions:
                        if self.condition_check(conditions, i, table):
                            condition_selected.append(selected[i])
                    else:
                        condition_selected.append(selected[i])
                selected = condition_selected
            
        # Dealing with distinct
        if "DISTINCT" in split_query:
            unique_data = [dict(t) for t in {tuple(sorted(entry.items())) for entry in condition_selected}]
            selected = unique_data

        self.field_names_from_select = field_names

        order_field = []
        if "ORDER" in split_query:
            order_index = split_query.index(key_words[7])    
            order_field.append(split_query[order_index + 2])
            reverse = False

            if "DESC" in split_query:
                reverse = True
            selected = sorted(selected, key=lambda x: x.get(order_field[0], ""), reverse = reverse)

        return selected
            

    def condition_check(self, comparison: List[str], index: int, table: Table):
        # Passar uma lista subquerry com o que eu preciso
        evaluation = []
        evaluation.append(table.perform_operation(str(table.data_dict_list[index].get(comparison[0])).upper(), comparison[1], comparison[2]))
        if len(comparison) <= 3:
            return evaluation[0]
        evaluation.append(table.perform_operation(str(table.data_dict_list[index].get(comparison[4])).upper(), comparison[5], comparison[6]))

        return table.perform_operation(evaluation[0], comparison[3], evaluation[1])

    def query_splitter(self, query: str) -> str:
        query = query.upper()
        # Sets the split query to be readable
        split_query = query.split()
        
        pattern = r'(\s*=\s*)'
        result = []
        for text in split_query:
            split_text = re.split(pattern, text)
            result.extend(filter(None, split_text))
        split_query = result

        result = []
        for word in split_query:
            word = word.replace (";", "")
            word = word.replace ('(', "")
            word = word.replace(")", "")
            result.append(word.replace(",", ""))
        split_query = result

        merged_strings = []
        
        merging = False
        for i in range(len(split_query)):

            if merging:
                merged_strings[-1] += " " + split_query[i]
            else:
                merged_strings.append(split_query[i])


            if split_query[i].startswith("'") and not split_query[i].endswith("'"):
                merging = True

            elif split_query[i].endswith("'") and not split_query[i].startswith("'"):
                merging = False

            elif split_query[i].endswith("'") and split_query[i].startswith("'"):
                merging = False

        split_query = []
        for words in merged_strings:
            split_query.append(words.strip("'"))
        return split_query
    
    def update(self, query: str):
        
        split_query = self.query_splitter(query)
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
            conditions = split_query[split_query.index("WHERE") + 1:]

        # Update the tables
        for table in self.tables_list:
            # If this is the correct table
            if table.table_name.upper() == table_name:
                for i, data in enumerate(table.data_dict_list):
                    # Read all fields checking if the condition is met
                    if self.condition_check(conditions, i, table):
                        # Update values
                        for x in range(len(field_name)):
                            #USAR INSERT DATA
                            data[field_name[x]] = new_values[x]

    def delete(self, query: str):
        split_query = self.query_splitter(query)
        table_name = split_query[split_query.index("FROM") + 1]

        # Extracts what are the fields and the values that will be attributed to them
        where_index = len(split_query)
        if "WHERE" in split_query:
            where_index = split_query.index("WHERE")

        conditions = []
        
        if where_index != len(split_query):
            conditions = split_query[split_query.index("WHERE") + 1:]
        print(conditions)

        for table in self.tables_list:
            # If this is the correct table
            if table.table_name.upper() == table_name:
                for i, data in enumerate(table.data_dict_list):
                    # Read all fields checking if the condition is met
                    if self.condition_check(conditions, i, table):
                        #print(table.data_dict_list)
                        
                        #REESCREVER O JSON DE ALGUM JEITO
                        del table.data_dict_list[i]
                        #print(table.data_dict_list)

                

    def insert(self, query: str):
        split_query = self.query_splitter(query) # Tirar os parenteses

        into_index = split_query.index("INTO")
        table_name = split_query[into_index + 1]

        values_index = len(split_query)
        if "VALUES" in split_query:
            values_index = split_query.index("VALUES")

        order = []

        if values_index > into_index + 2:
            order = split_query[into_index + 2 : values_index]
        
        values = split_query[values_index + 1 : ]
        
        insert = {}
        for table in self.tables_list:
            # If this is the correct table
            if table.table_name.upper() == table_name:
                if order:
                    
                    for j, data in enumerate(values):
                        #Ver se isso funciona
                        insert[order[j]] = data
                else:
                    for i, field in enumerate(table.fields_list):
                        insert[field.field_name] = values[i]
                print(insert)
                #USAR INSERT DATA
                table.data_dict_list.append(insert)
                print(table.data_dict_list)

        #print(table.data_dict_list)
    

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

    #TA FUNCIONANDO SO COM UMA PALAVRA
    def find_next_word(self, query:str, searched_word: str) -> str:  # Update the function signature to specify the return type
        query_words = query.split()
        #print(query_words)
        for i, word in enumerate(query_words):
            if searched_word.upper() == word:
                next_word = query_words[i + 1] if i + 1 < len(query_words) else ""
                #print(f"Encontrou '{searched_word}' na palavra '{word}'. Próxima palavra: {next_word}")
                return next_word
        return ""  # Ensure the function always returns a value of type "str"
    
if __name__ == "__main__":
    db = DataBase(1, "teste", "user", "password", "localhost")
    db.execute_query("SELECT ProductID, ProductName, CategoryName FROM Products, Tables INNER JOIN Categories ON Products CategoryID; ")
