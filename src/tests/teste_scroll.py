import tkinter as tk

def abrir_toplevel():
    toplevel = tk.Toplevel(root)

    # Adiciona um canvas ao TopLevel
    canvas = tk.Canvas(toplevel)
    canvas.pack(side="left", fill="both", expand=True)

    # Adiciona uma barra de rolagem lateral ao TopLevel
    scrollbar = tk.Scrollbar(toplevel, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Atualiza o método de rolagem do canvas para usar a barra de rolagem
    canvas.configure(yscrollcommand=scrollbar.set)

    # Adicione widgets ou qualquer conteúdo ao Canvas
    # Exemplo: rótulos com texto de exemplo
    for i in range(1, 21):
        label = tk.Label(canvas, text=f"Item {i}")
        canvas.create_window(0, i * 20, anchor="nw", window=label)

    # Configura o método de rolagem do canvas para se ajustar ao conteúdo
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Criação da janela principal
root = tk.Tk()

# Botão para abrir o TopLevel
btn_abrir_toplevel = tk.Button(root, text="Abrir TopLevel", command=abrir_toplevel)
btn_abrir_toplevel.pack(pady=10)

# Inicia o loop principal
root.mainloop()
