from typing import List, Dict, Any
import os
from db import get_cv_list, test_connection
from scrapper import get_cv_text, get_cv_file_path
from extractor import extract_all_info

# ============= UNTUK SEARCH ALGORITHM =============

def get_all_cvs():
    """
    Ambil daftar CV untuk pencarian
    Returns: List[Dict] dengan format:
    [{"cv_path": str, "name": str, "email": str, "role": str}]
    """
    try:
        raw_data = get_cv_list()
        cv_data = []
        
        for cv in raw_data:
            cv_info = {
                "detail_id": cv["detail_id"],
                "cv_path": cv["cv_path"],
                "applicant_id": cv["applicant_id"],
                "name": f"{cv['first_name']} {cv['last_name']}",
                "email": cv["email"],
                "role": cv["application_role"]
            }
            cv_data.append(cv_info)
        
        return cv_data
    except Exception as e:
        print(f"Error ambil CV data: {e}")
        return []

def get_cv_content(cv_path):
    """
    Ambil teks CV untuk pattern matching
    Args: cv_path dari database ("/data/cv/filename.pdf")
    Returns: String teks CV
    """
    try:
        return get_cv_text(cv_path)
    except Exception as e:
        print(f"Error ambil teks CV: {e}")
        return ""

# ============= UNTUK GUI =============

def get_cv_summary(cv_path):
    """
    Ambil summary CV untuk display GUI
    Returns: Dict dengan info lengkap untuk tampilan
    """
    try:
        # Ambil data dari database
        cv_list = get_all_cvs()
        db_info = None
        for cv in cv_list:
            if cv["cv_path"] == cv_path:
                db_info = cv
                break
        
        # Ambil info hasil ekstraksi
        extracted = get_cv_info(cv_path)
        
        # Gabungkan info
        summary = {
            "applicant_name": db_info["name"] if db_info else extracted.get("name", "Unknown"),
            "email": db_info["email"] if db_info else extracted.get("email", ""),
            "role": db_info["role"] if db_info else "Unknown",
            "phone": extracted.get("phone", ""),
            "skills": extracted.get("skills", []),
            "education": extracted.get("education", []),
            "experience": extracted.get("experience", []),
            "summary": extracted.get("summary", ""),
            "cv_path": cv_path
        }
        
        return summary
    except Exception as e:
        print(f"Error buat summary: {e}")
        return {
            "applicant_name": "Error", "email": "", "role": "",
            "phone": "", "skills": [], "education": [], "experience": [],
            "summary": "", "cv_path": cv_path
        }

def get_cv_info(cv_path):
    """Ambil info hasil ekstraksi CV"""
    try:
        cv_text = get_cv_content(cv_path)
        if cv_text:
            return extract_all_info(cv_text)
        return {"success": False}
    except Exception as e:
        print(f"Error ekstraksi info: {e}")
        return {"success": False}

def get_cv_file(cv_path):
    """Ambil path lengkap file CV untuk viewer"""
    try:
        return get_cv_file_path(cv_path)
    except Exception as e:
        print(f"Error ambil path file: {e}")
        return ""

# ============= UTILITY =============

def check_system():
    """Cek status sistem"""
    from config import CV_DIR
    
    status = {
        "database_ok": False,
        "cv_dir_exists": False,
        "total_cvs": 0,
        "system_ready": False
    }
    
    try:
        # Cek database
        status["database_ok"] = test_connection()
        
        # Cek direktori CV
        status["cv_dir_exists"] = os.path.exists(CV_DIR)
        
        # Hitung CV
        if status["cv_dir_exists"]:
            cv_list = get_all_cvs()
            status["total_cvs"] = len(cv_list)
        
        # Status ready
        status["system_ready"] = (
            status["database_ok"] and 
            status["cv_dir_exists"] and 
            status["total_cvs"] > 0
        )
        
    except Exception as e:
        print(f"Error cek sistem: {e}")
    
    return status

def test_integration():
    """Test integrasi sistem"""
    print("Test integrasi...")
    
    # Test status
    status = check_system()
    print(f"Database: {'OK' if status['database_ok'] else 'Error'}")
    print(f"CV Dir: {'OK' if status['cv_dir_exists'] else 'Error'}")
    print(f"Total CVs: {status['total_cvs']}")
    
    if not status['system_ready']:
        print("Sistem belum siap")
        return False
    
    # Test dengan CV pertama
    cv_list = get_all_cvs()
    if cv_list:
        test_cv = cv_list[0]
        cv_path = test_cv["cv_path"]
        
        # Test ekstraksi teks
        text = get_cv_content(cv_path)
        print(f"Ekstraksi teks: {len(text)} karakter")
        
        # Test summary
        summary = get_cv_summary(cv_path)
        print(f"Summary untuk: {summary['applicant_name']}")
        
        print("Test berhasil!")
        return True
    
    print("Tidak ada CV untuk test")
    return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_integration()
    else:
        status = check_system()
        print("Status sistem:")
        for key, value in status.items():
            print(f"  {key}: {value}")