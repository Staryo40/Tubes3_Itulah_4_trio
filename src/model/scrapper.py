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
    """Cari semua file PDF"""
    search_dir = directory if directory else CV_DIR
    pdf_files = []
    
    try:
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        return sorted(pdf_files)
    except Exception as e:
        print(f"Error cari PDF: {e}")
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
    """Ambil teks CV berdasarkan path database"""
    # cv_path format: '/data/cv/filename.pdf'
    filename = cv_path.split('/')[-1]
    full_path = os.path.join(CV_DIR, filename)
    
    if os.path.exists(full_path):
        return extract_pdf_text(full_path)
    return ""

def get_cv_file_path(cv_path):
    """Konversi path database ke path file lengkap"""
    filename = cv_path.split('/')[-1]
    return os.path.join(CV_DIR, filename)

if __name__ == "__main__":
    files = find_pdf_files()
    print(f"Ditemukan {len(files)} file PDF")
    if files:
        text = extract_pdf_text(files[0])
        print(f"Test ekstraksi: {len(text)} karakter")