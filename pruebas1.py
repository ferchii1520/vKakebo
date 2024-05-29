import tkinter as tk
from tkinter import ttk
from kakebo.vistas import Input, DateInput, FormMovimiento

root = tk.Tk() #Crear la ventana de tk
root.pack_propagate(False) #Para que la ventana no se extienda o se redusca dependiendo el marco
marco = tk.Frame(root, width=200, height=80, background="red") #Creamos el marco
#marco.pack(side=tk.TOP, expand=True, fill="both") #Empaquetamos el marco para que se pueda ver en la ventana
marco.pack() #Empaquetamos el marco para que se pueda ver en la ventana
#marco.pack_propagate(False)#Para que el marco no se extienda o se redusca dependiendo el marco
lbl_fecha = tk.Label(marco, text="Fecha:", anchor=tk.NW) #Creamos la label
lbl_fecha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) #Empaquetamos la label para que se pueda ver en la ventana
var_fecha = tk.StringVar() #Tenemos que poner el tipo de variable que se va a guardar en el input
inp_fecha = tk.Entry(marco, textvariable=var_fecha) #Ponemos el Entry
inp_fecha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) #Empaquetamos el entry para que se pueda ver en la ventana

i1 = Input(root, "Primer Input", 300, 60)
i1.pack(side=tk.TOP)

i2 = Input(root, "Segundo Input", 310, 60)
i2.pack(side=tk.TOP)

di = DateInput(root, 250, 35)
di.pack(side=tk.TOP)

root.mainloop() #Para que salga la ventana