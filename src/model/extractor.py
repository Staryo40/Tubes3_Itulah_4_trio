import re
from typing import Dict, List, Any

# Daftar skill yang dicari
SKILLS = [
    "python", "java", "javascript", "c++", "c#", "php", "go", "rust",
    "html", "css", "react", "angular", "vue", "node", "express", "django",
    "sql", "mysql", "postgresql", "mongodb", "oracle", "redis",
    "docker", "kubernetes", "git", "linux", "aws", "azure", "jenkins",
    "pandas", "numpy", "tensorflow", "tableau", "excel", "powerbi",
    "figma", "adobe", "photoshop", "office", "powerpoint",
    "android", "ios", "flutter", "api", "rest", "agile", "scrum"
]

def extract_email(text):
    """Ekstrak email dari teks"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group().strip() if match else ""

def extract_phone(text):
    """Ekstrak nomor telepon"""
    patterns = [
        r'(\+62|62|0)[\s\-\.]?8\d{2}[\s\-\.]?\d{3,4}[\s\-\.]?\d{3,4}',
        r'(\+62|62|0)[\s\-\.]?\d{2,3}[\s\-\.]?\d{3,4}[\s\-\.]?\d{3,4}',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            phone = re.sub(r'[\s\-\.]', '', match.group())
            return phone
    return ""

def extract_name(text):
    """Ekstrak nama dari CV"""
    lines = text.strip().split('\n')
    
    for line in lines[:8]:
        line = line.strip()
        if 3 < len(line) < 50 and re.match(r'^[A-Za-z\s\.\-]+$', line):
            if not any(c.isdigit() for c in line):
                cv_words = ['curriculum', 'vitae', 'resume', 'cv', 'contact']
                if not any(word in line.lower() for word in cv_words):
                    words = line.split()
                    if 2 <= len(words) <= 4:
                        return line.strip()
    
    # Fallback pattern
    name_pattern = r'(name|nama)\s*[:\-]\s*([A-Za-z\s\.\-]+)'
    match = re.search(name_pattern, text, re.IGNORECASE)
    if match:
        return match.group(2).strip()
    
    return ""

def extract_skills(text, custom_skills=None):
    """Ekstrak keahlian dari teks"""
    skills_list = custom_skills if custom_skills else SKILLS
    found_skills = []
    text_lower = text.lower()
    normalized = re.sub(r'[^\w\s]', ' ', text_lower)
    
    for skill in skills_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, normalized):
            found_skills.append(skill)
    
    return sorted(list(set(found_skills)))

def extract_education(text):
    """Ekstrak informasi pendidikan"""
    education_list = []
    patterns = [
        r'(universitas|university|institute|politeknik|sekolah tinggi)',
        r'(bachelor|master|sarjana|magister|s1|s2|s3|d3|d4)'
    ]
    year_pattern = r'(19|20)\d{2}'
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if len(line) < 5:
            continue
        
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                edu_info = {"institution": line}
                
                # Cari tahun
                years = re.findall(year_pattern, line)
                if years:
                    edu_info["year"] = years[-1]
                
                # Cari gelar
                degree_pattern = r'(bachelor|master|sarjana|s1|s2|s3|d3|d4)'
                degree_match = re.search(degree_pattern, line, re.IGNORECASE)
                if degree_match:
                    edu_info["degree"] = degree_match.group().strip()
                
                education_list.append(edu_info)
                break
    
    return education_list

def extract_experience(text):
    """Ekstrak pengalaman kerja"""
    experience_list = []
    
    # Pattern untuk pengalaman
    patterns = [
        r'([\w\s\-\/]+)\s+(at|di)\s+([\w\s\-\.&]+)[\s,]*(\d{4})[\s\-–]*(\d{4}|present)',
        r'(\d{4})[\s\-–]+(\d{4}|present)[\s:]*([^\n]+)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            groups = match.groups()
            if len(groups) >= 3:
                exp_info = {}
                if 'at' in match.group().lower() or 'di' in match.group().lower():
                    exp_info["position"] = groups[0].strip()
                    exp_info["company"] = groups[2].strip()
                    if len(groups) > 3:
                        exp_info["year"] = groups[3]
                else:
                    exp_info["description"] = match.group().strip()
                
                experience_list.append(exp_info)
    
    return experience_list[:5]

def extract_summary(text):
    """Ekstrak ringkasan CV"""
    lines = text.strip().split('\n')
    summary_lines = []
    
    section_words = ['education', 'pendidikan', 'experience', 'skill', 'keahlian']
    
    for line in lines[:12]:
        line = line.strip()
        if len(line) < 15:
            continue
        if any(word in line.lower() for word in section_words):
            break
        if re.search(r'@|\+|\d{4}', line):
            continue
        if 20 < len(line) < 250:
            summary_lines.append(line)
    
    summary = ' '.join(summary_lines)
    return summary[:600] if len(summary) > 600 else summary

def extract_all_info(text, custom_skills=None):
    """Ekstrak semua informasi dari CV"""
    if not text or not text.strip():
        return {
            "name": "", "email": "", "phone": "", "skills": [],
            "education": [], "experience": [], "summary": "", "success": False
        }
    
    try:
        result = {
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": extract_skills(text, custom_skills),
            "education": extract_education(text),
            "experience": extract_experience(text),
            "summary": extract_summary(text),
            "success": True
        }
        
        # Validasi minimal
        if not any([result["name"], result["email"], result["phone"]]):
            result["success"] = False
        
        return result
    except Exception as e:
        print(f"Error ekstraksi: {e}")
        return {
            "name": "", "email": "", "phone": "", "skills": [],
            "education": [], "experience": [], "summary": "", "success": False
        }

# Fungsi untuk kompatibilitas
def extract_applicant_info(text, skills=None):
    """Fungsi kompatibilitas dengan kode lama"""
    return extract_all_info(text, skills)

if __name__ == "__main__":
    sample = """
    John Doe
    Software Engineer
    john@email.com
    +628123456789
    
    Experienced developer with Python, JavaScript, React skills.
    """
    result = extract_all_info(sample)
    print("Test ekstraksi:")
    for key, value in result.items():
        print(f"  {key}: {value}")