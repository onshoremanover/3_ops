-- 01_create_lukaspe1_my_db.sql

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS lukaspe1_my_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the newly created database
USE lukaspe1_my_db;

-- Import the schema and data from lukaspe1_my_db.sql
-- Note: Since we cannot use the SOURCE command in this context,
-- you need to paste the contents of lukaspe1_my_db.sql here.

-- Example schema and data (replace with actual content from lukaspe1_my_db.sql)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password, email) VALUES
('admin', '$2y$10$abcdefghijklmnopqrstuv', 'admin@example.com'),
('user1', '$2y$10$abcdefghijklmnopqrstuv', 'user1@example.com');

