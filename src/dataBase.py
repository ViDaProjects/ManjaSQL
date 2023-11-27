from table import Table

class DataBase:

    db_id = int
    db_name = str
    fields_list = list[str] #class fields
    tables_list = list[Table] #class table

    def __init__(self, id: int, name: str) -> None:
        self.fields_list = []
        self.tables_list = []
        self.db_id = id
        self.db_name = name

    def create_table(self, query: str):
       
       pass 

    def drop_table():
        pass

    def import_database():
        pass

    def create_table_by_json():
        pass

    def connect_to_database():
        pass

    def read_query(query: str):
        pass

    def select(query: str):
        pass

    def update(query: str):
        pass

    def delete(query: str):
        pass

    def insert(query: str):
        pass

    def save_data():
        pass


