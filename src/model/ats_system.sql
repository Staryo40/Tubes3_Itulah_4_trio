CREATE DATABASE IF NOT EXISTS ats_system;
USE ats_system;

CREATE TABLE ApplicantProfile (
    applicant_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    email VARCHAR(100),
    phone_number VARCHAR(20),
    address VARCHAR(255)
);

CREATE TABLE ApplicationDetail (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    applicant_id INT NOT NULL,
    application_role VARCHAR(100) NOT NULL,
    cv_path VARCHAR(500) NOT NULL,
    FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id)
);