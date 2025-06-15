import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.db import create_connection, enable_database_encryption
from model.wrapper import encrypt_applicant_profile
from mysql.connector import Error

def encrypt_all_force():
    """Force encrypt all applicant data"""
    enable_database_encryption()
    
    conn = create_connection()
    if not conn:
        print("Database connection failed")
        return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ApplicantProfile")
        all_applicants = cursor.fetchall()
        
        print(f"Total applicants: {len(all_applicants)}")
        
        count = 0
        for applicant in all_applicants:
            applicant_id = applicant['applicant_id']
            
            # Force encrypt without checking
            encrypted_data = encrypt_applicant_profile(applicant)
            
            # Update database
            update_sql = """UPDATE ApplicantProfile 
                          SET first_name = %s, last_name = %s, address = %s, phone_number = %s
                          WHERE applicant_id = %s"""
            
            cursor.execute(update_sql, (
                encrypted_data.get('first_name'),
                encrypted_data.get('last_name'),
                encrypted_data.get('address'),
                encrypted_data.get('phone_number'),
                applicant_id
            ))
            count += 1
        
        conn.commit()
        print(f"Encrypted {count} applicants")
        return True
        
    except Error as e:
        print(f"Error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    answer = input("Force encrypt semua data (y/n): ").strip().lower()
    if answer == 'y':
        if encrypt_all_force():
            print("Enkripsi berhasil")
        else:
            print("Enkripsi gagal")
    else:
        print("Dibatalkan")