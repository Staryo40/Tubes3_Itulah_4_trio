import os
import random
import re
from PyPDF2 import PdfReader
from config import CV_DIR

def extract_pdf_text(file_path):
    """Ekstrak teks dari file PDF"""
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += clean_text(page_text) + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

def clean_text(raw_text):
    """Bersihkan teks hasil ekstraksi"""
    if not raw_text:
        return ""
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', raw_text)
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
    cleaned = re.sub(r' +', ' ', cleaned)
    return cleaned.strip()

def extract_role_from_pdf(pdf_path):
    """Ekstrak role dari baris pertama PDF"""
    try:
        text = extract_pdf_text(pdf_path)
        if text:
            lines = text.strip().split('\n')
            if lines:
                role = lines[0].strip()
                role = role.replace('_', ' ').replace('-', ' ').title()
                return role
        return "General Position"
    except Exception as e:
        print(f"Error ekstrak role dari {pdf_path}: {e}")
        return "General Position"

def scan_cv_directory(cv_dir_path):
    """Scan direktori CV dan ambil info file + role"""
    cv_files = []
    if not os.path.exists(cv_dir_path):
        print(f"❌ Direktori CV tidak ditemukan: {cv_dir_path}")
        return []
    pdf_files = [f for f in os.listdir(cv_dir_path) if f.lower().endswith('.pdf')]
    print(f"📁 Ditemukan {len(pdf_files)} file PDF di direktori CV")
    for i, filename in enumerate(pdf_files, 1):
        full_path = os.path.join(cv_dir_path, filename)
        print(f"[{i:3d}/{len(pdf_files)}] Memproses: {filename}")
        role = extract_role_from_pdf(full_path)
        cv_files.append({
            'filename': filename,
            'role': role
        })
        print(f"       Role: {role}")
    return cv_files

def read_existing_applicants(seed_file_path):
    """Baca data applicant dari seed.sql yang sudah ada"""
    applicant_data = []
    try:
        with open(seed_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        in_applicant_insert = False
        for line in lines:
            line = line.strip()
            if 'INSERT INTO ApplicantProfile' in line:
                in_applicant_insert = True
                continue
            if in_applicant_insert and ('INSERT INTO ApplicationDetail' in line or line == ''):
                break
            if in_applicant_insert and line.startswith("('") and line.endswith((',', ';')):
                clean_line = line.rstrip(',').rstrip(';')
                applicant_data.append(clean_line)
    except FileNotFoundError:
        print(f"❌ File {seed_file_path} tidak ditemukan")
        return []
    print(f"📊 Ditemukan {len(applicant_data)} data applicant dari seed.sql")
    return applicant_data

def generate_seeding_sql(cv_dir_path, seed_file_path, output_file='seeding.sql'):
    """Generate seeding.sql dengan CV files asli dan role dari PDF"""
    print("🔄 Generating seeding.sql...")
    cv_files = scan_cv_directory(cv_dir_path)
    if not cv_files:
        print("❌ Tidak ada CV ditemukan")
        return False
    applicant_data = read_existing_applicants(seed_file_path)
    if not applicant_data:
        print("❌ Tidak ada data applicant ditemukan")
        return False
    random.shuffle(cv_files)
    while len(cv_files) < len(applicant_data):
        cv_files.extend(cv_files)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Seeding data untuk ATS System\n")
        f.write("-- Data applicant dari seed.sql + CV files asli dengan role dari PDF\n")
        f.write("-- Generated automatically\n")
        f.write("USE ats_system;\n\n")
        f.write("-- Clear existing data\n")
        f.write("DELETE FROM ApplicationDetail;\n")
        f.write("DELETE FROM ApplicantProfile;\n\n")
        f.write("-- Insert Applicants\n")
        f.write("INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number, email) VALUES\n")
        for i, applicant_line in enumerate(applicant_data):
            comma = "," if i < len(applicant_data) - 1 else ";"
            f.write(f"{applicant_line}{comma}\n")
        f.write("\n")
        f.write("-- Insert Applications dengan CV files asli\n")
        f.write("INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path) VALUES\n")
        for i, applicant_line in enumerate(applicant_data):
            cv_file = cv_files[i % len(cv_files)]
            applicant_id = i + 1
            comma = "," if i < len(applicant_data) - 1 else ";"
            cv_path = cv_file['filename']
            f.write(f"({applicant_id}, '{cv_file['role']}', '{cv_path}'){comma}\n")
    print(f"✅ File {output_file} berhasil dibuat!")
    role_count = {}
    used_cvs = cv_files[:len(applicant_data)]
    for cv in used_cvs:
        role = cv['role']
        role_count[role] = role_count.get(role, 0) + 1
    print(f"\n📋 Role distribution:")
    for role, count in sorted(role_count.items()):
        print(f"   {role}: {count}")
    print(f"\n🎯 Summary:")
    print(f"   📊 Total applicants: {len(applicant_data)}")
    print(f"   📄 Total CV files: {len(cv_files)}")
    print(f"   🔗 Paired: {len(used_cvs)}")
    print(f"   📁 Output: {output_file}")
    return True

def main():
    
    cv_dir = CV_DIR
    seed_file = 'seed.sql'
    output_file = 'seeding.sql'

    # Allow override with config
    if os.path.exists(CV_DIR):
        cv_dir = CV_DIR

    if not os.path.exists(cv_dir):
        print(f"❌ CV directory tidak ditemukan: {cv_dir}")
        return

    if not os.path.exists(seed_file):
        print(f"❌ seed.sql tidak ditemukan: {seed_file}")
        return

    print(f"📁 CV Directory: {cv_dir}")
    print(f"📄 Seed File: {seed_file}")
    print(f"📤 Output: {output_file}")
    print("-" * 50)
    success = generate_seeding_sql(cv_dir, seed_file, output_file)
    if success:
        print(f"\n🚀 Cara menggunakan:")
        print(f"   mysql -u root -p ats_system < {output_file}")
        print(f"\n✅ File {output_file} siap digunakan!")
    else:
        print("❌ Gagal generate seeding.sql")

if __name__ == "__main__":
    main()
