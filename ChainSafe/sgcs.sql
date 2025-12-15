CREATE DATABASE IF NOT EXISTS sgcs;
USE sgcs;

-- =========================
-- TABLA ROLES
-- =========================
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO roles (nombre) VALUES
('Administrador'),
('Lider'),
('Gestor'),
('Invitado');

-- =========================
-- TABLA USUARIOS
-- =========================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- =========================
-- USUARIO ADMIN INICIAL
-- password: admin123
-- =========================
INSERT INTO usuarios (nombres, apellidos, email, usuario, password, rol_id)
VALUES (
    'Administrador',
    'Sistema',
    'admin@chainsafe.com',
    'admin',
    '$pbkdf2-sha256$260000$W9Z5f3C7E...REEMPLAZAR_HASH...',
    1
);

-- =========================
-- TABLA LISTADO MAESTRO
-- =========================
CREATE TABLE listadomaestro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL,
    nombre_documento VARCHAR(200) NOT NULL,
    version VARCHAR(20),
    estado ENUM('Vigente','Pendiente','Obsoleto') DEFAULT 'Pendiente',
    fecha_creacion DATE,
    fecha_vencimiento DATE,
    responsable INT,
    FOREIGN KEY (responsable) REFERENCES usuarios(id)
);