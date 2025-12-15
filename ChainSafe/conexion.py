import mysql.connector

def crear_conexion():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="sgcs"
        )
    except mysql.connector.Error as e:
        print("Error de conexión a MySQL:", e)
        return None
