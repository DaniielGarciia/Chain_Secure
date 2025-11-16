import mysql.connector

def crear_conexion():

    try:

        conexion = mysql.connector.connect(user='root', password='admin',
                                   host='localhost',
                                   database='sgcs',
                                   port='3306')
        print(conexion)

        return conexion
    except mysql.connector.Error as e:
        print("Error al conectar")
        return None
    
    
    if conexion.is_connected():
                print("✅ Conexión exitosa a la base de datos SGCS")



 