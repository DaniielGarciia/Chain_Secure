// ==================== Lógica de inicio de sesión ====================

document.addEventListener('DOMContentLoaded', () => {

    const loginForm = document.getElementById('loginForm');
    const usuarioInput = document.getElementById('usuario');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('errorMessage');

    // ===== VALIDACIÓN DEL USUARIO =====
    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const usuario = usuarioInput.value.trim();
        const password = passwordInput.value.trim();

        // Validación básica
        if (!usuario || !password) {
            mostrarError('Por favor complete todos los campos');
            return;
        }

        // ===== SIMULACIÓN TEMPORAL PARA PRUEBA =====
        if (usuario === 'admin' && password === 'admin123') {
            // SOLO SE CORRIGE LA RUTA
            window.location.href = '/dashboard';
        } else {
            mostrarError('Usuario o contraseña incorrectos');
        }
    });

    // ===== OCULTAR ERROR AL ESCRIBIR =====
    [usuarioInput, passwordInput].forEach(input => {
        input.addEventListener('input', ocultarError);
    });

    // ===== ENTER EN PASSWORD =====
    passwordInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            loginForm.dispatchEvent(new Event('submit'));
        }
    });

    // ===== FUNCIONES AUXILIARES =====
    function mostrarError(mensaje) {
        errorMessage.textContent = mensaje;
        errorMessage.classList.add('show');
    }

    function ocultarError() {
        errorMessage.classList.remove('show');
    }

});
