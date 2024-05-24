import tkinter as tk
from datetime import datetime

class Input(tk.Frame):
    def __init__(self, parent, label_text, W, H):
        super().__init__(parent,  width=W, height=H)
        self.pack_propagate(False)
        lbl = tk.Label(self, text=label_text, anchor=tk.NW)
        lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.var = tk.StringVar()
        inp = tk.Entry(self, textvariable=self.var)
        inp.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        btn_action = tk.Button(self, text="Enter", command=self.el_comando)
        btn_action.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def el_comando(self):
        print(self.var_fecha.get())

class DateInput(tk.Frame):
    def __init__(self, parent, W, H, text="Fecha:"):
        super().__init__(parent,  width=W, height=H)
        self.pack_propagate(False)

        lbl_fecha = tk.Label(self, text=text, width=10, height=W)
        lbl_fecha.pack(side=tk.LEFT)

        self.day_Var = tk.IntVar()
        day_Var = tk.Entry(self, textvariable=self.day_Var, width=2)
        day_Var.pack(side=tk.LEFT)
        self.day_Var.set("dd")

        lbl_slash = tk.Label(self, text="/", width=3)
        lbl_slash.pack(side=tk.LEFT)

        self.month_Var = tk.IntVar()
        mont_Var = tk.Entry(self, textvariable=self.month_Var, width=2)
        mont_Var.pack(side=tk.LEFT)
        self.month_Var.set("mm")

        lbl_slash = tk.Label(self, text="/", width=3)
        lbl_slash.pack(side=tk.LEFT)

        self.year_Var = tk.IntVar()
        year_Var = tk.Entry(self, textvariable=self.year_Var, width=4)
        year_Var.pack(side=tk.LEFT)

        # Obtener la fecha actual
        today = datetime.today()
        
        # Establecer los valores de las variables con la fecha actual
        self.day_Var.set(today.day)
        self.month_Var.set(today.month)
        self.year_Var.set(today.year)