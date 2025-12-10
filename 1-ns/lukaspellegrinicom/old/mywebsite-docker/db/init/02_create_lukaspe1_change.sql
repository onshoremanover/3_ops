-- 02_create_lukaspe1_change.sql

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS lukaspe1_change CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the newly created database
USE lukaspe1_change;

-- Import the schema and data from lukaspe1_change.sql
-- Similarly, paste the contents of lukaspe1_change.sql here.

-- Example schema and data (replace with actual content from lukaspe1_change.sql)
CREATE TABLE IF NOT EXISTS settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    key_name VARCHAR(100) NOT NULL UNIQUE,
    value TEXT NOT NULL
);

INSERT INTO settings (key_name, value) VALUES
('site_name', 'My Website'),
('admin_email', 'admin@example.com');

