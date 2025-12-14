import pytest
from unittest.mock import patch, MagicMock
from Database.querys import insertar_documento, obtener_documentos, obtener_documento_por_id, actualizar_documento, eliminar_documento, obtener_procesos

@patch("Database.querys.crear_conexion")
def test_insertar_documento(mock_conexion):
    mock_cursor = MagicMock()
    mock_conexion.return_value.cursor.return_value = mock_cursor
    
    resultado = insertar_documento(
        Proceso = "Gestión Humana",
        CodigoDocumento = "GH-01",
        NombreDocumento = "Solicitud de Personal",
        Version = "01",
        Estado = "Vigente"

    )

    assert resultado is True

@patch("Database.querys.crear_conexion")
def test_obtener_documentos(mock_conexion):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conexion.return_value.cursor.return_value = mock_cursor

    resultado = obtener_documentos()
    
    assert resultado == []

@patch("Database.querys.crear_conexion")
def test_obtener_documentos_por_id(mock_conexion):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = None
    mock_conexion.return_value.cursor.return_value = mock_cursor

    with patch("Database.querys.crear_conexion", return_value = None):
        resultado = obtener_documento_por_id(1)
    
    assert resultado is None


def test_actualizar_documento():
    fake_conexion = MagicMock()
    fake_cursor = MagicMock()

    fake_conexion.cursor.return_value = fake_cursor
    fake_cursor.rowcount = 1

    with patch("Database.querys.crear_conexion", return_value = fake_conexion):
        resultado = actualizar_documento(
        id_doc= 1, 
        nuevo_Proceso = "Nuevo",
        )
    
    assert resultado is True


def test_eliminar_documento():
    fake_conexion = MagicMock()
    fake_cursor = MagicMock()

    fake_conexion.cursor.return_value = fake_cursor
    fake_cursor.rowcount = 1

    with patch("Database.querys.crear_conexion", return_value = fake_conexion):
        resultado = eliminar_documento(1)
    
    assert resultado is True

def test_obtener_proceso():
    fake_conexion = MagicMock()
    fake_cursor = MagicMock()

    fake_cursor.fetchall.return_value = [
        {"idProceso":1, "nombre": "Proceso 1"},
        {"idProceso":2, "nombre": "Proceso 2"}
    ]
    fake_conexion.cursor.return_value = fake_cursor

    with patch("Database.querys.crear_conexion", return_value = fake_conexion):
        resultado = obtener_procesos()

    assert resultado == [
        {"idProceso":1, "nombre": "Proceso 1"},
        {"idProceso":2, "nombre": "Proceso 2"}
    ]

   