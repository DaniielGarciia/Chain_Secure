from Controllers.documento_controller import registrar_documento_interactivo, editar_documento_interactivo
import pytest
from unittest.mock import patch, MagicMock


@patch("Database.querys.crear_conexion")
def test_registrar_documento_interactivo (mock_conexion):
    mock_cursor = MagicMock()
    mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    controlador = registrar_documento_interactivo()

    resultado_insert = controlador.insertar_documento(
        Proceso = "Gestión Humana",
        CodigoDocumento = "GH-01",
        NombreDocumento = "Solicitud de Personal",
        Version = "01",
        Estado = "Vigente"
    )
    assert resultado_insert is True

    mock_cursor.execute.assert_called_once()
    mock_conexion.return_value.commit.assert_called_once()

    documentos_simul =[("GH-01","Solicitud de Personal", "Vigente")]
    mock_cursor.fetchall.return_value = documentos_simul

    resultado = controlador.obtener_documentos()

    assert resultado == documentos_simul

    mock_conexion.return_value.close.assert_called_once()

@patch("Database.querys.crear_conexion")
def test_editar_documento_interactivo (mock_conexion):
    mock_cursor = MagicMock()
    mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = None

    editor = editar_documento_interactivo()

    with patch("Database.querys.crear_conexion", return_value = None):
        resultado_obt = editar_documento_interactivo.obtener_documento_por_id(1)
    
    assert resultado_obt is None

    fake_conexion = MagicMock()
    fake_cursor = MagicMock()

    fake_conexion.cursor.return_value = fake_cursor
    fake_cursor.rowcount = 1

    with patch("Database.querys.crear_conexion", return_value = fake_conexion):
         resultado = editar_documento_interactivo.actualizar_documento(
        id_doc= 1, 
        nuevo_Proceso = "Nuevo",
        )
    
    assert resultado is True