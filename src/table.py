from field import Field
from data import Data
from typing import List

class Table:

    def __init__(self, table_id: str, table_name: str) -> None:
        self.table_id = table_id
        self.table_name = table_name
        self.fields_list: List[Field] = [] 
        self.fields_name_list = []
        self.data: List[Data] = [] 
        self.primary_key = []
        self.foreign_key = []
        self.current_field_id = 0
        self.current_data_id = 0

    def create_field(self, id: int, name: str, type: str, constraints: str, query: str):
        
        #receive some data and divide it on each variable

        new_field = Field(id, name, type, constraints)
        self.fields.append(new_field)
        #define primary and foreign keys here
        pass
        
    def define_foreign_key(self, name: str, data: str):
        #receive some data and divide it on each variable
        self.foreign_key.append(name)
        
        for field in self.fields:
            if field.field_name == name:
                field.is_foreign_key = 1
                field.origin_field_name = ""
                field.origin_table_name = ""
                field.foreign_key_constraints = ""

    def define_primary_key(self, name: str):
        self.primary_key.append(name)

    def insert_data(self, query: str):
        #Colocar os dados da query em um vetor 
        data = []
        new_data = Data(data)
        self.data.append(new_data)

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
            '=': lambda x, y: x == y
        }

        return operators.get(string_operator, None)                