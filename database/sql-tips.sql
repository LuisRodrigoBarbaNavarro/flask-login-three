# Crear Esquema 'store'; E Implementación.
CREATE SCHEMA store ;
USE store;

#  Crear Tabla 'users; Permite Almacenamiento De Usuarios.
CREATE TABLE users (
	id smallint unsigned NOT NULL AUTO_INCREMENT,
	username varchar(20) NOT NULL,
	password char(102) NOT NULL,
	fullname varchar(50),
	usertype tinyint NOT NULL,
	PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci

# Crear Procedimiento Almacenado Para Añadir Usuarios.
DELIMITER //
CREATE PROCEDURE sp_AddUser(
    IN pUserName VARCHAR(20),
    IN pPassword VARCHAR(102),
    IN pFullName VARCHAR(50),
    IN pUserType TINYINT
)
BEGIN
	DECLARE userCount INT;
    DECLARE hashedPassword VARCHAR(255);
    SET hashedPassword = SHA2(pPassword, 256);

    -- Verificar si el usuario ya existe
    SELECT COUNT(*) INTO userCount FROM users WHERE username = pUserName COLLATE utf8mb4_unicode_ci;
    
    -- Manejar la excepción de usuario duplicado
    IF userCount > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: Usuario ya existe.';
    END IF;

    -- Verificar campos nulos
    IF pUserName IS NULL OR pPassword IS NULL OR pUserType IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: Campos obligatorios no pueden ser nulos.';
    END IF;

    -- Insertar el nuevo usuario
    INSERT INTO users (username, password, fullname, usertype)
    VALUES (pUserName, hashedPassword, pFullName, pUserType);
END //
DELIMITER ;

# Crear Procedimiento Almacenado Para Verificar Usuarios.
DELIMITER //
CREATE PROCEDURE sp_verifyIdentity(IN pUsername VARCHAR(20), IN pPlainTextPassword VARCHAR(20))
BEGIN
	DECLARE storedPassword VARCHAR(255);
	SELECT password INTO storedPassword FROM users
	WHERE username = pUsername COLLATE utf8mb4_unicode_ci;
	IF storedPassword IS NOT NULL AND storedPassword = SHA2(pPlainTextPassword, 256) THEN
		SELECT id, username, storedPassword, fullname, usertype FROM users
		WHERE username = pUserName COLLATE utf8mb4_unicode_ci;
		ELSE
		SELECT NULL;
	END IF;
END //
DELIMITER ;

# Creación De Usuario Normal Y Administrador.
call sp_AddUser("rodrigobarba", "user-12345", "Rodrigo Barba", 0);
call sp_AddUser("luisr", "user-12345", "Luis Barba", 0);
call sp_AddUser("null-user", null, "Luis Rodrigo", 0);
call sp_AddUser("administrador", "adminuser-12345", "John Doe", 1);

# Creación De Usuario Normal Y Administrador.
call sp_verifyIdentity("administrador","adminuser-12345");

# Borrar Usuario
DELETE FROM users WHERE id=2;

# Eliminación De Procedimientos.
DROP PROCEDURE IF EXISTS sp_AddUser;