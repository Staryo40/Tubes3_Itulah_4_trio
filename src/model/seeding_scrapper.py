# seeding_scrapper.py - Update CV paths dengan role dari dalam PDF
import os
import random
from config import CV_DIR
from scrapper import extract_pdf_text

def extract_role_from_pdf(pdf_path):
    """Ekstrak role dari baris pertama PDF"""
    try:
        text = extract_pdf_text(pdf_path)
        if not text:
            return "Unknown Role"
        
        # Ambil baris pertama
        lines = text.strip().split('\n')
        if lines:
            first_line = lines[0].strip()
            
            # Format role: Title Case
            role = first_line.title()
            
            # Clean up jika ada karakter aneh
            role = role.replace('_', ' ').replace('-', ' ')
            
            return role
        
        return "Unknown Role"
    except Exception as e:
        print(f"Error ekstrak role dari {pdf_path}: {e}")
        return "Unknown Role"

def scan_cv_files_and_roles():
    """Scan folder CV dan ambil nama file + role dari PDF"""
    print("Scanning CV files dan ekstrak role dari PDF...")
    
    cv_files_with_roles = []
    
    # Scan langsung di CV_DIR (tidak ada subfolder)
    pdf_files = [f for f in os.listdir(CV_DIR) if f.lower().endswith('.pdf')]
    
    print(f"📁 Found {len(pdf_files)} PDF files in CV directory")
    
    for i, file in enumerate(pdf_files, 1):
        full_path = os.path.join(CV_DIR, file)
        
        print(f"[{i:4d}/{len(pdf_files)}] Ekstrak role dari: {file}")
        
        # Ekstrak role dari PDF
        role = extract_role_from_pdf(full_path)
        
        cv_files_with_roles.append({
            'filename': file,
            'role': role
        })
        
        print(f"       Role: {role}")
    
    print(f"\n📁 Total: {len(cv_files_with_roles)} file CV dengan role")
    return cv_files_with_roles

def generate_updated_seed_sql(cv_files_with_roles, output_file='updated_seed.sql'):
    """Update seed.sql yang sudah ada dengan CV files asli"""
    
    # Baca seed.sql yang sudah ada untuk ambil data ApplicantProfile
    seed_file = 'seed.sql'
    applicant_data = []
    
    try:
        with open(seed_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract data applicant dari INSERT statement yang ada
        lines = content.split('\n')
        for line in lines:
            if line.startswith("('") and "," in line:
                # Parse line format: ('Ahmad', 'Santoso', '1985-03-15', ...)
                line = line.strip().rstrip(',').rstrip(';')
                if line.startswith('(') and line.endswith(')'):
                    applicant_data.append(line)
                    
    except FileNotFoundError:
        print(f"❌ File {seed_file} tidak ditemukan")
        return False
    
    print(f"📊 Data applicant dari seed: {len(applicant_data)}")
    print(f"📄 CV files tersedia: {len(cv_files_with_roles)}")
    
    # Shuffle CV files untuk random assignment
    random.shuffle(cv_files_with_roles)
    
    # Pastikan jumlah CV cukup untuk semua applicant
    while len(cv_files_with_roles) < len(applicant_data):
        cv_files_with_roles.extend(cv_files_with_roles)  # Duplicate jika kurang
    
    # Generate SQL file baru
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Updated seed data dengan CV files asli dan role dari PDF\n")
        f.write("-- Data ApplicantProfile dari seed.sql + CV files + role dari teks PDF\n")
        f.write("USE ats_system;\n\n")
        
        # Clear existing data
        f.write("-- Clear existing data\n")
        f.write("DELETE FROM ApplicationDetail;\n")
        f.write("DELETE FROM ApplicantProfile;\n\n")
        
        # Insert applicants (copy dari seed.sql)
        f.write("-- Insert Applicants (dari seed.sql)\n")
        f.write("INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number, email) VALUES\n")
        
        for i, applicant_line in enumerate(applicant_data):
            comma = "," if i < len(applicant_data) - 1 else ";"
            f.write(f"{applicant_line}{comma}\n")
        
        f.write("\n")
        
        # Insert applications dengan CV files asli dan role dari PDF
        f.write("-- Insert Applications dengan CV files asli dan role dari PDF\n")
        f.write("INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path) VALUES\n")
        
        for i, applicant_line in enumerate(applicant_data):
            cv_file = cv_files_with_roles[i]  # Ambil CV sesuai urutan (sudah di-shuffle)
            applicant_id = i + 1
            
            comma = "," if i < len(applicant_data) - 1 else ";"
            cv_path = cv_file['filename']  # Langsung nama file saja
            
            f.write(f"({applicant_id}, '{cv_file['role']}', '{cv_path}'){comma}\n")
    
    print(f"✅ SQL file updated: {output_file}")
    
    # Print summary roles
    role_count = {}
    for cv in cv_files_with_roles[:len(applicant_data)]:
        role = cv['role']
        role_count[role] = role_count.get(role, 0) + 1
    
    print(f"\n📋 Role distribution (dari PDF):")
    for role, count in sorted(role_count.items()):
        print(f"   {role}: {count}")
    
    return True

def main():
    """Main function untuk update seeding data"""
    print("🔄 Updating seed data dengan role dari PDF...")
    
    # Scan CV files dan ekstrak role
    cv_files_with_roles = scan_cv_files_and_roles()
    
    if not cv_files_with_roles:
        print("❌ Tidak ada file CV ditemukan")
        return
    
    # Generate updated SQL
    success = generate_updated_seed_sql(cv_files_with_roles)
    
    if success:
        print(f"\n🎯 Hasil:")
        print(f"   ✅ Data identitas: Dari seed.sql")
        print(f"   ✅ CV files: Dari folder CV asli")
        print(f"   ✅ Roles: Dari baris pertama PDF")
        print(f"   ✅ Pairing: Random assignment")
        print(f"   📄 File: updated_seed.sql")
        print(f"   🚀 Run: mysql -u root -p ats_system < updated_seed.sql")
    else:
        print("❌ Gagal generate updated seed")

if __name__ == "__main__":
    main()