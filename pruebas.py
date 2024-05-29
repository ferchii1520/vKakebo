import tkinter as tk
from tkinter import ttk
from kakebo.vistas import FormMovimiento

root = tk.Tk() #Crear la ventana de tk

form = FormMovimiento(root)
form.pack(side=tk.TOP)
    
root.mainloop() #Para que salga la ventana