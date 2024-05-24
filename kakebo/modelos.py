from datetime import date
from enum import Enum
import csv, os, sqlite3

class Movimiento:
    def __init__(self, concepto, fecha, cantidad, id = None):
        self.concepto = concepto
        self.fecha = fecha
        self.cantidad = cantidad
        self.id = id
        self.validar_tipos()
    
    def validar_tipos(self):
        if not isinstance(self.concepto, str):
            raise TypeError("Concepto debe ser cadena de texto")
        if len(self.concepto) < 5:
            raise ValueError("El concepto no puede estar vacio, o ser menor de 5 caracteres")
        if not isinstance(self.fecha, date):
            raise TypeError("La fecha debe estar en formato (yyyy,mm,dd)")
        if self.fecha > date.today():
            raise ValueError("La fecha no puede ser posterior al dia de hoy")
        if not (isinstance(self.cantidad, int) or isinstance(self.cantidad, float)):
            raise TypeError("La cantidad debe ser entero o decimal")
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe no debe ser 0 o menor")
        
    def __repr__(self):
        return f"IMovimiento: {self.fecha} {self.concepto} {self.cantidad:.2f}"

class Ingreso(Movimiento):
    def __repr__(self, other):
        return f"Ingreso: {self.fecha} {self.concepto} {self.cantidad:.2f}"
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.concepto == other.concepto and self.cantidad == other.cantidad and self.fecha == other.fecha

class Gasto(Movimiento):
    def __init__(self, concepto, fecha, cantidad, categoria, id = None):
        super().__init__(concepto, fecha, cantidad, id)
        self.categoria = categoria
        self.validar_categoria()
        
    def validar_categoria(self):
        if not isinstance(self.categoria, CategoriaGastos):
            raise TypeError("Categoria debe ser CategoriaGastos")

    def __repr__(self):
        return f"Gasto ({self.categoria.name}): {self.fecha} {self.concepto} {self.cantidad:.2f}"
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.concepto == other.concepto and self.cantidad == other.cantidad and self.fecha == other.fecha and self.categoria == other.categoria

class CategoriaGastos(Enum):
    NECESIDAD = 1
    CULTURA = 2
    OCIO_VICIO = 3
    EXTRAS = 4

class Dao_CSV:
    def __init__(self, ruta):
        self.ruta = ruta
        if not os.path.exists(self.ruta):
            with open(self.ruta, "w", newline="") as f:
                f.write("concepto,fecha,cantidad,categoria\n")
        self.puntero_lectura = 0

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
            contador = 0
            for row in reader:
                if row['categoria'] == "":
                    variable = Ingreso(row['concepto'], date.fromisoformat(row['fecha']), float(row['cantidad']))
                else:
                    variable = Gasto(row["concepto"], date.fromisoformat(row["fecha"]), float(row["cantidad"]), CategoriaGastos(int(row["categoria"])))
                
                if contador == self.puntero_lectura:
                    self.puntero_lectura += 1
                    return variable
                contador += 1
            return None

class DaoSqlite:
    def __init__(self, ruta):
        self.ruta = ruta

    def leer(self, id):
        con = sqlite3.connect(self.ruta)
        cur = con.cursor()

        query = """
                    SELECT id, tipo_movimiento, concepto, fecha, cantidad, categoria
                        FROM movimientos
                        WHERE id = ?
                """

        res = cur.execute(query, (id,))
        valores = res.fetchone()
        con.close()

        if valores:
            if valores[1] == "I":
                return Ingreso(valores[2], date.fromisoformat(valores[3]), valores[4], valores[0])
            elif valores[1] == "G":
                return Gasto(valores[2], date.fromisoformat(valores[3]), valores[4], CategoriaGastos(valores[5]), valores[0])
        return None
    
    def grabar(self, movimiento):
        con = sqlite3.connect(self.ruta)
        cur = con.cursor()

        if isinstance(movimiento, Ingreso):
            tipo_mov = "I"
            categoria = None
        elif isinstance(movimiento, Gasto):
            tipo_mov = "G"
            categoria = movimiento.categoria.value

        if movimiento.id is None:
            query = """
                        INSERT INTO movimientos (tipo_movimiento, concepto, fecha, cantidad, categoria)
                            VALUES (?, ?, ?, ?, ?)
                    """
            cur.execute(query, (tipo_mov, movimiento.concepto, movimiento.fecha, movimiento.cantidad, categoria))
        else:
            query = """
                        UPDATE movimientos set concepto = ?, fecha = ?, cantidad = ?, categoria = ?
                            WHERE id = ?
                    """
            cur.execute(query,(movimiento.concepto, movimiento.fecha, movimiento.cantidad, categoria, movimiento.id))

        con.commit()
        con.close()

    def borrar(self, id):
        con = sqlite3.connect(self.ruta)
        cur = con.cursor()
        
        query = "DELETE FROM movimientos where id = ?"
        
        cur.execute(query, (id,))
        con.commit()
        con.close()

    def leerTodo(self):
        con = sqlite3.connect(self.ruta)
        cur = con.cursor()

        query = """
                    SELECT id, tipo_movimiento, concepto, fecha, cantidad, categoria
                        FROM movimientos
                """
        
        res = cur.execute(query)
        valores = res.fetchall() # para coger de la base de datos 
        con.close()
        
        lista_completa= []
        for valor in valores :
            if valor[1] == "I":
                lista_completa.append(Ingreso(valor[2], date.fromisoformat(valor[3]), valor[4], valor[0]))
                
            elif valor[1] == "G":
                lista_completa.append(Gasto(valor[2], date.fromisoformat(valor[3]), valor[4], CategoriaGastos(valor[5]), valores[0]))
                
        return lista_completa
    