// ==================== GESTIÓN DE USUARIOS ====================

let rolesDisponibles = [];

// Cargar al iniciar
document.addEventListener('DOMContentLoaded', () => {
    verificarSesion();
    cargarRoles();
    cargarUsuarios();
    
    document.getElementById('formUsuario').addEventListener('submit', guardarUsuario);
});

// ==================== VERIFICAR SESIÓN ====================
async function verificarSesion() {
    try {
        const response = await fetch('/api/verificar_sesion');
        const data = await response.json();
        
        if (!data.autenticado) {
            window.location.href = '/';
            return;
        }
        
        document.getElementById('userName').textContent = data.nombre;
        document.getElementById('userRole').textContent = data.rol;
        document.getElementById('userAvatar').textContent = data.nombre.charAt(0).toUpperCase();
    } catch (error) {
        console.error('Error al verificar sesión:', error);
        window.location.href = '/';
    }
}

// ==================== CARGAR ROLES ====================
async function cargarRoles() {
    try {
        const response = await fetch('/api/roles');
        const data = await response.json();
        
        if (data.success) {
            rolesDisponibles = data.roles;
            const select = document.getElementById('rol');
            select.innerHTML = '<option value="">Seleccione un rol</option>';
            
            data.roles.forEach(rol => {
                select.innerHTML += `<option value="${rol.id}">${rol.nombre}</option>`;
            });
        }
    } catch (error) {
        console.error('Error al cargar roles:', error);
    }
}

// ==================== CARGAR USUARIOS ====================
async function cargarUsuarios() {
    try {
        const response = await fetch('/api/usuarios');
        const data = await response.json();
        
        if (data.success) {
            mostrarUsuarios(data.usuarios);
        }
    } catch (error) {
        console.error('Error al cargar usuarios:', error);
        document.getElementById('tablaUsuarios').innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; color: red;">
                    Error al cargar usuarios
                </td>
            </tr>
        `;
    }
}

// ==================== MOSTRAR USUARIOS ====================
function mostrarUsuarios(usuarios) {
    const tbody = document.getElementById('tablaUsuarios');
    
    if (usuarios.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center;">
                    No hay usuarios registrados
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = '';
    
    usuarios.forEach(usuario => {
        const rolClass = usuario.rol.toLowerCase().replace(/\s/g, '');
        tbody.innerHTML += `
            <tr>
                <td>${usuario.nombres}</td>
                <td>${usuario.apellidos}</td>
                <td>${usuario.email}</td>
                <td>${usuario.usuario}</td>
                <td><span class="badge ${rolClass}">${usuario.rol}</span></td>
                <td>
                    <button class="btn-accion" onclick="inactivarUsuario(${usuario.id})" title="Inactivar">
                        🗑️
                    </button>
                </td>
            </tr>
        `;
    });
}

// ==================== MODAL ====================
function abrirModalNuevo() {
    document.getElementById('formUsuario').reset();
    document.getElementById('modalUsuario').classList.add('active');
}

function cerrarModal() {
    document.getElementById('modalUsuario').classList.remove('active');
}

// ==================== GUARDAR USUARIO ====================
async function guardarUsuario(e) {
    e.preventDefault();
    
    const usuario = {
        nombres: document.getElementById('nombres').value,
        apellidos: document.getElementById('apellidos').value,
        email: document.getElementById('email').value,
        usuario: document.getElementById('usuario').value,
        password: document.getElementById('password').value,
        perfil: document.getElementById('rol').value
    };
    
    try {
        const response = await fetch('/api/crear_usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(usuario)
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Usuario creado exitosamente');
            cerrarModal();
            cargarUsuarios();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error al guardar usuario:', error);
        alert('Error al guardar usuario');
    }
}

// ==================== INACTIVAR USUARIO ====================
async function inactivarUsuario(usuarioId) {
    if (!confirm('¿Está seguro de inactivar este usuario?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/inactivar_usuario/${usuarioId}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Usuario inactivado correctamente');
            cargarUsuarios();
        } else {
            alert('Error al inactivar usuario');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al inactivar usuario');
    }
}

// ==================== CERRAR SESIÓN ====================
async function cerrarSesion() {
    if (!confirm('¿Está seguro que desea cerrar sesión?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/logout', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            window.location.href = data.redirect;
        }
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
        window.location.href = '/';
    }
}