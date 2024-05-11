from datetime import date
from enum import Enum
import csv
import os

class Movimiento:
    def __init__(self, concepto, fecha, cantidad):
        self.concepto = concepto
        self.fecha = fecha
        self.cantidad = cantidad
        self.validar_tipos()
    
    def validar_tipos(self):
        if not isinstance(self.concepto, str):
            raise TypeError("Concepto debe ser cadena de texto")
        if len(self.concepto) < 5:
            raise ValueError("El concepto no puede estar vacio, o ser menor de 5 caracteres")
        if not isinstance(self.fecha, date):
            raise TypeError("Lafecha debe estar en formato (yyyy,mm,dd)")
        if self.fecha > date.today():
            raise ValueError("La fecha no puede ser posterior al dia de hoy")
        if not (isinstance(self.cantidad, int) or isinstance(self.cantidad, float)):
            raise TypeError("La cantidad debe ser entero o decimal")
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe no debe ser 0 o menor")
        
    def __repr__(self):
        return f"IMovimiento: {self.fecha} {self.concepto} {self.cantidad:.2f}"

class Ingreso(Movimiento):
    def __repr__(self):
        return f"Ingreso: {self.fecha} {self.concepto} {self.cantidad:.2f}"

class Gasto(Movimiento):
    def __init__(self, concepto, fecha, cantidad, categoria):
        super().__init__(concepto, fecha, cantidad)
        self.categoria = categoria
        self.validar_categoria()
        
    def validar_categoria(self):
        if not isinstance(self.categoria, CategoriaGastos):
            raise TypeError("Categoria debe ser CategoriaGastos")

    def __repr__(self):
        return f"Gasto ({self.categoria.name}): {self.fecha} {self.concepto} {self.cantidad:.2f}"

class CategoriaGastos(Enum):
    NECESIDAD = 1
    CULTURA = 2
    OCIO_VICIO = 3
    EXTRAS = 4

class Dao:
    def __init__(self, ruta):
        self.ruta = ruta
        if not os.path.exists(self.ruta):
            with open(self.ruta, "w", newline="") as f:
                f.write("concepto,fecha,cantidad,categoria\n")

    def grabar(self, movimiento):
        with open(self.ruta, "a", newline="") as f:
            writer = csv.writer(f, delimiter=",", quotechar='"')
            if isinstance(movimiento, Ingreso):
                #f.write(f"{movimiento.concepto},{movimiento.fecha},{movimiento.cantidad},\n") #Sin usar libreria csv
                writer.writerow([movimiento.concepto,movimiento.fecha,movimiento.cantidad,""])
            elif isinstance(movimiento, Gasto):
                writer.writerow([movimiento.concepto,movimiento.fecha,movimiento.cantidad,movimiento.categoria.value])
                #f.write(f"{movimiento.concepto},{movimiento.fecha},{movimiento.cantidad},{movimiento.categoria.value}\n") #Sin usar libreria csv
    
    def leer(self):
        with open(self.ruta, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['categoria'] == "":
                    variable = Ingreso(row['concepto'], date.fromisoformat(row['fecha']), float(row['cantidad']))
                else:
                    variable = Gasto(row["concepto"], date.fromisoformat(row["fecha"]), float(row["cantidad"]), CategoriaGastos(int(row["categoria"])))
                return variable
