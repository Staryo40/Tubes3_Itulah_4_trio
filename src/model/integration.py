from typing import Dict, Any, List
from .db import get_cv_list
from .config import CV_DIR
import os

def get_data() -> Dict[int, Dict[str, Any]]:
    try:
        raw_data = get_cv_list()
        result = {}
        for row in raw_data:
            applicant_id = row["applicant_id"]
            data = {k: v for k, v in row.items() if k != "applicant_id"}
            result[applicant_id] = data
        return result
    except Exception as e:
        print(f"Error getting data: {e}")
        return {}

def get_cv_path(cv_filename: str) -> str:
    return os.path.join(CV_DIR, cv_filename)

def get_applicant_by_id(applicant_id: int) -> Dict[str, Any]:
    """
    Get applicant data by ID
    Args:
        applicant_id: ID applicant
    Returns:
        Dict berisi data applicant atau empty dict jika tidak ditemukan
    """
    data = get_data()
    return data.get(applicant_id, {})

def get_all_cv_files() -> List[str]:
    """
    Get list of all CV files from directory
    Returns:
        List nama file CV yang ada di direktori
    """
    try:
        if not os.path.exists(CV_DIR):
            print(f"CV directory tidak ditemukan: {CV_DIR}")
            return []
        
        cv_files = [f for f in os.listdir(CV_DIR) if f.lower().endswith('.pdf')]
        return sorted(cv_files)
    except Exception as e:
        print(f"Error getting CV files: {e}")
        return []

def validate_cv_paths() -> Dict[str, bool]:
    """
    Validate semua CV path yang ada di database
    Returns:
        Dict dengan cv_path sebagai key dan boolean (exists) sebagai value
    """
    data = get_data()
    results = {}
    
    for applicant_id, info in data.items():
        cv_path = info.get('cv_path', '')
        full_path = get_cv_path(cv_path)
        exists = os.path.exists(full_path)
        results[cv_path] = exists
        
        if not exists:
            print(f"⚠️  CV not found: {cv_path} (Applicant ID: {applicant_id})")
    
    return results

def get_stats() -> Dict[str, Any]:
    """
    Returns:
        Dict berisi statistik data
    """
    data = get_data()
    cv_files = get_all_cv_files()
    validation = validate_cv_paths()
    
    valid_cvs = sum(1 for exists in validation.values() if exists)
    invalid_cvs = len(validation) - valid_cvs
    
    roles = {}
    for info in data.values():
        role = info.get('application_role', 'Unknown')
        roles[role] = roles.get(role, 0) + 1
    
    return {
        'total_applicants': len(data),
        'total_cv_files_in_dir': len(cv_files),
        'valid_cv_paths': valid_cvs,
        'invalid_cv_paths': invalid_cvs,
        'roles_distribution': roles,
        'cv_directory': CV_DIR,
        'cv_dir_exists': os.path.exists(CV_DIR)
    }

"""
Format output get_data():
{
  applicant_id: {
    "first_name": str,
    "last_name": str,
    "date_of_birth": date,
    "email": str,
    "phone_number": str,
    "address": str,
    "detail_id": int,
    "application_role": str,
    "cv_path": str,  # hanya nama file: "12345.pdf"
  }, ...
}

Usage examples:
- data = get_data()
- applicant = get_applicant_by_id(1)
- full_cv_path = get_cv_path(applicant['cv_path'])
- stats = get_stats()
"""

if __name__ == "__main__":
    print("=== Testing Integration ===")
    
    data = get_data()
    print(f"Total applicants: {len(data)}")
    
    if data:
        first_id = list(data.keys())[0]
        first_applicant = data[first_id]
        print(f"\nFirst applicant (ID {first_id}):")
        for key, value in first_applicant.items():
            print(f"  {key}: {value}")
        
        cv_path = first_applicant.get('cv_path', '')
        if cv_path:
            full_path = get_cv_path(cv_path)
            exists = os.path.exists(full_path)
            print(f"\nCV Path: {cv_path}")
            print(f"Full Path: {full_path}")
            print(f"Exists: {exists}")
    
    print(f"\n=== Statistics ===")
    stats = get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")