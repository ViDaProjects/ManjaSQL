import tkinter as tk

def create_scrolls():
    global canvas 
    window = query_results_window
    # Adiciona um canvas ao TopLevel
    canvas = tk.Canvas(window)
    canvas.pack(side="left", fill="both", expand=True)

    # Adiciona uma barra de rolagem lateral ao TopLevel
    scrollbar_y = tk.Scrollbar(window, command=canvas.yview)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x = tk.Scrollbar(window, command=canvas.xview)
    scrollbar_x.pack(side="bottom", fill="x")

    # Atualiza o método de rolagem do canvas para usar a barra de rolagem
    canvas.configure(yscrollcommand=scrollbar_y.set)
    canvas.configure(xscrollcommand=scrollbar_x.set)

    # Adicione widgets ou qualquer conteúdo ao Canvas
    # Exemplo: rótulos com texto de exemplo
    '''for i in range(1, 21):
        label = tk.Label(canvas, text=f"Item {i}")
        canvas.create_window(0, i * 20, anchor="nw", window=label)
'''
    # Configura o método de rolagem do canvas para se ajustar ao conteúdo
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
