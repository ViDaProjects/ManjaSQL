import tkinter as tk
from tkinter import filedialog
from manjaSQL import ManjaSQL
from tkinter import ttk
import numpy as np

main_window = tk.Tk()
main_window.title("ManjaSQL")
main_window.geometry("800x500")
#Simbolo da janela
#root.iconbitmap('caminho pra imagem')

global manja
global current_db
global create_database_window

#Get from save data
last_id = 0
manja = ManjaSQL(last_id)

presentation1 = tk.Label(main_window, text="ManjaSQL")
presentation1.pack()
presentation2 = tk.Label(main_window, text="Sistema Gerenciador de Banco de Dados")
presentation2.pack(pady=5)

#functions

def send_create_db():
    global current_db, manja
    current_db = manja.create_database(db_name_entry.get(), db_host_entry.get(), db_user_entry.get(),db_password_entry.get())
    create_label = tk.Label(db_data_frame, text="Banco de dados criado!")
    create_label.pack()    

def send_connect_db():
    global current_db
    message = manja.connect_to_database(db_name_entry.get(), db_host_entry.get(), db_user_entry.get(),db_password_entry.get())
    if message == "Conectado com sucesso!":
        send_create_db()
        message = manja.send_connection_to_database(current_db)

    connect_label = tk.Label(db_data_frame, text=message)
    connect_label.pack()         
   

def create_database_window_config(title: str): 
    global create_database_window, db_name_entry, db_host_entry, db_user_entry, db_password_entry, db_data_frame
    create_database_window = tk.Toplevel()
    create_database_window.title("ManjaSQL - " + title)
    create_database_window.geometry("800x500")
    create_database_window.resizable(False, False)
    create_database_window.focus_force()
    create_database_window.grab_set()
    create_database_window.transient(main_window)
    create_database_window.protocol("WM_DELETE_WINDOW", lambda: close_create_database_window())

    db_data_frame = tk.Frame(create_database_window, pady=20)
    db_data_frame.pack()
    
    db_name_frame = tk.Frame(db_data_frame, pady=10)
    db_name_frame.pack()
    db_name_label = tk.Label(db_name_frame, text="Nome do Banco de Dados: ")
    db_name_label.pack()
    db_name_entry = tk.Entry(db_name_frame, )
    db_name_entry.pack()
    db_name_entry.insert(0, "livros-db")

    db_host_frame = tk.Frame(db_data_frame, pady=10)
    db_host_frame.pack()
    db_host_label = tk.Label(db_host_frame, text="Host: ")
    db_host_label.pack()
    db_host_entry = tk.Entry(db_host_frame)
    db_host_entry.pack()
    db_host_entry.insert(0, "localhost")

    db_user_frame = tk.Frame(db_data_frame, pady=10)
    db_user_frame.pack()
    db_user_label = tk.Label(db_user_frame, text="Usuário: ")
    db_user_label.pack()
    db_user_entry = tk.Entry(db_user_frame)
    db_user_entry.pack()
    db_user_entry.insert(0, "user")

    db_password_frame = tk.Frame(db_data_frame, pady=10)
    db_password_frame.pack()
    dp_password_label = tk.Label(db_password_frame, text="Senha: ")
    dp_password_label.pack()
    db_password_entry = tk.Entry(db_password_frame)
    db_password_entry.pack()
    db_password_entry.insert(0, "SENHA2senha.")
   
def close_create_database_window():
    global create_database_window
    create_database_window.destroy()


def close_select_database_window():
    global select_database_window
    select_database_window.destroy()

def close_current_database_window():
    current_database_window.destroy()

def close_login_database_window():
    global login_database_window
    login_database_window.destroy()
    
def close_execute_query_window():
    execute_query_window.destroy()

def close_import_csv_window():
    import_csv_window.destroy() 

def close_query_results_window():
    query_results_window.destroy()  
    create_current_database_window()  

def create_database():  
    create_database_window_config("Criar Banco de Dados")
    db_create_button = tk.Button(db_data_frame, text="Criar", command=send_create_db)
    db_create_button.pack()

    
def select_database():  
    global select_database_window, existent_database_button, query_text
    select_database_window = tk.Toplevel()
    select_database_window.title("ManjaSQL - Selecionar Banco de Dados")
    select_database_window.geometry("800x500")
    select_database_window.resizable(False, False)
    select_database_window.focus_force()
    select_database_window.grab_set()
    select_database_window.transient(main_window)
    select_database_window.protocol("WM_DELETE_WINDOW", lambda: close_select_database_window())

    db_select_frame = tk.Frame(select_database_window, pady=20)
    db_select_frame.pack()

    if manja.database_list == []:
        db_information = tk.Label(db_select_frame, text="Ainda não possui Bancos de Dados")
        db_information.pack()
    else:    
        db_information = tk.Label(db_select_frame, text="Bancos de dados existentes: ")
        db_information.pack()
        for i, database in enumerate(manja.database_list):
            existent_database_button = tk.Button(db_select_frame, text=database.db_name, borderwidth=5, padx=15, pady=15, command= lambda k=i: login_database(k))
            existent_database_button.pack(pady=10)

def verify_login():
    if current_database.login(db_user_login_entry.get(), db_password_login_entry.get()):
        login_database_window.destroy()
        create_current_database_window()
    else:
        db_incorrect_login_label = tk.Label(db_login_frame, text="Credenciais incorretas")
        db_incorrect_login_label.pack()

def login_database(i: int):
    global current_database, login_database_window, select_database_window
    global db_password_login_entry, db_user_login_entry, db_login_frame
    current_database = manja.database_list[i]
    select_database_window.destroy()

    login_database_window = tk.Toplevel()
    login_database_window.title("ManjaSQL - Login - Banco de Dados: " + current_database.db_name)
    login_database_window.geometry("800x500")
    login_database_window.resizable(False, False)
    login_database_window.focus_force()
    login_database_window.grab_set()
    login_database_window.transient(main_window)
    login_database_window.protocol("WM_DELETE_WINDOW", lambda: close_login_database_window())

    db_login_frame = tk.Frame(login_database_window, pady=20)
    db_login_frame.pack()

    db_user_login_frame = tk.Frame(db_login_frame, pady=10)
    db_user_login_frame.pack()
    db_user_login_label = tk.Label(db_user_login_frame, text="Usuário: ")
    db_user_login_label.pack()
    db_user_login_entry = tk.Entry(db_user_login_frame)
    db_user_login_entry.pack()
    db_user_login_entry.insert(0, "user")

    db_password_login_frame = tk.Frame(db_login_frame, pady=10)
    db_password_login_frame.pack()
    db_password_login_label = tk.Label(db_password_login_frame, text="Senha: ")
    db_password_login_label.pack()
    db_password_login_entry = tk.Entry(db_password_login_frame)
    db_password_login_entry.pack()
    db_password_login_entry.insert(0, "SENHA2senha.")

    db_login_button = tk.Button(db_login_frame, text="Confirmar", command= verify_login)
    db_login_button.pack()

    db_cancel_login_button = tk.Button(db_login_frame, text="Cancelar", command= close_login_database_window)
    db_cancel_login_button.pack()

def create_query_window():
    global query_text, execute_query_window, query_db_frame
    close_current_database_window()
    execute_query_window = tk.Toplevel()
    execute_query_window.title("ManjaSQL - Banco de Dados: " + current_database.db_name)
    execute_query_window.geometry("800x650")
    execute_query_window.resizable(False, False)
    execute_query_window.focus_force()
    execute_query_window.grab_set()
    execute_query_window.transient(main_window)
    execute_query_window.protocol("WM_DELETE_WINDOW", lambda: close_execute_query_window())

    query_db_frame = tk.Frame(execute_query_window, pady=20)
    query_db_frame.pack()

    query_text = tk.Text(query_db_frame, width=60, height=20)
    query_text.pack(pady=20)
    execute_query_button = tk.Button(query_db_frame, text="Executar query", borderwidth=5, padx=15, pady=15, command= execute_query_function)
    execute_query_button.pack(pady=10)

#Result of "Select * from table"
#k - button id
def show_all_saved_data(k: int):
    global query_columns, result_table
    current_table = current_database.tables_list[k]
    current_database_window.destroy()
    query_columns = list(field.field_name for field in current_table.fields_list)
    
    columns_length = len(query_columns)
    lines_length = len(current_table.data_dict_list)
    result_table = np.zeros((lines_length, columns_length), dtype=object)

    #Save result on table
    for i in range(result_table.shape[0]):
        for j in range(result_table.shape[1]):
            result_table[i, j] = current_table.data_dict_list[i][query_columns[j]]
    
    create_query_results_window()


def create_current_database_window():
    global current_database_window
    
    current_database_window = tk.Toplevel()
    current_database_window.title("ManjaSQL - Banco de Dados: " + current_database.db_name)
    current_database_window.geometry("800x500")
    current_database_window.resizable(False, False)
    current_database_window.focus_force()
    current_database_window.grab_set()
    current_database_window.transient(main_window)
    current_database_window.protocol("WM_DELETE_WINDOW", lambda: close_current_database_window())

    current_db_frame = tk.Frame(current_database_window, pady=20)
    current_db_frame.pack()

    create_query = tk.Button(current_db_frame, text="Escrever query", borderwidth=5, padx=15, pady=15, command = create_query_window)
    create_query.pack(pady=10)

    #Import data from CSV
    import_from_csv_button = tk.Button(current_db_frame, text="Importar dados de um arquivo CSV", borderwidth=5, padx=15, pady=15, command=import_from_csv)
    import_from_csv_button.pack(pady=10)

    if current_database.tables_list == []:
        db_tables_list = tk.Label(current_db_frame, text="Ainda não possui tabelas")
        db_tables_list.pack()
    else:    
        db_tables_list = tk.Label(current_db_frame, text="Tabelas existentes: ")
        db_tables_list.pack()
        for i, table in enumerate(current_database.tables_list):
            table_list_button = tk.Button(current_db_frame, text=table.table_name, borderwidth=5, padx=15, pady=15, command= lambda k=i: show_all_saved_data(k))
            table_list_button.pack(pady=10, side= tk.LEFT)


def execute_query_function():
    global query_text, query_columns, result_table, query_db_frame
    #query translate
    query_manja = query_text.get(1.0, tk.END)
    query_sql = current_database.translator(query_manja)
    print(query_sql)
    #trocar para query_sql
    query_results = current_database.execute_query(query_sql)
    print(query_results)
    #current_database.update(query_text.get(1.0, tk.END))
    #current_database.delete(query_text.get(1.0, tk.END))
    if query_results:
        if query_results == "Query executada com sucesso!":
            query_result_label = tk.Label(query_db_frame, text=query_results)
            query_result_label.pack()
        else:
            show_select_results(list(query_results))
  

def show_select_results(query_results: list):
    global query_columns, result_table
    #PRECISO DO QUERY COLUMNSSSS
    query_columns = current_database.field_names_from_select
    #Columns and lines quantities in this select
    columns_len = len(query_columns)
    lines_len = len(query_results)
    result_table = np.zeros((lines_len, columns_len), dtype=object)

    #Save result on table
    for i in range(result_table.shape[0]):
        for j in range(result_table.shape[1]):
            #result_table[i, j] = list(str(result[query_columns[j]]) for result in query_results[i])
            result_table[i, j] = str(query_results[i][query_columns[j]])
    
    close_execute_query_window()
    create_query_results_window()

def create_query_results_window():
    global query_results_window, query_columns, result_table

    query_results_window = tk.Toplevel()
    query_results_window.title("ManjaSQL - Banco de Dados: " + current_database.db_name)
    query_results_window.geometry("1400x800")
    query_results_window.resizable(False, False)
    query_results_window.focus_force()
    query_results_window.grab_set()
    query_results_window.transient(main_window)
    query_results_window.protocol("WM_DELETE_WINDOW", lambda: close_query_results_window())

    query_results_frame = tk.Frame(query_results_window, pady=10)
    query_results_frame.pack(expand=True, fill=tk.BOTH)

    
    tree = ttk.Treeview(query_results_frame, columns=query_columns, show="headings")

    #config headings
    for column_str in query_columns:
        tree.heading(column_str,text=column_str)
        tree.column(column_str, anchor="center")

    #config columns data
    for i in range(result_table.shape[0]):
        tree.insert("", tk.END, values=tuple(result_table[i]))

    tree.pack(expand=True, fill=tk.BOTH)


def connect_database():    
    create_database_window_config("Conectar a um Banco de Dados existente")
    connect_create_button = tk.Button(db_data_frame, text="Conectar", command=send_connect_db)
    connect_create_button.pack()	

def import_csv_function():
    current_database.import_database(table_name_entry.get(), file_path)
    #Atualizar result_table talvez ---- erro no current database window
    close_import_csv_window()
    create_current_database_window()

def search_csv_file():
    global file_path
    file_path = filedialog.askopenfilename(title="Selecionar arquivo CSV", filetypes=[("Arquivos CSV", "*.csv")])
    if file_path:
        csv_frame = tk.Frame(csv_data_frame, pady=10)
        csv_frame.pack()
        csv_label = tk.Label(csv_frame, text="Caminho do arquivo: " + file_path)
        csv_label.pack()
        import_csv_button = tk.Button(csv_data_frame, text="Importar", borderwidth=5, padx=15, pady=15, command= import_csv_function)
        import_csv_button.pack(pady=10)

def import_from_csv():
    global import_csv_window, csv_data_frame, table_name_entry
    close_current_database_window()
    import_csv_window = tk.Toplevel()
    import_csv_window.title("ManjaSQL - Banco de Dados: " + current_database.db_name)
    import_csv_window.geometry("800x500")
    import_csv_window.resizable(False, False)
    import_csv_window.focus_force()
    import_csv_window.grab_set()
    import_csv_window.transient(main_window)
    import_csv_window.protocol("WM_DELETE_WINDOW", lambda: close_import_csv_window())

    csv_data_frame = tk.Frame(import_csv_window, pady=20)
    csv_data_frame.pack()

    table_name_frame = tk.Frame(csv_data_frame, pady=10)
    table_name_frame.pack()
    table_name_label = tk.Label(table_name_frame, text="Nome da tabela: ")
    table_name_label.pack()
    table_name_entry = tk.Entry(table_name_frame)
    table_name_entry.pack()

    find_csv_button = tk.Button(csv_data_frame, text="Buscar arquivo", borderwidth=5, padx=15, pady=15, command= search_csv_file)
    find_csv_button.pack(pady=10)
   

#create new database 
new_database_button = tk.Button(main_window, text="Novo banco de dados", borderwidth=5, padx=15, pady=15, command=create_database)
new_database_button.pack(pady=10)

#Select required database
choose_database_button = tk.Button(main_window, text= "Escolher um Banco de Dados", borderwidth=5, padx=15, pady=15, command=select_database)
choose_database_button.pack(pady=10)

#Connect to existent database
connect_to_database_button = tk.Button(main_window, text="Conectar a um banco de dados", borderwidth=5, padx=15, pady=15, command=connect_database)
connect_to_database_button.pack(pady=10)

#Window loop
main_window.mainloop()