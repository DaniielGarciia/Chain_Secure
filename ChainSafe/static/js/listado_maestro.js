// ==================== LISTADO MAESTRO DE DOCUMENTOS ====================

let documentosOriginales = [];

// Cargar al iniciar
document.addEventListener('DOMContentLoaded', () => {
    verificarSesion();
    cargarDocumentos();
    
    // Event listeners para filtros
    document.getElementById('buscarCodigo').addEventListener('input', filtrarDocumentos);
    document.getElementById('buscarNombre').addEventListener('input', filtrarDocumentos);
    document.getElementById('filtroEstado').addEventListener('change', filtrarDocumentos);
    
    document.getElementById('formEditar').addEventListener('submit', guardarEdicion);
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

// ==================== CARGAR DOCUMENTOS ====================
async function cargarDocumentos() {
    try {
        const response = await fetch('/api/documentos');
        const data = await response.json();
        
        if (data.success) {
            documentosOriginales = data.documentos;
            mostrarDocumentos(data.documentos);
        }
    } catch (error) {
        console.error('Error al cargar documentos:', error);
        document.getElementById('tablaListado').innerHTML = `
            <tr>
                <td colspan="6" class="sin-resultados">
                    <div class="sin-resultados-icon">⚠️</div>
                    <p>Error al cargar documentos</p>
                </td>
            </tr>
        `;
    }
}

// ==================== MOSTRAR DOCUMENTOS ====================
function mostrarDocumentos(documentos) {
    const tbody = document.getElementById('tablaListado');
    
    if (documentos.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="sin-resultados">
                    <div class="sin-resultados-icon">📄</div>
                    <p>No se encontraron documentos</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = '';
    
    documentos.forEach(doc => {
        const estadoClass = doc.estado.toLowerCase();
        const fechaCreacion = doc.fecha_creacion ? 
            new Date(doc.fecha_creacion).toLocaleDateString('es-ES') : 'N/A';
        
        tbody.innerHTML += `
            <tr>
                <td><strong>${doc.codigo}</strong></td>
                <td>${doc.nombre_documento}</td>
                <td>${doc.version}</td>
                <td><span class="badge ${estadoClass}">${doc.estado}</span></td>
                <td>${fechaCreacion}</td>
                <td>
                    <button class="btn-accion" onclick="abrirModalEditar(${doc.id})" title="Editar">
                        ✏️
                    </button>
                    <button class="btn-accion" onclick="eliminarDocumento(${doc.id})" title="Eliminar">
                        🗑️
                    </button>
                </td>
            </tr>
        `;
    });
}

// ==================== FILTRAR DOCUMENTOS ====================
function filtrarDocumentos() {
    const buscarCodigo = document.getElementById('buscarCodigo').value.toLowerCase();
    const buscarNombre = document.getElementById('buscarNombre').value.toLowerCase();
    const filtroEstado = document.getElementById('filtroEstado').value;
    
    const documentosFiltrados = documentosOriginales.filter(doc => {
        const coincideCodigo = doc.codigo.toLowerCase().includes(buscarCodigo);
        const coincideNombre = doc.nombre_documento.toLowerCase().includes(buscarNombre);
        const coincideEstado = filtroEstado === '' || doc.estado === filtroEstado;
        
        return coincideCodigo && coincideNombre && coincideEstado;
    });
    
    mostrarDocumentos(documentosFiltrados);
}

// ==================== MODAL EDITAR ====================
async function abrirModalEditar(documentoId) {
    try {
        const response = await fetch(`/api/documento/${documentoId}`);
        const data = await response.json();
        
        if (data.success && data.documento) {
            const doc = data.documento;
            document.getElementById('editId').value = doc.id;
            document.getElementById('editCodigo').value = doc.codigo;
            document.getElementById('editNombre').value = doc.nombre_documento;
            document.getElementById('editVersion').value = doc.version;
            document.getElementById('editEstado').value = doc.estado;
            
            document.getElementById('modalEditar').classList.add('active');
        }
    } catch (error) {
        console.error('Error al cargar documento:', error);
        alert('Error al cargar documento');
    }
}

function cerrarModalEditar() {
    document.getElementById('modalEditar').classList.remove('active');
}

// ==================== GUARDAR EDICIÓN ====================
async function guardarEdicion(e) {
    e.preventDefault();
    
    const documentoId = document.getElementById('editId').value;
    const datos = {
        codigo: document.getElementById('editCodigo').value,
        nombre: document.getElementById('editNombre').value,
        version: document.getElementById('editVersion').value,
        estado: document.getElementById('editEstado').value
    };
    
    try {
        const response = await fetch(`/api/actualizar_documento/${documentoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('✅ Documento actualizado exitosamente');
            cerrarModalEditar();
            cargarDocumentos();
        } else {
            alert('❌ Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error al actualizar documento:', error);
        alert('❌ Error al actualizar documento');
    }
}

// ==================== ELIMINAR DOCUMENTO ====================
async function eliminarDocumento(documentoId) {
    if (!confirm('¿Está seguro de marcar este documento como obsoleto?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/eliminar_documento/${documentoId}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('✅ Documento marcado como obsoleto');
            cargarDocumentos();
        } else {
            alert('❌ Error al eliminar documento');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error al eliminar documento');
    }
}

// ==================== EXPORTAR A EXCEL ====================
function exportarExcel() {
    // Crear tabla HTML para exportar
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Código</th>
                    <th>Nombre del Documento</th>
                    <th>Versión</th>
                    <th>Estado</th>
                    <th>Fecha Creación</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    documentosOriginales.forEach(doc => {
        const fechaCreacion = doc.fecha_creacion ? 
            new Date(doc.fecha_creacion).toLocaleDateString('es-ES') : 'N/A';
        
        html += `
            <tr>
                <td>${doc.codigo}</td>
                <td>${doc.nombre_documento}</td>
                <td>${doc.version}</td>
                <td>${doc.estado}</td>
                <td>${fechaCreacion}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    
    // Crear blob y descargar
    const blob = new Blob([html], { type: 'application/vnd.ms-excel' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Listado_Maestro_${new Date().toISOString().slice(0, 10)}.xls`;
    a.click();
    window.URL.revokeObjectURL(url);
    
    alert('✅ Listado exportado exitosamente');
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