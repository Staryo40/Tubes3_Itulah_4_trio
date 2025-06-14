import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional
from .config import DB_CONFIG

def create_connection():
    """Buat koneksi database"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error koneksi: {e}")
        return None

def test_connection():
    """Test koneksi database"""
    conn = create_connection()
    if conn and conn.is_connected():
        conn.close()
        return True
    return False

# ============= APPLICANT OPERATIONS =============

def add_applicant(first, last, dob, email, phone, address):
    """Tambah pelamar baru"""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        sql = """INSERT INTO ApplicantProfile 
                 (first_name, last_name, date_of_birth, email, phone_number, address)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (first, last, dob, email, phone, address))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error tambah pelamar: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_applicant(applicant_id):
    """Ambil data pelamar"""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ApplicantProfile WHERE applicant_id = %s", (applicant_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error ambil pelamar: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_applicants():
    """Ambil semua pelamar"""
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ApplicantProfile ORDER BY last_name")
        return cursor.fetchall()
    except Error as e:
        print(f"Error ambil semua pelamar: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# ============= APPLICATION OPERATIONS =============

def add_application(applicant_id, role, cv_path):
    """Tambah detail lamaran"""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        sql = """INSERT INTO ApplicationDetail 
                 (applicant_id, application_role, cv_path)
                 VALUES (%s, %s, %s)"""
        cursor.execute(sql, (applicant_id, role, cv_path))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error tambah lamaran: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_cv_list():
    """
    Ambil daftar CV, hasil JOIN ApplicantProfile dan ApplicationDetail,
    field sesuai skema SQL terbaru.
    """
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
        SELECT
            ap.applicant_id,
            ap.first_name,
            ap.last_name,
            ap.date_of_birth,
            ap.email,
            ap.phone_number,
            ap.address,
            ad.detail_id,
            ad.application_role,
            ad.cv_path
        FROM ApplicationDetail ad
        JOIN ApplicantProfile ap ON ad.applicant_id = ap.applicant_id
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Error as e:
        print(f"Error ambil CV list: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# ============= UTILITY =============

def get_stats():
    """Ambil statistik database"""
    conn = create_connection()
    if not conn:
        return {}
    try:
        cursor = conn.cursor()
        stats = {}
        cursor.execute("SELECT COUNT(*) FROM ApplicantProfile")
        stats['applicants'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM ApplicationDetail")
        stats['applications'] = cursor.fetchone()[0]
        return stats
    except Error as e:
        print(f"Error ambil stats: {e}")
        return {}
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Test koneksi database:", test_connection())
    print("Statistik:", get_stats())
