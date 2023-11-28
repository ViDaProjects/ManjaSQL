from tkinter import *

main_window = Tk()
main_window.title("ManjaSQL")
main_window.geometry("800x500")
#Simbolo da janela
#root.iconbitmap('caminho pra imagem')

presentation1 = Label(main_window, text="ManjaSQL", font=100)
presentation1.pack()
presentation2 = Label(main_window, text="Sistema Gerenciador de Banco de Dados", font=10)
presentation2.pack(pady=5)

#functions
def create_database():
    pass

def select_database():
    pass

def connect_database():
    pass

def import_from_csv():
    pass


#choose database
#Lista abaixo os database cadastrados
#quando clica aparece nova janela para fazer login no database
#depois do login, fecha segunda janela e abre a terceira com os dados do data base

#create new database (pode ser só um campo new, no choose database)
#Nova janela para preencher os campos: nome, host, user, password, etc
new_database = Button(main_window, text="Novo banco de dados", borderwidth=5, padx=15, pady=15, command=create_database)
new_database.pack(pady=10)
#fazer um for para criar um novo botão a cada database cadastrado
database_exemplo = Button(main_window, text="database exemplo", borderwidth=5, padx=15, pady=15, command=select_database)
database_exemplo.pack(pady=10)


#Connect to existent database
#nova janela para login e coisas necessárias
connect_to_database = Button(main_window, text="Conectar a um banco de dados", borderwidth=5, padx=15, pady=15, command=connect_database)
connect_to_database.pack(pady=10)

#Import data from CSV
#nova janela para informar/criar o database e informar o caminho do arquivo etc
import_from_csv = Button(main_window, text="Importar de um .csv", borderwidth=5, padx=15, pady=15, command=import_from_csv)
import_from_csv.pack(pady=10)
#-------------------------------------------------------

#dentro do database
#selecionar botão de criar tabela e as tabelas existentes listadas em botões
# Se criar tabela: aparece um text box já escrito CREATE TABLE para completar a query
# Se seleciona uma tabela existente, aparece um text box para realizar a query dentro daquela tabela
# Tem que aparecer o nome da tabela atual

#Depois de um select, abrir nova janela para exibir resultados









#Window loop
main_window.mainloop()