import tkinter as tk
from tkinter import ttk
from datetime import datetime
from kakebo import WIDTH, PAD_DEFAULT
from kakebo.modelos import CategoriaGastos

class Input(tk.Frame):
    def __init__(self, parent, label_text, W, H):
        super().__init__(parent,  width=W, height=H)
        self.pack_propagate(False)
        lbl = tk.Label(self, text=label_text, anchor=tk.W, width=10)
        lbl.pack(side=tk.LEFT)
        
        self.inp = tk.Entry(self)
        self.inp.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def bind(self, event_type, callback):
        self.inp.bind(event_type, callback)

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
        try:
            datetime(2000, 1, int(candidato))
            self.month_Var.config(state=tk.NORMAL)
            return True
        except ValueError:
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

class NumerInput(Input):
    def __init__(self, parent, labelText, W, H):
        super().__init__(parent, labelText, W, H)
        
        validate_Input = self.register(self.__validate_Input)
        self.inp.config(validate="key", validatecommand=(validate_Input, "%P"))

    def __validate_Input(self, candidato):
        if candidato == "" or candidato == "-":
            return True

        try:
            float(candidato)
            return True
        except ValueError:
            return False
    
    @property
    def value(self):
        if self.inp.get() == "" or self.inp.get() == "-":
            return None
        else:
            return float(self.inp.get())

class SelectInput(tk.Frame):
    def __init__(self, parent, label_text, W, H, options):
        super().__init__(parent,  width=W, height=H)
        self.pack_propagate(False)

        tk.Label(self, text=label_text, anchor=tk.W, width=10).pack(side=tk.LEFT)

        self.selected = tk.StringVar()
        
        valores_op = []
        for cadena in options:
            valores_op.append(cadena.name)

        self.combo_box = ttk.Combobox(self, values=valores_op, textvariable=self.selected, state="readonly")
        self.combo_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

class FormMovimiento(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=WIDTH, height=250, padx=PAD_DEFAULT, pady=PAD_DEFAULT)
        self.pack_propagate(False)
        
        self.fecha = DateInput(self, WIDTH, 40)
        self.fecha.pack(side=tk.TOP)

        self.concepto = Input(self, "Concepto:", WIDTH, 30)
        self.concepto.pack(side=tk.TOP)

        self.cantidad = NumerInput(self, "Cantidad:", WIDTH, 30)
        self.cantidad.pack(side=tk.TOP)
        self.cantidad.bind("<Key>", self.__control_categoria)

        self.categoria = SelectInput(self, "Categoria:", WIDTH, 40, CategoriaGastos)
        self.categoria.pack(side=tk.TOP)

        fr = tk.Frame(self, pady=PAD_DEFAULT)
        fr.pack(side=tk.TOP, expand=True, fill=tk.X)

        self.btn_save = tk.Button(fr, text="Save")
        self.btn_save.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        btn_cancel = tk.Button(fr, text="Cancel")
        btn_cancel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def __control_categoria(self, ev):
        print(self.cantidad.value)