CREATE DATABASE placement_db;
USE placement_db;

CREATE TABLE students(
student_id INT PRIMARY KEY,
student_name VARCHAR(100),
department VARCHAR(50),
cgpa DECIMAL(3,2)
);

CREATE TABLE placements(
placement_id INT PRIMARY KEY AUTO_INCREMENT,
student_id INT,
company_name VARCHAR(100),
package_lpa DECIMAL(5,2),
placement_status VARCHAR(20),
placement_year INT,
FOREIGN KEY(student_id) REFERENCES students(student_id)
);
