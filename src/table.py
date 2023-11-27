from field import Field
from data import Data

class Table:

    table_id = int
    table_name = str
    fields = [Field]
    data = [Data]
    primary_key = [str]
    foreign_key = [str]

    def __init__(self, table_id: int, table_name = str) -> None:
        self.fields = []
        self.data = []
        self.primary_key = []
        self.foreign_key = []

    def create_field(self, id: int, name: str, type: str, constraints: str):
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



    def select_data(self, query: str, where: str, order_by: str):
        pass


