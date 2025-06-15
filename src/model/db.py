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

def add_applicant(first, last, dob, phone, address):
    """Tambah pelamar baru - UPDATED: Hapus email (tidak ada di tubes3_seeding.sql)"""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        sql = """INSERT INTO ApplicantProfile 
                 (first_name, last_name, date_of_birth, phone_number, address)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (first, last, dob, phone, address))
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
    field sesuai skema SQL terbaru - UPDATED: Hapus email karena tidak ada di tubes3_seeding.sql
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
    print("Statistik:", get_stats())# IMPORT ENCRYPTION WRAPPER
from .wrapper import (
    with_encryption, 
    encrypt_applicant_profile, 
    decrypt_applicant_profile,
    decrypt_applicant_list,
    enable_database_encryption,
    disable_database_encryption,
    is_database_encryption_enabled
)

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

@with_encryption(encrypt_input=True)
def add_applicant(first, last, dob, phone, address):
    """Tambah pelamar baru dengan enkripsi otomatis"""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        sql = """INSERT INTO ApplicantProfile 
                 (first_name, last_name, date_of_birth, phone_number, address)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (first, last, dob, phone, address))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error tambah pelamar: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

@with_encryption(decrypt_output=True)
def get_applicant(applicant_id):
    """Ambil data pelamar dengan dekripsi otomatis"""
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

@with_encryption(decrypt_output=True)
def get_applicant_by_id(applicant_id):
    """Ambil pelamar berdasarkan ID dengan dekripsi otomatis"""
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

@with_encryption(decrypt_list=True)
def get_all_applicants():
    """Ambil semua pelamar dengan dekripsi otomatis"""
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

@with_encryption(decrypt_list=True)
def get_cv_list():
    """
    Ambil daftar CV dengan JOIN dan dekripsi otomatis
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
            ap.phone_number,
            ap.address,
            ad.detail_id,
            ad.application_role,
            ad.cv_path
        FROM ApplicationDetail ad
        JOIN ApplicantProfile ap ON ad.applicant_id = ap.applicant_id
        ORDER BY ap.last_name
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        
        return result  
        
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

# ============= ENCRYPTION CONTROL =============

def init_database_encryption(enable=False):
    """Initialize database encryption settings"""
    if enable:
        enable_database_encryption()
    else:
        disable_database_encryption()

def get_encryption_status():
    """Get current encryption status"""
    return is_database_encryption_enabled()

def toggle_encryption():
    """Toggle encryption on/off"""
    if is_database_encryption_enabled():
        disable_database_encryption()
    else:
        enable_database_encryption()

# ============= MANUAL ENCRYPTION FUNCTIONS (OPTIONAL) =============

def add_applicant_manual_encryption(applicant_data):
    """Contoh fungsi dengan manual encryption"""
    if is_database_encryption_enabled():
        encrypted_data = encrypt_applicant_profile(applicant_data)
    else:
        encrypted_data = applicant_data
    
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        sql = """INSERT INTO ApplicantProfile 
                 (first_name, last_name, date_of_birth, phone_number, address)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            encrypted_data.get('first_name'),
            encrypted_data.get('last_name'),
            encrypted_data.get('date_of_birth'),
            encrypted_data.get('phone_number'),
            encrypted_data.get('address')
        ))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error tambah pelamar: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_applicant_manual_decryption(applicant_id):
    """Contoh fungsi dengan manual decryption"""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ApplicantProfile WHERE applicant_id = %s", (applicant_id,))
        encrypted_data = cursor.fetchone()
        
        if encrypted_data:
            if is_database_encryption_enabled():
                return decrypt_applicant_profile(encrypted_data)
            else:
                return encrypted_data
        return None
    except Error as e:
        print(f"Error ambil pelamar: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# ============= MIGRATION UTILITIES =============

def migrate_existing_data_to_encrypted():
    """
    Utility untuk migrate data existing ke format encrypted
    HATI-HATI: Backup database sebelum menjalankan!
    """
    
    confirmation = input("Continue? (yes/no): ")
    if confirmation.lower() != 'yes':
        print("Migration cancelled")
        return
    
    disable_database_encryption()
    
    conn = create_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ApplicantProfile")
        all_applicants = cursor.fetchall()
        
        print(f"Found {len(all_applicants)} applicants to encrypt")
        
        enable_database_encryption()
        
        for applicant in all_applicants:
            applicant_id = applicant['applicant_id']
            
            if any(str(value).startswith('RSA:') for value in applicant.values() if isinstance(value, str)):
                print(f"Skipping applicant {applicant_id} - already encrypted")
                continue
            
            encrypted_data = encrypt_applicant_profile(applicant)
            
            update_sql = """UPDATE ApplicantProfile 
                          SET first_name = %s, last_name = %s, 
                              date_of_birth = %s, address = %s, phone_number = %s
                          WHERE applicant_id = %s"""
            
            cursor.execute(update_sql, (
                encrypted_data.get('first_name'),
                encrypted_data.get('last_name'),
                encrypted_data.get('date_of_birth'),
                encrypted_data.get('address'),
                encrypted_data.get('phone_number'),
                applicant_id
            ))
            
            print(f"Encrypted applicant {applicant_id}")
        
        conn.commit()
        print("Migration completed successfully!")
        
    except Error as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Test koneksi database:", test_connection())
    print("Statistik:", get_stats())
    print("Database encryption integration ready!")