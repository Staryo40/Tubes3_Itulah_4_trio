-- Skema basis data untuk ATS (Applicant Tracking System)

-- Membuat database jika belum ada
CREATE DATABASE IF NOT EXISTS ats_system;
USE ats_system;

-- Menyimpan data identitas inti pelamar
CREATE TABLE ApplicantProfile (
    applicant_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (applicant_id),
    INDEX idx_email (email)
);

-- Menyimpan detail lamaran, termasuk path file CV
CREATE TABLE ApplicationDetail (
    detail_id INT NOT NULL AUTO_INCREMENT,
    applicant_id INT NOT NULL,
    application_role VARCHAR(100) NOT NULL,
    cv_path VARCHAR(500) NOT NULL,
    application_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (detail_id),
    FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE,

    INDEX idx_applicant_id (applicant_id),
    INDEX idx_application_role (application_role)
);

-- Menyimpan data sesi pencarian dan performa algoritma
CREATE TABLE SearchSession (
    session_id INT NOT NULL AUTO_INCREMENT,
    keywords TEXT NOT NULL,
    algorithm_used ENUM('KMP', 'BM', 'AC') NOT NULL,
    exact_match_time_ms INT DEFAULT 0,
    fuzzy_match_time_ms INT DEFAULT 0,
    total_cvs_scanned INT DEFAULT 0,
    results_found INT DEFAULT 0,
    top_matches_requested INT DEFAULT 10,
    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (session_id),
    INDEX idx_algorithm_timestamp (algorithm_used, search_timestamp)
);

-- Menyediakan view untuk query efisien identitas dan aplikasi
CREATE VIEW ApplicantApplicationView AS
SELECT 
    ap.applicant_id,
    ap.first_name,
    ap.last_name,
    ap.email,
    ap.date_of_birth,
    ap.address,
    ap.phone_number,
    ad.detail_id,
    ad.application_role,
    ad.cv_path,
    ad.application_date
FROM ApplicantProfile ap
LEFT JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id;
