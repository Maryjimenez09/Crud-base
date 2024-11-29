-- Crear base de datos
CREATE DATABASE domestica;
USE domestica;

-- Crear tabla `tarea`
CREATE TABLE tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    prioridad VARCHAR(100) NOT NULL,
    tipo VARCHAR(100),
    fecha_inicio DATE,
    fecha_fin DATE,
    hora TIME
);

-- Crear tabla `categoria`
CREATE TABLE categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_tarea INT NOT NULL,
    tipo_prioridad VARCHAR(50),
    categoria VARCHAR(100),
    FOREIGN KEY (id_tarea) REFERENCES tarea(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE tarea (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    prioridad VARCHAR(50) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    hora TIME NOT NULL
);
