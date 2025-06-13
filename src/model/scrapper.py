import os
from typing import Dict, List, Tuple
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Ekstrak seluruh teks dari 1 file PDF.
    """
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"❌ Error membaca {pdf_path}: {e}")
    return text

def find_all_pdf_files(root_dir: str) -> List[str]:
    """
    Cari semua file .pdf di root_dir dan seluruh subfoldernya.
    """
    pdf_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(dirpath, filename))
    return pdf_files

def batch_extract_pdf(root_dir: str, save_txt_dir: str = None) -> Dict[str, str]:
    """
    Ekstrak semua PDF di root_dir (dan subfolder), hasil dalam dict {pdf_path: teks}
    Jika save_txt_dir diisi, hasil juga disimpan dalam file .txt dengan struktur mirip source.
    """
    pdf_paths = find_all_pdf_files(root_dir)
    results = {}
    for pdf_path in pdf_paths:
        print(f"🔎 Mengekstrak {pdf_path} ...")
        text = extract_text_from_pdf(pdf_path)
        results[pdf_path] = text
        if save_txt_dir:
            # Buat struktur folder yang sama dengan source
            rel_path = os.path.relpath(pdf_path, root_dir)
            txt_path = os.path.join(save_txt_dir, rel_path)
            txt_path = txt_path.replace(".pdf", ".txt")
            os.makedirs(os.path.dirname(txt_path), exist_ok=True)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
    print(f"✅ Selesai ekstrak {len(pdf_paths)} file PDF.")
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scrapper.py <folder_pdf> [folder_output_txt]")
        exit(1)
    folder_pdf = sys.argv[1]
    folder_out = sys.argv[2] if len(sys.argv) >= 3 else None
    batch_extract_pdf(folder_pdf, folder_out)
