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
from kakebo.modelos import Dao, Ingreso, Gasto, CategoriaGastos
from datetime import date

def test_crear_dao():
    ruta = "datos/test_movimientos.csv"
    dao = Dao(ruta)
    assert dao.ruta == ruta

    with  open(ruta, "r") as f:
        cabecera = f.readline()
        assert cabecera == "concepto,fecha,cantidad,categoria\n"
        registro = f.readline()
        assert registro == ""

def test_guardar_Ingreso_Gasto():
    ruta = "datos/test_movimientos.csv"
    dao = Dao(ruta)
    
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
    
    dao = Dao(ruta)

    movimiento1 = dao.leer()
    assert movimiento1 == Ingreso("La luz", date(2020, 4, 2), 1000.50)

    movimiento2 = dao.leer()
    assert movimiento2 == Gasto("Sushi", date(2024, 5, 10), 350.20, CategoriaGastos.NECESIDAD)

    movimiento3 = dao.leer()
    assert movimiento3 is None
