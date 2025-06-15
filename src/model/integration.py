from typing import Dict, Any, List
from .db import get_cv_list
from .config import CV_DIR
import os

def get_data() -> Dict[int, Dict[str, Any]]:
    try:
        raw_data = get_cv_list()
        result = {}
        for row in raw_data:
            detail_id = row["detail_id"]
            data = {k: v for k, v in row.items() if k != "detail_id"}
            result[detail_id] = data
        return result
    except Exception as e:
        print(f"Error getting data: {e}")
        return {}

def get_cv_path(cv_filename: str) -> str:
    """
    UPDATED: Handle full path dari tubes3_seeding.sql
    Format path dari seeding: 'data/INFORMATION-TECHNOLOGY/15118506.pdf'
    """
    # Jika cv_filename sudah berupa full path (dari tubes3_seeding.sql)
    if cv_filename.startswith('data/'):
        # Konversi ke absolute path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, cv_filename)
    
    # Jika hanya nama file, join dengan CV_DIR (backward compatibility)
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
    UPDATED: Scan rekursif untuk mendukung struktur folder tubes3_seeding.sql
    """
    try:
        cv_files = []
        
        # Scan struktur folder sesuai tubes3_seeding.sql
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data')
        
        if not os.path.exists(data_dir):
            print(f"Data directory tidak ditemukan: {data_dir}")
            return []
        
        # Scan semua subfolder dalam data/
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    # Buat relative path dari base directory
                    relative_path = os.path.relpath(os.path.join(root, file), base_dir)
                    cv_files.append(relative_path.replace(os.sep, '/'))  # Normalize separator
        
        return sorted(cv_files)
    except Exception as e:
        print(f"Error getting CV files: {e}")
        return []

def validate_cv_paths() -> Dict[str, bool]:
    """
    Validate semua CV path yang ada di database
    UPDATED: Support format path tubes3_seeding.sql
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
            print(f"    Expected path: {full_path}")
    
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
        if role is None:
            role = 'NULL'
        roles[role] = roles.get(role, 0) + 1
    
    return {
        'total_applicants': len(data),
        'total_cv_files_in_dir': len(cv_files),
        'valid_cv_paths': valid_cvs,
        'invalid_cv_paths': invalid_cvs,
        'roles_distribution': roles,
        'cv_directory': os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data'
    }

def debug_cv_paths():
    """
    Debug function untuk memverifikasi path CV
    """
    print("=== DEBUG CV PATHS ===")
    data = get_data()
    
    print(f"Total applicants in DB: {len(data)}")
    print("\nSample CV paths from database:")
    
    for i, (applicant_id, info) in enumerate(data.items()):
        if i >= 5:  # Hanya tampilkan 5 sample
            break
            
        cv_path = info.get('cv_path', '')
        full_path = get_cv_path(cv_path)
        exists = os.path.exists(full_path)
        
        print(f"  ID {applicant_id}: {cv_path}")
        print(f"    Full path: {full_path}")
        print(f"    Exists: {exists}")
        print()
    
    print("CV files found in directory:")
    cv_files = get_all_cv_files()
    print(f"  Total: {len(cv_files)}")
    if cv_files:
        print(f"  Sample: {cv_files[0]}")

if __name__ == "__main__":
    debug_cv_paths()