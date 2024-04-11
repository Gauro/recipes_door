-- Create the recipes database
CREATE DATABASE IF NOT EXISTS recipe;

-- Switch to the recipes database
USE recipes;

-- Create the User table
CREATE TABLE IF NOT EXISTS `user` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL
);

-- Create the Recipe table
CREATE TABLE IF NOT EXISTS recipe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    `description` TEXT,
    ingredients TEXT,
    instructions TEXT,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES user(id)
);
