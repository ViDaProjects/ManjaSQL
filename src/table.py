from field import Field
from typing import List

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

    def create_field(self, name: str, type: str, constraints: str):
        id = "field_" + str(self.current_field_id) + "_" + self.table_id
        new_field = Field(id, name, type, constraints)
        self.current_field_id += 1
        self.fields_list.append(new_field)
        #define primary and foreign keys here
        return new_field
    
    def import_fields_from_csv(self, fields: List[Field]):
        self.fields_list = fields
        
    
    #Define attributes if field is foreignkey
    #Parameters:
    #foreign_data = [field_name, origin_table_name, origin_field_name, constraints]
    def define_key_type(self, field: Field, key_data: str):
        if field is None:
            field_object = (field for i, field in enumerate(self.fields_list) if self.fields_list[i].field_name == key_data[0])
        else:
            field_object = field

        field_object.key_type = key_data[0]
        field_object.origin_table_name = key_data[1]
        field_object.foreign_key_constraints = key_data[2]

        if field_object.key_type == "PRIMARY KEY":
            self.primary_key.append(field_object)
        elif field_object.key_type == "FOREIGN KEY":
            self.foreign_key.append(field_object)
        elif field_object.key_type == "UNIQUE KEY":
            self.unique_key.append(field_object)

    def define_primary_key(self, name: str):
        field_object = (field for i, field in enumerate(self.fields_list) if self.fields_list[i].field_name == name)
        self.primary_key.append(field_object)

    #Same length of indexes and data
    def insert_data(self, indexes: List, data: List):
        data_current_dict = {}
        if len(indexes) == len(data):
            print(data)
            for i, index in enumerate(indexes):
                print(index)
                print(i)
                data_current_dict[index] = data[index]
            self.data_dict_list.append(data_current_dict)
        else:
            print("Não foi possível inserir os dados")        
    #iimport csv
    #insert
    #update
 
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


    def find_next_word(self, query:str, searched_word: str):
        query_words = query.split()
        
        for i, word in enumerate(query_words):
            if searched_word.upper() == word:
                next_word = query_words[i + 1] if i + 1 < len(query_words) else None
                print(f"Encontrou '{searched_word}' na palavra '{word}'. Próxima palavra: {next_word}")
                return next_word
        return ""      

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
            '=': lambda x, y: x == y,
            'AND': lambda x, y: x and y,
            'OR': lambda x, y: x or y
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