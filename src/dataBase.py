from table import Table

#atributo privado: __nome__
class DataBase:

    db_id = int
    db_name = str    
    new_table_name = str
    fields_list = [str] #class fields
    tables_list = [Table] #class table
    tables_name_list = [str]

    def __init__(self, id: int, name: str) -> None:
        self.fields_list = []
        self.tables_list = []
        self.tables_name_list = []
        self.new_table_name = ""
        self.db_id = id
        self.db_name = name

    def create_table(self, id: int, query: str):
        #Cria um json com esse nome
        self.new_table_name = self.find_next_word(query, "CREATE TABLE")
        new_table = Table(id, self.new_table_name)
        self.table_name_list.append(self.new_table_name)
        self.table_list.append(new_table)
        return new_table

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

    def select(self, query: str):
        table_name = self.find_next_word(query, "FROM")
        for i, table in enumerate(self.tables_name_list):
            if table == table_name:
                self.tables_list[i].select_data(query)
                break

    def update(query: str):
        pass

    def delete(query: str):
        pass

    def insert(query: str):
        pass

    def save_data():
        pass

    def find_next_word(self, query:str, searched_word: str):
        query_words = query.split()
        
        for i, word in enumerate(query_words):
            if searched_word.upper() == word:
                next_word = query_words[i + 1] if i + 1 < len(query_words) else None
                print(f"Encontrou '{searched_word}' na palavra '{word}'. Próxima palavra: {next_word}")
                return next_word
        return  
