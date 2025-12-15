from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from conexion import crear_conexion
from querys import *

app = Flask(__name__)
app.secret_key = '123456'

# ===================== RUTAS DE PÁGINAS =====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inicio')
def inicio():
    return render_template('index.html')

@app.route('/ofline')
def ofline():
    return render_template('dashboard.html')

@app.route('/usuario-nuevo')
def usuario_nuevo():
    return render_template('usuarioNuevo.html')

@app.route('/recuperar')
def recuperar():
    return render_template('olvidoContrasena.html')

@app.route('/gestion-usuarios')
def gestion_usuarios():
    if 'usuario_id' not in session:
        return redirect(url_for('gestion_usuarios.html'))
    return render_template('gestion_usuarios.html')

@app.route('/construccion-documentos')
def construccion_documentos():
    if 'usuario_id' not in session:
        return redirect(url_for('construccion_documentos.html'))
    return render_template('construccion_documentos.html')

@app.route('/listado-maestro')
def listado_maestro():
    if 'usuario_id' not in session:
        return redirect(url_for('listado_maestro.html'))
    return render_template('listado_maestro.html')

# ===================== API - AUTENTICACIÓN =====================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    if not usuario or not password:
        return jsonify(success=False, message="Campos obligatorios")

    conexion = crear_conexion()
    if not conexion:
        return jsonify(success=False, message="Error de conexión a la base de datos")
    
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND activo = 1", (usuario,))
    user = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not user or not check_password_hash(user['password'], password):
        return jsonify(success=False, message="Usuario o contraseña incorrectos")

    session['usuario_id'] = user['id']
    session['usuario'] = user['usuario']
    session['rol'] = user['rol_id']
    session['nombre_completo'] = f"{user['nombres']} {user['apellidos']}"

    return jsonify(success=True, redirect="/dashboard")

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify(success=True, redirect="/")

@app.route('/api/verificar_sesion')
def verificar_sesion():
    if 'usuario_id' in session:
        return jsonify(
            autenticado=True,
            nombre=session.get('nombre_completo', 'Usuario'),
            rol=session.get('rol', 'Invitado')
        )
    return jsonify(autenticado=False)

# ===================== API - USUARIOS =====================

@app.route('/api/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    
    password_hash = generate_password_hash(data['password'])
    
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO usuarios (nombres, apellidos, email, usuario, password, rol_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['nombres'],
            data['apellidos'],
            data['email'],
            data['usuario'],
            password_hash,
            data['perfil']
        ))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        return jsonify(success=True, message="Usuario creado exitosamente")
    except Exception as e:
        return jsonify(success=False, message=f"Error al crear usuario: {str(e)}")

@app.route('/api/usuarios')
def api_obtener_usuarios():
    if 'usuario_id' not in session:
        return jsonify(success=False, message="No autorizado")
    
    usuarios = obtener_usuarios()
    return jsonify(success=True, usuarios=usuarios)

@app.route('/api/roles')
def api_obtener_roles():
    if 'usuario_id' not in session:
        return jsonify(success=False, message="No autorizado")
    
    roles = obtener_roles()
    return jsonify(success=True, roles=roles)

@app.route('/api/inactivar_usuario/<int:usuario_id>', methods=['POST'])
def api_inactivar_usuario(usuario_id):
    if 'usuario_id' not in session:
        return jsonify(success=False, message="No autorizado")
    
    if inactivar_usuario(usuario_id):
        return jsonify(success=True, message="Usuario inactivado correctamente")
    return jsonify(success=False, message="Error al inactivar usuario")

# ===================== API - DOCUMENTOS =====================

@app.route('/api/procesos')
def api_obtener_procesos():
    if 'usuario_id' not in session:
        return jsonify(success=False, message="No autorizado")
    
    procesos = obtener_procesos()
    return jsonify(success=True, procesos=procesos)

@app.route('/api/crear_documento', methods=['POST'])
def api_crear_documento():
    if 'usuario_id' not in session:
        return jsonify(success=False, message="No autorizado")
    
    data = request.get_json()
    
    if insertar_documento(
        data.get('proceso'),
        data.get('codigo'),
        data.get('nombre'),
        data.get('version'),
        data.get('estado', 'Pendiente')
    ):
        return jsonify(success=True, message="Documento creado exitosamente")
    return jsonify(success=False, message="Error al crear documento")

@app.route('/api/documentos')
def api_obtener_documentos():
    if 'usuario_id' not in session:
        return jsonify(success=False, message="No autorizado")
    
    documentos = obtener_documentos()
    return jsonify(success=True, documentos=documentos)

@app.route('/api/documento/<int:documento_id>')
def api_obtener_documento(documento_id):
    if 'usuario_id' not in session:
        return jsonify(success=False, message="No autorizado")
    
    documento = obtener_documento_por_id(documento_id)
    if documento:
        return jsonify(success=True, documento=documento)
    return jsonify(success=False, message="Documento no encontrado")

@app.route('/api/actualizar_documento/<int:documento_id>', methods=['POST'])
def api_actualizar_documento(documento_id):
    if 'usuario_id' not in session:
        return jsonify(success=False, message="No autorizado")
    
    data = request.get_json()
    
    if actualizar_documento(
        documento_id,
        data.get('codigo'),
        data.get('nombre'),
        data.get('version'),
        data.get('estado')
    ):
        return jsonify(success=True, message="Documento actualizado exitosamente")
    return jsonify(success=False, message="Error al actualizar documento")

@app.route('/api/eliminar_documento/<int:documento_id>', methods=['POST'])
def api_eliminar_documento(documento_id):
    if 'usuario_id' not in session:
        return jsonify(success=False, message="No autorizado")
    
    if eliminar_documento(documento_id):
        return jsonify(success=True, message="Documento marcado como obsoleto")
    return jsonify(success=False, message="Error al eliminar documento")

# ===================== API - ESTADÍSTICAS =====================

@app.route('/api/estadisticas')
def api_estadisticas():
    if 'usuario_id' not in session:
        return jsonify(success=False, message="No autorizado")
    
    stats = obtener_estadisticas()
    return jsonify(success=True, **stats)

# ===================== EJECUCIÓN =====================

if __name__ == '__main__':
    app.run(debug=True)