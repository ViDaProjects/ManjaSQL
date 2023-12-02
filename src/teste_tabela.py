import tkinter as tk
from tkinter import ttk

def preencher_tabela(tree):
    # Adicione os dados à tabela
    # Aqui, estou usando dados fictícios como exemplo
    data = [
        ("João", "Silva", "25"),
        ("Maria", "Santos", "30"),
        ("Carlos", "Oliveira", "22")
    ]

    for item in data:
        tree.insert("", "end", values=item)

# Criar a janela principal
root = tk.Tk()
root.title("Exemplo de Tabela")

# Criar Treeview
tree = ttk.Treeview(root, columns=("Nome", "Sobrenome", "Idade"), show="headings")

# Configurar os cabeçalhos da tabela
tree.heading("Nome", text="Nome")
tree.heading("Sobrenome", text="Sobrenome")
tree.heading("Idade", text="Idade")

# Configurar as colunas
tree.column("Nome", anchor="center", width=100)
tree.column("Sobrenome", anchor="center", width=100)
tree.column("Idade", anchor="center", width=100)

# Preencher a tabela com dados
preencher_tabela(tree)

# Colocar a tabela na janela
tree.pack()

# Iniciar o loop principal
root.mainloop()
