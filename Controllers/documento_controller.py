from Database.querys import(
    insertar_documento,
    obtener_documentos,
    obtener_documento_por_id,
    actualizar_documento,
    eliminar_documento,
    obtener_procesos,
)

def registrar_documento_interactivo():
    print("\n=== Registrar Documento ===")

#Mostrar los documentos desde las base de datos
    proceso = obtener_procesos()
    if not proceso:
        print("No hay procesos registrados")
        return
    
    print("\n Listado de Procesos")
    for p in proceso:
        print(f"{p['id']}. {p['nombre']}" if 'nombre' in p else f"{p['id']}. {p}")

# Seleccionar el proceso
    id_proceso = input("Selecciona el ID del proceso: ").strip()
    proceso_seleccionado = None
    for p in proceso:
        if str(p['id']) == id_proceso:
            proceso_seleccionado = p
            break

    if not proceso_seleccionado:
        print("⚠️ El ID del proceso no válido.")
        return
    
# en este punto sale el nombre del proceso

    proceso = proceso_seleccionado['nombre']  
    
# codigo para los otros datos
    
    codigo = input("Código del Documento: ").strip()
    nombre = input("Nombre del Documento: ").strip()
    version = input("Versión: ").strip()
    estado = input("Estado del Documento (Vigente o Eliminado): ").strip()

    if not (proceso and codigo and nombre):
        print("Todos los campos son obligatorios")
        return
    
    insertar_documento(proceso, codigo, nombre, version or 1, estado or "eliminado")


def listar_documentos_interactivo():
    print("\n=== Lista de Documentos ===")
    documentos = obtener_documentos()
    if not documentos:
        print("No hay documentos registrados.")
        return
    for doc in documentos:
        print(f"ID: {doc['id']} | {doc['proceso']} | {doc['codigodocumento']} | {doc['nombredocumento']} | v{doc['version']} | {doc['estado']}")


def ver_documento():
    id_doc = input("ID del documento: ").strip()
    if not id_doc.isdigit():
        print("⚠️ ID inválido.")
        return
    resultado = obtener_documento_por_id(int(id_doc))
    if not resultado:
        print("⚠️ Documento no encontrado.")
        return
    print("\n--- Detalle del Documento ---")
    for k, v in resultado.items():
        print(f"{k}: {v}")


def editar_documento_interactivo():
    id_doc = input("ID del documento a editar: ").strip()
    if not id_doc.isdigit():
        print("⚠️ ID inválido.")
        return
    id_doc = int(id_doc)
    doc = obtener_documento_por_id(id_doc)
    if not doc:
        print("⚠️ Documento no encontrado.")
        return

    print("Deja en blanco los campos que no quieras modificar.")
    nuevo_proceso = input(f"Nuevo proceso (actual: {doc['proceso']}): ").strip() or None
    nuevo_codigo = input(f"Nuevo código (actual: {doc['codigodocumento']}): ").strip() or None
    nuevo_nombre = input(f"Nuevo nombre (actual: {doc['nombredocumento']}): ").strip() or None
    nueva_version = input(f"Nueva versión (actual: {doc['version']}): ").strip() or None
    nuevo_estado = input(f"Nuevo estado (actual: {doc['estado']}): ").strip() or None

    actualizar_documento(id_doc, nuevo_proceso, nuevo_codigo, nuevo_nombre, nueva_version, nuevo_estado)


def borrar_documento_interactivo():
    id_doc = input("ID del documento a eliminar: ").strip()
    if not id_doc.isdigit():
        print("⚠️ ID inválido.")
        return
    confirmado = input(f"¿Seguro que deseas eliminar el documento {id_doc}? (s/n): ").lower()
    if confirmado == "s":
        eliminar_documento(int(id_doc))
    else:
        print("🚫 Operación cancelada.")


    