from dataBase import DataBase
from typing import List

class ManjaSQL:

    def __init__(self, last_id: int) -> None:
        self.database_name_list = []
        self.database_list: List[DataBase] = [] 
        #lista do tipo database tbm
        self.new_database_name = ""
        self.id = last_id
        #save last id data on txt or json for backup
        #calls get_db_data
        pass

    def create_database(self, name: str, host: str, user: str, password: str):
        #Cria um diretorio com esse nome
        self.new_database_name = name
        new_database = DataBase(self.iterate_new_id(), name, host, user, password)
        self.database_name_list.append(self.new_database_name)
        self.database_list.append(new_database)
        return new_database

    def iterate_new_id(self):
        self.id += 1
        return self.id
    
    def get_new_database_name(self):
        return self.new_database_name
        
    def drop_database():
        pass

    def get_db_data():
        #se existir data, inicializa os bancos de dados existentes, etc
        pass

    def find_next_word(self, query:str, searched_word: str):
        query_words = query.split()
        
        for i, word in enumerate(query_words):
            if searched_word.upper() == word:
                next_word = query_words[i + 1] if i + 1 < len(query_words) else None
                print(f"Encontrou '{searched_word}' na palavra '{word}'. Próxima palavra: {next_word}")
                return next_word
        return "" #tem como retornar falso?
    
    #Retirar a ultima palavra buscada da query e retornar a query reduzida
    def reduzir_query():
        pass