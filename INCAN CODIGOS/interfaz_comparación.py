import tkinter as tk

root = tk.Tk()
root.title("Comparación")
root.geometry("500x300")

label = tk.Label(root, text="Hola, mundo!")
label.pack()

button = tk.Button(root, text="Click me!", command= lambda: print("Botón clicado"))
button.pack()


button2 = tk.Button(root, text="No!", command= lambda: print("No"))
button2.pack()

root.mainloop()