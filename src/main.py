from manjaSQL import ManjaSQL
from dataBase import DataBase
from field import Field
from table import Table
from data import Data
from translator import Translator

def find_next_word(self, query:str, searched_word: str):
    query_words = query.split()
    
    for i, word in enumerate(query_words):
        if searched_word.upper() == word:
            next_word = query_words[i + 1] if i + 1 < len(query_words) else None
            print(f"Encontrou '{searched_word}' na palavra '{word}'. Próxima palavra: {next_word}")
            return next_word
    return "" #tem como retornar falso?


#Initialize
DBMS = ManjaSQL()

#busca dos dados existentes

command = ""
#receber comando do usuario
id = 1
current_database = DataBase
current_table = Table

while command != "exit":
    query_words = command.split()
    for i, word in enumerate(query_words):
        if "CREATE DATABASE".upper() == word:
            #quebrar a query a partir do create database
            new_query = query_words[i]
            current_database = DBMS.create_database(new_query, id)

        if "GET INTO DATABASE".upper() == word:
            new_database_name = query_words[i + 1] if i + 1 < len(query_words) else None
            for i, database in enumerate(DBMS.database_name_list):
                if database == new_database_name:
                    current_database = DBMS.database_list[i]  
                    break   

        if "IMPORT DATA FROM DATABASE".upper() == word:
            database_name = query_words[i + 1] if i + 1 < len(query_words) else None
            current_database = database_name

        if "IMPORT DATA FROM CSV".upper() == word:
            pass

        if "CREATE TABLE".upper() == word:
            #Ver se isso verifica a existencia desse ponteiro
            if not current_database:
                print("Erro! Banco de Dados não definido.")
                #Precisa sair do while
                break
            current_table = current_database.create_table()   
            #passar para o sql parser que devolve um json no padrão de objeto
            # E utilizar a função python para popular as classes com o json  

        if "GET INTO TABLE".upper() == word:
            #verificar se esta dentro de um database
            if not current_database:
                print("Erro! Banco de Dados não definido.")
                #Precisa sair do while
                break            
            new_table_name = query_words[i + 1] if i + 1 < len(query_words) else None
            for i, table in enumerate(current_database.tables_name_list):
                if table == new_table_name:
                    current_table = current_database.tables_list[i]  
                    break

        if "SELECT".upper() == word:
            #verificar se esta dentro de um database
            if not current_database:
                print("Erro! Banco de Dados não definido.")
                #Precisa sair do while
                break   
            #quebrar a query a partir do select
            new_query = query_words[i]
            current_database.select(new_query)          

        if "UPDATE".upper() == word:
            #verificar se esta dentro de um database
            if not current_database:
                print("Erro! Banco de Dados não definido.")
                #Precisa sair do while
                break 
            #quebrar a query a partir do select
            new_query = query_words[i]
            current_database.update(new_query) 

        if "INSERT INTO".upper() == word:
            #verificar se esta dentro de um database
            if not current_database:
                print("Erro! Banco de Dados não definido.")
                #Precisa sair do while
                break 
            #quebrar a query a partir do select
            new_query = query_words[i]
            current_database.insert(new_query) 

        if "DELETE".upper() == word:
            #verificar se esta dentro de um database
            if not current_database:
                print("Erro! Banco de Dados não definido.")
                #Precisa sair do while
                break 
            #quebrar a query a partir do select
            new_query = query_words[i]
            current_database.delete(new_query)    
    
    id = id + 1 


#Nao faço mais a minima ideia de como/onde criar as tabelas, campos e data base e onde ficar lendo o comando 
# na main? ou um dentro do outro? 
#manja sql cria database
#database cria tabela 
#tabela cria campo
#database faz select, update, delete      
  


