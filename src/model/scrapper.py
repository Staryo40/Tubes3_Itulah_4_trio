# scrapper.py - Ekstraksi teks dari PDF
import os
from typing import Dict, List
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
        print(f"Error baca PDF {file_path}: {e}")
        return ""

def clean_text(raw_text):
    """Bersihkan teks hasil ekstraksi"""
    if not raw_text:
        return ""
    
    import re
    # Hapus karakter aneh
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', raw_text)
    # Normalisasi whitespace
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
    cleaned = re.sub(r' +', ' ', cleaned)
    
    return cleaned.strip()

def find_pdf_files(directory=None):
    """Cari semua file PDF langsung di direktori utama"""
    search_dir = directory if directory else CV_DIR
    pdf_files = []
    
    try:
        if not os.path.exists(search_dir):
            print(f"Direktori tidak ditemukan: {search_dir}")
            return []
        
        # Scan langsung di direktori utama (tidak ada subfolder)
        for file in os.listdir(search_dir):
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(search_dir, file)
                pdf_files.append(full_path)
        
        print(f"Ditemukan {len(pdf_files)} file PDF di {search_dir}")
        return sorted(pdf_files)
        
    except Exception as e:
        print(f"Error mencari file PDF: {e}")
        return []

def process_all_pdfs():
    """Proses semua PDF di direktori"""
    pdf_files = find_pdf_files()
    results = {}
    
    for pdf_path in pdf_files:
        text = extract_pdf_text(pdf_path)
        if text:
            results[pdf_path] = text
    
    return results

def get_cv_text(cv_path):
    """Ambil teks CV berdasarkan nama file"""
    # cv_path sekarang langsung nama file: '57088974.pdf'
    filename = cv_path
    full_path = os.path.join(CV_DIR, filename)
    
    if os.path.exists(full_path):
        return extract_pdf_text(full_path)
    else:
        print(f"File PDF tidak ditemukan: {filename}")
        return ""

def get_cv_file_path(cv_path):
    """Konversi nama file ke path lengkap"""
    # cv_path sekarang langsung nama file: '57088974.pdf'
    filename = cv_path
    return os.path.join(CV_DIR, filename)

if __name__ == "__main__":
    files = find_pdf_files()
    print(f"Ditemukan {len(files)} file PDF")
    if files:
        text = extract_pdf_text(files[0])
        print(f"Test ekstraksi: {len(text)} karakter")