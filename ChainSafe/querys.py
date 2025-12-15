"""
Módulo de consultas a la base de datos para ChainSecure
Contiene todas las funciones CRUD para usuarios, documentos y procesos
"""

from conexion import crear_conexion
from datetime import datetime

# ===================== FUNCIONES DE USUARIOS =====================

def obtener_usuarios():
    """Obtiene todos los usuarios activos"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id, u.nombres, u.apellidos, u.email, u.usuario, 
                   r.nombre as rol, u.activo, u.fecha_creacion
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            WHERE u.activo = 1
            ORDER BY u.fecha_creacion DESC
        """)
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def obtener_roles():
    """Obtiene todos los roles disponibles"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre FROM roles ORDER BY id")
        roles = cursor.fetchall()
        cursor.close()
        conexion.close()
        return roles
    except Exception as e:
        print(f"Error al obtener roles: {e}")
        return []

def inactivar_usuario(usuario_id):
    """Inactiva un usuario en lugar de eliminarlo"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET activo = 0 WHERE id = %s", (usuario_id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al inactivar usuario: {e}")
        return False

# ===================== FUNCIONES DE DOCUMENTOS =====================

def obtener_procesos():
    """Obtiene todos los procesos disponibles"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id as idProceso, nombre FROM procesos ORDER BY nombre")
        procesos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return procesos
    except Exception as e:
        print(f"Error al obtener procesos: {e}")
        return []

def insertar_documento(proceso, codigo_documento, nombre_documento, version, estado):
    """Inserta un nuevo documento en la base de datos"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            INSERT INTO listadomaestro 
            (codigo, nombre_documento, version, estado, fecha_creacion, responsable)
            VALUES (%s, %s, %s, %s, %s, 1)
        """, (codigo_documento, nombre_documento, version, estado, fecha_actual))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al insertar documento: {e}")
        return False

def obtener_documentos():
    """Obtiene todos los documentos del listado maestro"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, codigo, nombre_documento, version, estado, 
                   fecha_creacion, fecha_vencimiento
            FROM listadomaestro
            ORDER BY fecha_creacion DESC
        """)
        documentos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return documentos
    except Exception as e:
        print(f"Error al obtener documentos: {e}")
        return []

def obtener_documento_por_id(documento_id):
    """Obtiene un documento específico por su ID"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, codigo, nombre_documento, version, estado, 
                   fecha_creacion, fecha_vencimiento
            FROM listadomaestro
            WHERE id = %s
        """, (documento_id,))
        documento = cursor.fetchone()
        cursor.close()
        conexion.close()
        return documento
    except Exception as e:
        print(f"Error al obtener documento: {e}")
        return None

def actualizar_documento(documento_id, codigo, nombre, version, estado):
    """Actualiza un documento existente"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE listadomaestro 
            SET codigo = %s, nombre_documento = %s, version = %s, estado = %s
            WHERE id = %s
        """, (codigo, nombre, version, estado, documento_id))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        cursor.close()
        conexion.close()
        return filas_afectadas > 0
    except Exception as e:
        print(f"Error al actualizar documento: {e}")
        return False

def eliminar_documento(documento_id):
    """Cambia el estado del documento a 'Obsoleto'"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE listadomaestro 
            SET estado = 'Obsoleto'
            WHERE id = %s
        """, (documento_id,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        cursor.close()
        conexion.close()
        return filas_afectadas > 0
    except Exception as e:
        print(f"Error al eliminar documento: {e}")
        return False

# ===================== FUNCIONES DE ESTADÍSTICAS =====================

def obtener_estadisticas():
    """Obtiene estadísticas del sistema para el dashboard"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        # Total documentos
        cursor.execute("SELECT COUNT(*) as total FROM listadomaestro")
        total_docs = cursor.fetchone()['total']
        
        # Documentos vigentes
        cursor.execute("SELECT COUNT(*) as total FROM listadomaestro WHERE estado = 'Vigente'")
        docs_vigentes = cursor.fetchone()['total']
        
        # Documentos pendientes
        cursor.execute("SELECT COUNT(*) as total FROM listadomaestro WHERE estado = 'Pendiente'")
        docs_pendientes = cursor.fetchone()['total']
        
        # Usuarios activos
        cursor.execute("SELECT COUNT(*) as total FROM usuarios WHERE activo = 1")
        usuarios_activos = cursor.fetchone()['total']
        
        cursor.close()
        conexion.close()
        
        return {
            'total_documentos': total_docs,
            'documentos_vigentes': docs_vigentes,
            'documentos_pendientes': docs_pendientes,
            'usuarios_activos': usuarios_activos,
            'documentos_por_vencer': 0  # Puedes implementar esta lógica después
        }
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return {
            'total_documentos': 0,
            'documentos_vigentes': 0,
            'documentos_pendientes': 0,
            'usuarios_activos': 1,
            'documentos_por_vencer': 0
        }