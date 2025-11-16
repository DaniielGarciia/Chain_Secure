from Conexion import crear_conexion

# crear documento
def insertar_documento(Proceso,CodigoDocumento,NombreDocumento,Version,Estado):
    Conexion = crear_conexion()
    if not Conexion:
        print("❌ No se pudo conectar a la base de datos.")
        return None
    try:
        cursor = Conexion.cursor()
        sql = """
            INSERT INTO listadomaestro (Proceso, CodigoDocumento, NombreDocumento, Version, Estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (Proceso, CodigoDocumento, NombreDocumento, Version, Estado)
        cursor.execute(sql,valores)
        Conexion.commit()
        print("Documento registrado exitosamente")
    except Exception as e:
        print("Se produjo un error", e)
    finally:
        cursor.close()
        Conexion.close()

# Read (obtener los documentos)
def obtener_documentos():
    Conexion = crear_conexion()
    if not Conexion:
        print("❌ No se pudo conectar a la base de datos.")
        return []
    try:
        cursor = Conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM listadomaestro ORDER BY id DESC")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print("Error al obtener documentos:", e)
        return []
    finally:
        cursor.close()
        Conexion.close()

#READ (Obtener los documentos por Id)
def obtener_documento_por_id(id_doc):
    Conexion = crear_conexion()
    if not Conexion:
        print("❌ No se pudo conectar a la base de datos.")
        return None
    try:
        cursor = Conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM listadomaestro WHERE id = %s", (id_doc,))
        resultado = cursor.fetchone()
        return resultado
    except Exception as e:
        print("Error al obtener documento:", e)
        return None
    finally:
        cursor.close()
        Conexion.close()

#UPDATE (actualizar los documentos)
def actualizar_documento(id_doc, nuevo_Proceso=None, nuevo_Codigo=None, nuevo_Nombre=None, nueva_Version=None, nuevo_Estado=None):
    Conexion = crear_conexion()
    if not Conexion:
        print("❌ No se pudo conectar a la base de datos.")
        return False
    try:
        cursor = Conexion.cursor()
        
        campos = []
        valores = []

        if nuevo_Proceso:
            campos.append("Proceso = %s")
            valores.append(nuevo_Proceso)
        if nuevo_Codigo:
            campos.append("CodigoDocumento = %s")
            valores.append(nuevo_Codigo)
        if nuevo_Nombre:
            campos.append("NombreDocumento = %s")
            valores.append(nuevo_Nombre)
        if nueva_Version:
            campos.append("Version = %s")
            valores.append(nueva_Version)
        if nuevo_Estado:
            campos.append("estado = %s")
            valores.append(nuevo_Estado)

        if not campos:
            print("⚠️ No se proporcionaron campos para actualizar.")
            return False
        
        sql = f"UPDATE listadomaestro SET {', '.join(campos)} WHERE id = %s"
        valores.append(id_doc)

        cursor.execute(sql, tuple(valores))
        Conexion.commit()

        if cursor.rowcount:
            print("✏️ Documento actualizado correctamente.")
            return True
        else:
            print("⚠️ No se encontró el documento especificado.")
            return False
    except Exception as e:
        print("Error al actualizar documento:", e)
        return False
    finally:
        cursor.close()
        Conexion.close()

#DELETE (Eliminar el documento)
def eliminar_documento(id_doc):
    Conexion = crear_conexion()
    if not Conexion:
        print("❌ No se pudo conectar a la base de datos.")
        return False
    try:
        cursor = Conexion.cursor()
        cursor.execute("DELETE FROM listadomaestro WHERE id = %s", (id_doc,))
        Conexion.commit()
        if cursor.rowcount:
            print("🗑️ Documento eliminado correctamente.")
            return True
        else:
            print("⚠️ No se encontró el documento a eliminar.")
            return False
    except Exception as e:
        print("Error al eliminar documento:", e)
        return False
    finally:
        cursor.close()
        Conexion.close()    

#Crear la función para obtener los procesos
def obtener_procesos():
    Conexion = crear_conexion()
    if not Conexion:
        print("❌ No se puede conectar a la base de datos")
        return False
    try:
        cursor = Conexion.cursor()
        cursor.execute("SELECT * FROM proceso ORDER BY idProceso ASC")
        resultados = cursor.fetchall()
    except Exception as e:
        print("Error al obtener procesos:", e)
        return []
    finally:
        cursor.close()
        Conexion.close()



    





        