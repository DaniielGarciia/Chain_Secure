from Controllers.documento_controller import(
    registrar_documento_interactivo,
    listar_documentos_interactivo,
    ver_documento,
    editar_documento_interactivo,
    borrar_documento_interactivo,
)

def menu():
    while True:
        print("\n📁 CHAIN SECURE - SGCS")
        print("1. REGISTRAR DOCUMENTOS")
        print("2. LISTAR LOS DOCUMENTO")
        print("3. VER DOCUMENTOS")
        print("4. EDITAR DOCUMENTOS")
        print("5. BORRAR DOCUMENTOS")
        print("6. SALIR")

        opcion = input("Seleccionar una opción").strip()

        try:

            if opcion == "1":
                registrar_documento_interactivo()
            elif opcion == "2":
                listar_documentos_interactivo()
            elif opcion == "3":
                ver_documento()
            elif opcion == "4":
                editar_documento_interactivo()
            elif opcion == "5":
                borrar_documento_interactivo()
            elif opcion == "6":
                print("Saliendo de CHAIN SECURE")
                break            
            else:
                print("La opción no es válida")
        except Exception:
            print("Error al ejecutar la opción")
            

if __name__ == "__main__":
    menu()
            


