"""
1. Crear un dao y comprobar
    1.1 Tiene una ruta de fichero fijado a un fichero csv
    1.2 El fichero csv tiene que ser vacio pero tener encabezados
2. Guardar un ingreso y un gasto
    2.1 El fichero contiene las filas adecuadas, una de cabecera, una de ingreso y una de gasto
3. Leer datos del fichero con un dao
    3.1 Preparar un fichero con datos
    3.2 Leer esos datos con el dao
    3.3 Comprobar que nos ha creado tantos movimientos como haya creado
"""
from kakebo.modelos import Dao_CSV, Ingreso, Gasto, CategoriaGastos, DaoSqlite
from datetime import date
import os
import sqlite3

ruta_Sqlite = "datos/movimientos_test.db"

def borrar_fichero(path):
    if os.path.exists(path):
        os.remove(path)

def borrar_movimientos_sqlite():
    con = sqlite3.connect(ruta_Sqlite)
    cur = con.cursor()

    query = "DELETE FROM movimientos;"
    cur.execute(query)
    con.commit()
    con.close()

def test_crear_dao_csv():
    ruta = "datos/test_movimientos.csv"
    borrar_fichero(ruta)
    dao = Dao_CSV(ruta)
    assert dao.ruta == ruta

    with  open(ruta, "r") as f:
        cabecera = f.readline()
        assert cabecera == "concepto,fecha,cantidad,categoria\n"
        registro = f.readline()
        assert registro == ""

def test_guardar_Ingreso_Gasto():
    ruta = "datos/test_movimientos.csv"
    borrar_fichero(ruta)
    dao = Dao_CSV(ruta)
    
    ing = Ingreso("Un ingreso", date(1999, 12, 31), 100)
    dao.grabar(ing)

    gas = Gasto("pizza", date(2000, 1, 1), 150, CategoriaGastos.EXTRAS)
    dao.grabar(gas)

    with open(ruta, "r") as f:
        cabecera = f.readline()
        ingreso = f.readline()
        assert ingreso == "Un ingreso,1999-12-31,100,\n"
        registro = f.readline()
        assert registro == "pizza,2000-01-01,150,4\n"
        registro = f.readline()
        assert registro == ""

def test_leer_Ingreso_Gasto():
    ruta = "datos/test_movimientos.csv"
    with open(ruta, "w", newline="") as f:
        f.write("concepto,fecha,cantidad,categoria\n")
        f.write("La luz,2020-04-02,1000.50,\n")
        f.write("Sushi,2024-05-10,350.20,1\n")
    
    dao = Dao_CSV(ruta)

    movimiento1 = dao.leer()
    assert movimiento1 == Ingreso("La luz", date(2020, 4, 2), 1000.50)

    movimiento2 = dao.leer()
    assert movimiento2 == Gasto("Sushi", date(2024, 5, 10), 350.20, CategoriaGastos.NECESIDAD)

    movimiento3 = dao.leer()
    assert movimiento3 is None

def test_crear_dao_sqlite():
    ruta = ruta_Sqlite
    dao = DaoSqlite(ruta)

    assert dao.ruta == ruta

def test_leer_dao_sqlite():
    borrar_movimientos_sqlite()
    con = sqlite3.connect(ruta_Sqlite)
    cur = con.cursor()

    query = """
        INSERT INTO movimientos (id, tipo_movimiento, concepto, fecha, cantidad, categoria)
            VALUES(?, ?, ?, ?, ?, ?)
        """
    
    cur.executemany(query, [(1, "I", "Un ingreso", date(2024, 5, 14), 100, None), 
                        (2, "G", "Un gasto", date(2024, 5, 1), 123, 3)])
    
    con.commit()
    con.close()

    dao = DaoSqlite(ruta_Sqlite)

    movimiento = dao.leer(1)
    assert movimiento == Ingreso("Un ingreso", date(2024, 5, 14), 100)

    movimiento = dao.leer(2)
    assert movimiento == Gasto("Un gasto", date(2024, 5, 1), 123, CategoriaGastos.OCIO_VICIO)

def test_grabar_sqlite():
    borrar_movimientos_sqlite()

    ing = Ingreso("Venta carro", date(2024, 5, 4), 123)
    dao = DaoSqlite(ruta_Sqlite)
    dao.grabar(ing)

    con = sqlite3.connect(ruta_Sqlite)
    cur = con.cursor()

    query = """
        SELECT id, tipo_movimiento, concepto, fecha, cantidad, categoria
            FROM movimientos
            ORDER BY id DESC LIMIT 1
        """
    res = cur.execute(query)
    fila = res.fetchone()
    con.close()

    assert fila[1] == "I"
    assert fila[2] == "Venta carro"
    assert fila[3] == "2024-05-04"
    assert fila[4] == 123.0
    assert fila[5] is None

def test_update_sqlite():
    borrar_movimientos_sqlite()
    
    con = sqlite3.connect(ruta_Sqlite)
    cur = con.cursor()
    
    query = """
            INSERT INTO movimientos (id, tipo_movimiento, concepto, fecha, cantidad)
                VALUES (1,'I', 'Concepto original', '0001-01-01', 0.1)
            """
    
    cur.execute(query)
    con.commit()
    con.close()
    
    dao = DaoSqlite(ruta_Sqlite)
    
    movimiento = dao.leer(1)
    movimiento.concepto = "Concepto cambiado"
    movimiento.fecha = date(2024, 1, 4)
    movimiento.cantidad = 32
    
    dao.grabar(movimiento)
    
    # Comprobar la modificacion
    
    modificado = dao.leer(1)
    
    assert isinstance(modificado, Ingreso)
    assert modificado.concepto == "Concepto cambiado"
    assert modificado.fecha == date(2024, 1, 4)
    assert modificado.cantidad == 32.0