# db.py -- Modul koneksi & query ATS DB MySQL
import mysql.connector

# Bikin koneksi ke database
def db_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="passwordmu",   # ganti sesuai setting
        database="ats_system"
    )

# Insert data pelamar, return id
def add_applicant(first, last, dob, email, phone, addr):
    db = db_conn()
    cur = db.cursor()
    sql = """
    INSERT INTO ApplicantProfile
    (first_name, last_name, date_of_birth, email, phone_number, address)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql, (first, last, dob, email, phone, addr))
    db.commit()
    aid = cur.lastrowid
    cur.close()
    db.close()
    return aid

# Insert detail lamaran, return id
def add_detail(applicant_id, role, cv_path):
    db = db_conn()
    cur = db.cursor()
    sql = """
    INSERT INTO ApplicationDetail
    (applicant_id, application_role, cv_path)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (applicant_id, role, cv_path))
    db.commit()
    did = cur.lastrowid
    cur.close()
    db.close()
    return did

# Ambil semua data pelamar
def get_applicants():
    db = db_conn()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM ApplicantProfile")
    rows = cur.fetchall()
    cur.close()
    db.close()
    return rows

# Ambil detail lamaran + profile (join view)
def get_details():
    db = db_conn()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM ApplicantApplicationView")
    rows = cur.fetchall()
    cur.close()
    db.close()
    return rows

# Ambil satu CV berdasarkan id
def get_cv(aid):
    db = db_conn()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM ApplicantProfile WHERE applicant_id=%s", (aid,))
    row = cur.fetchone()
    cur.close()
    db.close()
    return row

# Contoh penggunaan
if __name__ == "__main__":
    # Insert contoh
    aid = add_applicant("Budi", "Santoso", "1999-09-09", "budi@mail.com", "0812345678", "Bandung")
    print("ID pelamar:", aid)
    # Insert detail lamaran
    did = add_detail(aid, "Software Engineer", "/data/cv/budi_software.pdf")
    print("ID detail:", did)
    # Cek semua pelamar
    data = get_applicants()
    print(data)
