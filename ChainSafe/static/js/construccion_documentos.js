// ==================== CONSTRUCCIÓN DE DOCUMENTOS ====================

// Cargar al iniciar
document.addEventListener('DOMContentLoaded', () => {
    verificarSesion();
    cargarProcesos();
    cargarDocumentosRecientes();
    
    document.getElementById('formDocumento').addEventListener('submit', guardarDocumento);
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

// ==================== CARGAR PROCESOS ====================
async function cargarProcesos() {
    try {
        const response = await fetch('/api/procesos');
        const data = await response.json();
        
        if (data.success) {
            const select = document.getElementById('proceso');
            select.innerHTML = '<option value="">Seleccione un proceso</option>';
            
            data.procesos.forEach(proceso => {
                select.innerHTML += `<option value="${proceso.nombre}">${proceso.nombre}</option>`;
            });
        }
    } catch (error) {
        console.error('Error al cargar procesos:', error);
        mostrarAlerta('Error al cargar procesos', 'error');
    }
}

// ==================== GUARDAR DOCUMENTO ====================
async function guardarDocumento(e) {
    e.preventDefault();
    
    const documento = {
        proceso: document.getElementById('proceso').value,
        codigo: document.getElementById('codigo').value,
        nombre: document.getElementById('nombre').value,
        version: document.getElementById('version').value,
        estado: document.getElementById('estado').value
    };
    
    try {
        const response = await fetch('/api/crear_documento', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(documento)
        });
        
        const data = await response.json();
        
        if (data.success) {
            mostrarAlerta('✅ Documento creado exitosamente', 'success');
            document.getElementById('formDocumento').reset();
            cargarDocumentosRecientes();
        } else {
            mostrarAlerta('❌ Error: ' + data.message, 'error');
        }
    } catch (error) {
        console.error('Error al guardar documento:', error);
        mostrarAlerta('❌ Error al guardar documento', 'error');
    }
}

// ==================== CARGAR DOCUMENTOS RECIENTES ====================
async function cargarDocumentosRecientes() {
    try {
        const response = await fetch('/api/documentos');
        const data = await response.json();
        
        if (data.success) {
            mostrarDocumentosRecientes(data.documentos.slice(0, 5)); // Últimos 5
        }
    } catch (error) {
        console.error('Error al cargar documentos recientes:', error);
    }
}

// ==================== MOSTRAR DOCUMENTOS RECIENTES ====================
function mostrarDocumentosRecientes(documentos) {
    const container = document.getElementById('listaRecientes');
    
    if (documentos.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #718096;">No hay documentos creados</p>';
        return;
    }
    
    container.innerHTML = '';
    
    documentos.forEach(doc => {
        const estadoClass = doc.estado.toLowerCase();
        container.innerHTML += `
            <div class="doc-card">
                <div class="doc-info">
                    <h4>${doc.codigo} - ${doc.nombre_documento}</h4>
                    <p>Versión ${doc.version} • Creado: ${formatearFecha(doc.fecha_creacion)}</p>
                </div>
                <span class="doc-badge ${estadoClass}">${doc.estado}</span>
            </div>
        `;
    });
}

// ==================== UTILIDADES ====================
function mostrarAlerta(mensaje, tipo) {
    const alert = document.getElementById('alertMsg');
    alert.textContent = mensaje;
    alert.className = `alert ${tipo}`;
    
    setTimeout(() => {
        alert.className = 'alert';
    }, 5000);
}

function formatearFecha(fecha) {
    const date = new Date(fecha);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
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