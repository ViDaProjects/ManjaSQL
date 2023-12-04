from field import Field
from typing import List
import os 
import json

class Table:

    def __init__(self, table_id: str, table_name: str) -> None:
        self.table_id = table_id
        self.table_name = table_name
        self.fields_list: List[Field] = [] 
        self.data_dict_list = []
        self.data_current_dict = {}
        self.primary_key: List[Field] = [] 
        self.foreign_key : List[Field] = [] 
        self.unique_key : List[Field] = []
        self.current_field_id = 0

    def create_field(self, name: str, type: str, constraints: str, db_name: str):
        id = "field_" + str(self.current_field_id) + "_" + self.table_id
        new_field = Field(id, name, type, constraints)
        self.current_field_id += 1
        self.fields_list.append(new_field)
        self.save_create_field_on_json(new_field, db_name)
        #define primary and foreign keys here
        return new_field
    
    def save_create_field_on_json(self, field: Field, db_name: str):
        field_dict = {}
        current_path = os.getcwd()
        db_path = os.path.join(current_path, db_name) 
        json_path = os.path.join(db_path, self.table_name + ".json")
        
        existent_data = self.get_existent_table_json(db_name)

        field_dict['FIELD_ID'] = field.field_id
        field_dict['FIELD_NAME'] = field.field_name
        field_dict['TYPE'] = field.type
        field_dict['CONSTRAINTS'] = field.constraints
        field_dict['KEY TYPE'] = ""
        field_dict['ORIGIN TABLE'] = ""
        field_dict['FOREIGIN CONSTRAINTS'] = ""
        print("tamanho")
        print(len(self.fields_list))
        existent_data['COLUMNS'][len(self.fields_list)] = field_dict
        #existent_data['COLUMNS'].append = field_dict

        #Fazer o columns como um dicionário também e uma chave para acessar (field_name)

        with open(json_path, 'w') as json_file:
            json.dump(existent_data, json_file)
    
    
    def import_fields_from_csv(self, fields: List[Field]):
        self.fields_list = fields
        
    def get_existent_table_json(self, db_name: str):
        current_path = os.getcwd()
        db_path = os.path.join(current_path, db_name) 
        json_path = os.path.join(db_path, self.table_name + ".json")
        print(f'Diretório atual get existent data on json: {os.getcwd()}')

        existent_data = {}
        with open(json_path, 'r') as json_file:
            existent_data = json.load(json_file)
        
        return existent_data


    #Define attributes if field is foreignkey
    #Parameters:
    #foreign_data = [field_name, origin_table_name, origin_field_name, constraints]
    def define_key_type(self, key_data: str, db_name: str):
        field_position = len(self.fields_list)
        field_object = None
        field_dict = {}
        for i, field in enumerate(self.fields_list):
            if field.field_name == key_data[0]:
                field_position = i
                field_object = field

        field_object.key_type = key_data[0]
        field_object.origin_table_name = key_data[1]
        field_object.foreign_key_constraints = key_data[2]
        field_dict['KEY TYPE'] = key_data[0]
        field_dict['ORIGIN TABLE'] = key_data[1]
        field_dict['FOREIGN CONSTRAINTS'] = key_data[2]

        current_path = os.getcwd()
        db_path = os.path.join(current_path, db_name) 
        json_path = os.path.join(db_path, self.table_name + ".json") 

        existent_data = self.get_existent_table_json(db_name)

        existent_data['COLUMNS'][field_position] = field_dict

        if field_object.key_type == "PRIMARY KEY":
            self.primary_key.append(field_object)
            existent_data['PRIMARY KEY'] = (key.field_name for key in self.primary_key)
        elif field_object.key_type == "FOREIGN KEY":
            self.foreign_key.append(field_object)
            existent_data['FOREIGN KEY'] = (key.field_name for key in self.foreign_key)
        elif field_object.key_type == "UNIQUE KEY":
            self.unique_key.append(field_object)
            existent_data['UNIQUE KEY'] = (key.field_name for key in self.unique_key)

        with open(json_path, 'w') as json_file:
            json.dump(existent_data, json_file) 


    #Same length of indexes and data
    def insert_data(self, indexes: List, data: List, is_csv: bool, db_name: str):
        data_current_dict = {}
        if len(indexes) == len(data):
            if is_csv:
                for index in indexes:
                    data_current_dict[index] = data[index]
            else:
                for i, index in enumerate(indexes):
                    data_current_dict[index] = data[i]                
            self.data_dict_list.append(data_current_dict)
            self.save_table_data_on_json(data_current_dict, db_name)
        else:
            print("Não foi possível inserir os dados")        
 
    def save_table_data_on_json(self, data: List, db_name: str):
        current_path = os.getcwd()
        db_path = os.path.join(current_path, db_name) 
        json_path = os.path.join(db_path, self.table_name + ".json")        
        
        existent_data = self.get_existent_table_json(db_name)
        index = len(self.data_dict_list)
        print(existent_data)
        existent_data['DATA'][index] = data

        with open(json_path, 'w') as json_file:
            json.dump(existent_data, json_file) 
    

    def update_data(self, query: str, where: str):
        #descobre proxima palavra depois do where
        update_positions = []
        update_data = []
        column = ""
        condition = ""
        for i, field_name in self.fields[i].field_name:
            if field_name == column:
                condition_position = i

            #descobrir posições dos dados para serem alterados    
            
        for j, column_data in self.data[j].fields_data[condition_position]:
            if column_data == condition:
                for k in update_positions:
                    self.data[j].fields[k] = update_data[k]


    def delete_data(self, query: str, where: str):
        #descobre condição do where
        column = ""
        condition = ""
        for i, field_name in self.fields[i].field_name:
            if field_name == column:
                condition_position = i

        for j, column_data in self.data[j].fields_data[condition_position]:
            if column_data == condition:
                self.data[j].fields_data.clear()    



    def select_data(self, query: str):
        #Tem que ser possivel comparar um ou dois campos
        selected_fields = []
        where_field = self.find_next_word(query, "WHERE")
        #where field +/-/=/>/< condition
        condition_operator = self.find_next_word(query, where_field)
        condition_value = self.find_next_word(query, condition_operator)
        order_by_field = self.find_next_word(query, "ORDER BY")
        order_direction = self.find_next_word(query, order_by_field)

        selected_fields_position = []
        where_field_position = []
        order_by_field_position = []
        result = []

        operator = self.recognize_operator(condition_operator)

        for i, field_name in enumerate(self.fields_list_name):
            if field_name in selected_fields:
                selected_fields_position.append(i)

            if field_name in where_field:
                where_field_position.append(i)  

            if field_name in order_by_field:
                order_by_field_position.append(i)                  



        #BUSCAR DENTRO DA CLASSE DATA
        for i, data in enumerate(self.data):
            #DATA TEM QUE SATISFAZER A CONDIÇÃO
            #Satisfazer a condição com o sinal certo, COMO PEGAR O SINAL?????????
            #varios ifs?
            if data.fields_data[where_field_position] in where_field and operator(where_field, condition_value):
                selected_data = []
                self.tables_list[i].select_data(query)
                break


    def recognize_operator(self, string_operator):
        operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '>': lambda x, y: x > y,
            '<': lambda x, y: x < y,
            '=': lambda x, y: x == y
        }

        return operators.get(string_operator, None)                

# Exemplo de uso
#operador_string = ">"

# Mapear a string do operador para uma função
#operador = mapear_operador(operador_string)

'''if operador:
    resultado = operador(5, 3)  # Substitua 5 e 3 pelos valores que deseja comparar
    print(f"O resultado da comparação é: {resultado}")
else:
    print("Operador não reconhecido.")'''