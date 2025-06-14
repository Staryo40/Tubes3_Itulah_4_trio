from typing import List, Dict, Any
import os
from db import get_cv_list, test_connection
from scrapper import get_cv_text, get_cv_file_path
from extractor import extract_all_info

def get_all_cvs():
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
        return []

def get_cv_content(cv_path):
    try:
        return get_cv_text(cv_path)
    except Exception as e:
        return ""

def get_cv_summary(cv_path):
    try:
        cv_list = get_all_cvs()
        db_info = None
        
        for cv in cv_list:
            if cv["cv_path"] == cv_path:
                db_info = cv
                break
        
        cv_text = get_cv_content(cv_path)
        extracted = extract_all_info(cv_text) if cv_text else {}
        
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
        return create_empty_summary(cv_path)

def get_cv_info(cv_path):
    try:
        cv_text = get_cv_content(cv_path)
        if cv_text:
            return extract_all_info(cv_text)
        return {"success": False}
    except Exception as e:
        return {"success": False}

def get_cv_file(cv_path):
    try:
        return get_cv_file_path(cv_path)
    except Exception as e:
        return ""

def check_system():
    from config import CV_DIR
    
    status = {
        "database_ok": False,
        "cv_dir_exists": False,
        "total_cvs": 0,
        "system_ready": False
    }
    
    try:
        status["database_ok"] = test_connection()
        status["cv_dir_exists"] = os.path.exists(CV_DIR)
        
        if status["database_ok"]:
            cv_list = get_all_cvs()
            status["total_cvs"] = len(cv_list)
        
        status["system_ready"] = (
            status["database_ok"] and 
            status["cv_dir_exists"] and 
            status["total_cvs"] > 0
        )
        
    except Exception as e:
        pass
    
    return status

def create_empty_summary(cv_path):
    return {
        "applicant_name": "Error",
        "email": "",
        "role": "",
        "phone": "",
        "skills": [],
        "education": [],
        "experience": [],
        "summary": "",
        "cv_path": cv_path
    }