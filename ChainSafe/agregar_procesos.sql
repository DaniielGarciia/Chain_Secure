-- =========================
-- SCRIPT PARA AGREGAR PROCESOS A LA BASE DE DATOS
-- =========================

USE sgcs;

-- Crear tabla de procesos si no existe
CREATE TABLE IF NOT EXISTS procesos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar procesos comunes en sistemas BASC
INSERT INTO procesos (nombre, descripcion) VALUES
('Gestión Humana', 'Procesos relacionados con la gestión del talento humano'),
('Gestión Financiera', 'Procesos relacionados con la gestión financiera y contable'),
('Gestión Comercial', 'Procesos de ventas y relación con clientes'),
('Gestión de Compras', 'Procesos de adquisición de bienes y servicios'),
('Gestión Logística', 'Procesos de almacenamiento, transporte y distribución'),
('Gestión de Calidad', 'Procesos del sistema de gestión de calidad'),
('Gestión de Seguridad', 'Procesos de seguridad física y control de accesos'),
('Gestión Tecnológica', 'Procesos de tecnología e infraestructura IT'),
('Gestión Estratégica', 'Procesos de planeación estratégica y dirección'),
('Gestión Operacional', 'Procesos operativos principales de la organización')
ON DUPLICATE KEY UPDATE nombre = nombre;

-- Verificar los procesos insertados
SELECT * FROM procesos ORDER BY nombre;