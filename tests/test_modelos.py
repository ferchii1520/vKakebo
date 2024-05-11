from datetime import date
from kakebo.modelos import Ingreso, CategoriaGastos, Gasto
import pytest

def test_instanciar_ingresos():
    movimiento = Ingreso("Loteria del nino, premio", date(2024, 1, 5), 1000)

    assert movimiento.concepto == "Loteria del nino, premio"
    assert movimiento.fecha == date(2024, 1, 5)
    assert movimiento.cantidad == 1000

def test_ingreso_concepto_string():
    with pytest.raises(TypeError):
        movimiento = Ingreso(19, date(2024, 1, 5), 1000)

def test_ingreso_fecha_typeError():
    with pytest.raises(TypeError):
        movimiento = Ingreso("Indiferente", "1 de enero de 2024", "0")
    
    movimiento = Ingreso("Indiferente", date(2024, 1, 5), 5)
    movimiento = Ingreso("Indiferente", date(2024, 1, 5), 5.2)

def test_concepto_vacio():
    with pytest.raises(ValueError):
        movimiento = Ingreso("", date(2024, 12, 5), 5)

def test_concepto_menor_5():
    with pytest.raises(ValueError):
        movimiento = Ingreso("Hi", date(2024, 12, 5), 8)

def test_fecha_posterior_Hoy():
    with pytest.raises(ValueError):
        movimiento = Ingreso("Loteria", date(2025, 12, 5), 89)

def test_cantidad_no_negativo():
    with pytest.raises(ValueError):
        movimiento = Ingreso("Loteria", date.today(), -8)

def test_crear_gasto():
    movimiento = Gasto("Factura del Agua", date(2024, 5, 1), 70, CategoriaGastos.NECESIDAD)
    assert movimiento.concepto == "Factura del Agua"
    assert movimiento.fecha == date(2024, 5, 1)
    assert movimiento.cantidad == 70
    assert movimiento.categoria == CategoriaGastos.NECESIDAD

def test_gasto_categoria_tipo_correcto():
    with pytest.raises(TypeError):
        movimiento = Gasto("Factura del Agua", date(2024, 5, 1), 70, "Necesidad")