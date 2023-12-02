import tkinter as tk
from tkinter import filedialog
from manjaSQL import ManjaSQL

main_window = tk.Tk()
main_window.title("ManjaSQL")
main_window.geometry("800x500")
#Simbolo da janela
#root.iconbitmap('caminho pra imagem')

global manja
global current_db
global current_table
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
    #Deixar apenas para criar e fechar janela, escolhe o db depois
    current_db = manja.create_database(db_name_entry.get(), db_host_entry.get(), db_user_entry.get(),db_password_entry.get())
    create_database_window.destroy()
    print(manja.database_list[0].db_name)
    pass

def create_database_window_config(): 
    global create_database_window, db_name_entry, db_host_entry, db_user_entry, db_password_entry
    create_database_window = tk.Toplevel()
    create_database_window.title("ManjaSQL - Criar Banco de Dados")
    create_database_window.geometry("800x500")
    #create_database_window.iconbitmap('src/icons/database.ico')
    create_database_window.resizable(False, False)
    create_database_window.focus_force()
    create_database_window.grab_set()
    create_database_window.transient(main_window)
    #ISso faz o que?
    create_database_window.protocol("WM_DELETE_WINDOW", lambda: close_create_database_window())

    db_data_frame = tk.Frame(create_database_window, pady=20)
    db_data_frame.pack()
    
    db_name_frame = tk.Frame(db_data_frame, pady=10)
    db_name_frame.pack()
    db_name_label = tk.Label(db_name_frame, text="Nome do Banco de Dados: ")
    db_name_label.pack()
    db_name_entry = tk.Entry(db_name_frame)
    db_name_entry.pack()

    db_host_frame = tk.Frame(db_data_frame, pady=10)
    db_host_frame.pack()
    db_host_label = tk.Label(db_host_frame, text="Host: ")
    db_host_label.pack()
    db_host_entry = tk.Entry(db_host_frame)
    db_host_entry.pack()

    db_user_frame = tk.Frame(db_data_frame, pady=10)
    db_user_frame.pack()
    db_user_label = tk.Label(db_user_frame, text="Usuário: ")
    db_user_label.pack()
    db_user_entry = tk.Entry(db_user_frame)
    db_user_entry.pack()

    db_password_frame = tk.Frame(db_data_frame, pady=10)
    db_password_frame.pack()
    dp_password_label = tk.Label(db_password_frame, text="Senha: ")
    dp_password_label.pack()
    db_password_entry = tk.Entry(db_password_frame)
    db_password_entry.pack()

    db_create_button = tk.Button(db_data_frame, text="Criar", command=send_create_db)
    db_create_button.pack()
    
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

def create_database():  
    create_database_window_config()


    
def select_database():  
    global select_database_window, existent_database_button, query_text
    select_database_window = tk.Toplevel()
    select_database_window.title("ManjaSQL - Selecionar Banco de Dados")
    select_database_window.geometry("800x500")
    #select_database_window.iconbitmap('src/icons/database.ico')
    select_database_window.resizable(False, False)
    select_database_window.focus_force()
    select_database_window.grab_set()
    select_database_window.transient(main_window)
    #ISso faz o que?
    select_database_window.protocol("WM_DELETE_WINDOW", lambda: close_select_database_window())

    db_select_frame = tk.Frame(select_database_window, pady=20)
    db_select_frame.pack()
    #fazer um for para criar um novo botão a cada database cadastrado
    for i, database in enumerate(manja.database_list):
        print(database.db_name)
        existent_database_button = tk.Button(db_select_frame, text=database.db_name, borderwidth=5, padx=15, pady=15, command= lambda: login_database(i))
        existent_database_button.pack(pady=10)



def create_table():
    
    pass

def select_table():
    pass

def verify_login():
    #Login no database, se der certo, abre a página do database, se não, volta a pagina do select
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
    #select_database_window.iconbitmap('src/icons/database.ico')
    login_database_window.resizable(False, False)
    login_database_window.focus_force()
    login_database_window.grab_set()
    login_database_window.transient(main_window)
    #ISso faz o que?
    login_database_window.protocol("WM_DELETE_WINDOW", lambda: close_login_database_window())

    db_login_frame = tk.Frame(login_database_window, pady=20)
    db_login_frame.pack()

    db_user_login_frame = tk.Frame(db_login_frame, pady=10)
    db_user_login_frame.pack()
    db_user_login_label = tk.Label(db_user_login_frame, text="Usuário: ")
    db_user_login_label.pack()
    db_user_login_entry = tk.Entry(db_user_login_frame)
    db_user_login_entry.pack()

    db_password_login_frame = tk.Frame(db_login_frame, pady=10)
    db_password_login_frame.pack()
    db_password_login_label = tk.Label(db_password_login_frame, text="Senha: ")
    db_password_login_label.pack()
    db_password_login_entry = tk.Entry(db_password_login_frame)
    db_password_login_entry.pack()

    db_login_button = tk.Button(db_login_frame, text="Confirmar", command= verify_login)
    db_login_button.pack()

    db_cancel_login_button = tk.Button(db_login_frame, text="Cancelar", command= close_login_database_window)
    db_cancel_login_button.pack()

#Fazer função com os dados para criar essa janela
def create_query_window():
    global query_text, execute_query_window
    close_current_database_window()
    execute_query_window = tk.Toplevel()
    execute_query_window.title("ManjaSQL - Banco de Dados: " + current_database.db_name)
    execute_query_window.geometry("800x500")
    #select_database_window.iconbitmap('src/icons/database.ico')
    execute_query_window.resizable(False, False)
    execute_query_window.focus_force()
    execute_query_window.grab_set()
    execute_query_window.transient(main_window)
    #ISso faz o que?
    execute_query_window.protocol("WM_DELETE_WINDOW", lambda: close_execute_query_window())

    query_db_frame = tk.Frame(execute_query_window, pady=20)
    query_db_frame.pack()

     #Text para colocar a query sql
    query_text = tk.Text(query_db_frame, width=60, height=20)
    query_text.pack(pady=20)
    execute_query_button = tk.Button(query_db_frame, text="Executar query", borderwidth=5, padx=15, pady=15, command= execute_query_function)
    execute_query_button.pack(pady=10)

def create_current_database_window():
    global current_database_window
    
    current_database_window = tk.Toplevel()
    current_database_window.title("ManjaSQL - Banco de Dados: " + current_database.db_name)
    current_database_window.geometry("800x500")
    #select_database_window.iconbitmap('src/icons/database.ico')
    current_database_window.resizable(False, False)
    current_database_window.focus_force()
    current_database_window.grab_set()
    current_database_window.transient(main_window)
    #ISso faz o que?
    current_database_window.protocol("WM_DELETE_WINDOW", lambda: close_current_database_window())

    current_db_frame = tk.Frame(current_database_window, pady=20)
    current_db_frame.pack()

    create_query = tk.Button(current_db_frame, text="Escrever query", borderwidth=5, padx=15, pady=15, command = create_query_window)
    create_query.pack(pady=10)

    #Import data from CSV
    #nova janela para informar/criar o database e informar o caminho do arquivo etc
    import_from_csv_button = tk.Button(current_db_frame, text="Importar dados de um arquivo CSV", borderwidth=5, padx=15, pady=15, command=import_from_csv)
    import_from_csv_button.pack(pady=10)

    if current_database.tables_list == []:
        db_tables_list = tk.Label(current_db_frame, text="Ainda não possui tabelas")
        db_tables_list.pack()
    else:    
        db_tables_list = tk.Label(current_db_frame, text="Tabelas existentes: ")
        db_tables_list.pack()
        for i, table in enumerate(current_database.tables_list):
            print(table.table_name)
            table_list = tk.Button(current_db_frame, text=table.table_name, borderwidth=5, padx=15, pady=15, state = tk.DISABLED)
            table_list.pack(pady=10)

def execute_query_function():
    global query_text
    current_database.execute_query(query_text.get(1.0, tk.END))
    print(query_text.get(1.0, tk.END))
    table = current_database.create_table(query_text.get(1.0, tk.END))
    print(table.table_name)
    print("criou?")
    close_execute_query_window()
    create_current_database_window()

def show_query_results():
    pass


def connect_database():    
	pass

def import_csv_function():
    current_database.import_database(table_name_entry.get(), file_path)

def search_csv_file():
    global file_path
    if file_path == None:
        file_path = filedialog.askopenfilename(title="Selecionar arquivo CSV", filetypes=[("Arquivos CSV", "*.csv")])
        if file_path:
            print(f"Arquivo CSV selecionado: {file_path}")
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
    #select_database_window.iconbitmap('src/icons/database.ico')
    import_csv_window.resizable(False, False)
    import_csv_window.focus_force()
    import_csv_window.grab_set()
    import_csv_window.transient(main_window)
    #ISso faz o que?
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

    

    
#choose database
#Lista abaixo os database cadastrados
#quando clica aparece nova janela para fazer login no database
#depois do login, fecha segunda janela e abre a terceira com os dados do data base

#create new database (pode ser só um campo new, no choose database)
#Nova janela para preencher os campos: nome, host, user, password, etc
new_database_button = tk.Button(main_window, text="Novo banco de dados", borderwidth=5, padx=15, pady=15, command=create_database)
new_database_button.pack(pady=10)

  
choose_database_button = tk.Button(main_window, text= "Escolher um Banco de Dados", borderwidth=5, padx=15, pady=15, command=select_database)
choose_database_button.pack(pady=10)

#Connect to existent database
#nova janela para login e coisas necessárias
connect_to_database_button = tk.Button(main_window, text="Conectar a um banco de dados", borderwidth=5, padx=15, pady=15, command=connect_database)
connect_to_database_button.pack(pady=10)


#-------------------------------------------------------

#dentro do database
#selecionar botão de criar tabela e as tabelas existentes listadas em botões
# Se criar tabela: aparece um text box já escrito CREATE TABLE para completar a query
# Se seleciona uma tabela existente, aparece um text box para realizar a query dentro daquela tabela
# Tem que aparecer o nome da tabela atual
#Depois de um select, abrir nova janela para exibir resultados



#Window loop
main_window.mainloop()