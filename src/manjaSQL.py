from dataBase import DataBase
from typing import List
import mysql.connector
from mysql.connector import Error
import os

class ManjaSQL:

    def __init__(self, last_id: int) -> None:
        self.database_list: List[DataBase] = [] 
        self.new_database_name = ""
        self.id = last_id
        #save last id data on txt or json for backup
        self.saved_data_default_path = ""
        self.load_saved_data()

    def create_database(self, name: str, host: str, user: str, password: str):
        self.new_database_name = name
        new_database = DataBase(self.iterate_new_id(), name, host, user, password)
        self.database_list.append(new_database)
        self.save_database_data(new_database)
        return new_database

    def save_database_data(self, db: DataBase):
        #Create database dir
        current_dir = self.saved_data_default_path
        path_new_database = os.path.join(current_dir, db.db_name)
        db.db_default_path = path_new_database
        print("Path para conectar com novo banco")
        print(path_new_database)

        if os.path.exists(path_new_database) and os.path.isdir(path_new_database):
            os.chdir(path_new_database)
            path_new_database_txt = os.path.join(path_new_database, (db.db_name + ".txt"))
            if not (os.path.exists(path_new_database_txt) and os.path.isdir(path_new_database_txt)):
                with open(path_new_database_txt, 'w') as file:
                    file.write(db.db_name + "\n")
                    file.write(db.host + "\n")
                    file.write(db.user + "\n")
                    file.write(db.password + "\n")    
        else: 
            os.mkdir(path_new_database)
            path_new_database_txt = os.path.join(path_new_database, (db.db_name + ".txt"))
            #escreer dados de conexão no txt
            with open(path_new_database_txt, 'w') as file:
                # Escreve no arquivo
                file.write(db.db_name + "\n")
                file.write(db.host + "\n")
                file.write(db.user + "\n")
                file.write(db.password + "\n") 
    
    def connect_to_database(self, db_name: str, host: str, user: str, password: str):
        try:
            self.connection = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=db_name,
                raise_on_warnings=True
            )
            self.cursor = self.connection.cursor()
            return "Conectado com sucesso!"

        except mysql.connector.Error as e:
            return ("Erro de MySQL: " + str(e))
        except Exception as e:
            return ("Erro: " + str(e))
            
   
    def send_connection_to_database(self, db: DataBase):
        self.connection.close()  # Feche a conexão após a execução        
        return db.get_data_from_connected_database()

    def iterate_new_id(self):
        self.id += 1
        return self.id
    
    def get_new_database_name(self):
        return self.new_database_name
        
    def drop_database():
        pass

    def load_saved_databases(self, databases_files: List):
        database_data = []
        for database in databases_files:
            path_database = os.path.join(self.saved_data_default_path, database)
            path_database_txt = os.path.join(path_database, database + ".txt")
            with open(path_database_txt, 'r') as file:
                for line in file: 
                    database_data.append(line.strip())
                
            new_database = self.create_database(database_data[0], database_data[1], database_data[2], database_data[3]) 
            #os.chdir(path_database)
            saved_tables = os.listdir()
            if saved_tables:
                new_database.load_saved_tables(saved_tables, path_database)
 
            database_data = []

    def load_saved_data(self):
        current_dir = os.getcwd()

        #path to dir saved_data
        path_saved_data = os.path.join(current_dir, '..', 'saved_data')
        if os.path.exists(path_saved_data) and os.path.isdir(path_saved_data):
            #Changes to dir "ManjaSQL/saved_data"
            os.chdir(path_saved_data)
            self.saved_data_default_path = str(os.getcwd())
            print("path no load manja sql")
            print(self.saved_data_default_path)
            #Files on this dir
            saved_databases = os.listdir()
            if saved_databases:
                self.load_saved_databases(saved_databases)

        else:
            os.mkdir(path_saved_data)
            os.chdir(path_saved_data)
            self.saved_data_default_path = str(os.getcwd())

