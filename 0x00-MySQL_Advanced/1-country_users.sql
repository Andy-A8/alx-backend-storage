-- A SQL script that creates a table users following these requirements:
-- id, email, name, country(enumeration of countries: US, CO and TN)
DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
	email varchar(255) NOT NULL UNIQUE,
	name varchar(255),
	country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL
);
