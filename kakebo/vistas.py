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

        # Obtener la fecha actual
        self.today = datetime.today()

        lbl_fecha = tk.Label(self, text=text, width=10, height=W)
        lbl_fecha.pack(side=tk.LEFT)

        #self.day_Var = tk.IntVar()
        validateDay = self.register(self.__validate_day)
        self.day_Var = tk.Entry(self, width=2, validate="key", validatecommand=(validateDay, "%P"))
        self.day_Var.pack(side=tk.LEFT)
        #self.day_Var.insert(0, f"{self.today.day:02d}")

        lbl_slash = tk.Label(self, text="/", width=3)
        lbl_slash.pack(side=tk.LEFT)

        #self.month_Var = tk.IntVar()
        validateMonth = self.register(self.__validate_mes)
        self.month_Var = tk.Entry(self,  width=2, state=tk.DISABLED, validate="key", validatecommand=(validateMonth, "%P"))
        self.month_Var.pack(side=tk.LEFT)
        #month_Var.insert(0, f"{self.today.month:02d}")

        lbl_slash = tk.Label(self, text="/", width=3)
        lbl_slash.pack(side=tk.LEFT)

        #self.year_Var = tk.IntVar()
        validateYear = self.register(self.__validate_year)
        self.year_Var = tk.Entry(self, width=4, state=tk.DISABLED, validate="key", validatecommand=(validateYear, "%P"))
        self.year_Var.pack(side=tk.LEFT)
        #year_Var.insert(0, str(self.today.year))
        
    def __validate_day(self, candidato):
        if not candidato.isdigit() and candidato != "":
            return False
        if candidato == "":
            self.month_Var.config(state=tk.DISABLED)
            return True
        if int(candidato) > 0 and int(candidato) < 32:
            self.month_Var.config(state=tk.NORMAL)
            return True
        else:
            return False
        
    def __validate_mes(self, candidato):
        if not candidato.isdigit() and candidato != "":
            return False
        if candidato == "":
            self.year_Var.config(state=tk.DISABLED)
            return True
        try:
            datetime(2000, int(candidato), int(self.day_Var.get()))
            self.year_Var.config(state=tk.NORMAL)
            return True
        except ValueError:
            return False

    def __validate_year(self, candidato):
        if not candidato.isdigit() and candidato != "":
            return False
        if len(candidato) < 4:
            return True
        try:
            datetime(int(candidato), int(self.month_Var.get()), int(self.day_Var.get()))
            return True
        except ValueError:
            return False