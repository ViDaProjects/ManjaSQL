from tkinter import *

root = Tk()
root.title("ManjaSQL")
root.geometry("800x850")
#Simbolo da janela
#root.iconbitmap('caminho pra imagem')

#creating a label widget
myLabel1 = Label(root, text="Hello World Again")
myLabel2 = Label(root, text="My name is Viviane")

#shoving it onto the screen

#myLabel1.grid(row=1, column=0)
#myLabel2.grid(row=2, column=1)


def myClick():
    myLabel = Label(root, text="Hello " + e.get())
    myLabel.pack()
    #fechar a janela top.destroy
    top = Toplevel()
    top.title("My second window")
    myLabel3 = Label(top, text="Hello " + e.get())
    myLabel3.pack()    


e = Entry(root, width=50)
e.pack()
#Essa msg nao apaga quando envia
e.insert(0, "Enter your name: ")

#creating buttons
myButton = Button(root, text="Send", padx=50, pady=50, command=myClick)
#obs: state=DISABLED
myButton.pack()

#TEXT BOXXX
my_text = Text(root, width=60, height=20)
my_text.pack(pady=20)

def clear():
    my_text.delete(1.0,END)

def get_text():
    #linha 1.0 até a linha final
    text_Label.config(text=my_text.get(1.0, END))

button_frame = Frame(root)
button_frame.pack()

clear_button = Button(button_frame, text="Clear text box", command=clear)
clear_button.pack()

get_text_button = Button(button_frame, text="Get text", command=get_text)
get_text_button.pack()

text_Label = Label(root, text=" ")
text_Label.pack()

button_quit = Button(root, text="Exit program", command= root.quit)
button_quit.pack()

#Window loop
root.mainloop()