import re
from typing import Dict, List, Any

DEFAULT_SKILLS = [
    "python", "java", "c++", "c#", "php", "sql", "html", "css", "javascript",
    "react", "node", "express", "django", "flask", "matlab", "golang", "docker",
    "linux", "git", "office", "excel", "powerpoint", "adobe", "figma"
]

def extract_email(text: str) -> str:
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text, re.I)
    return match.group() if match else ""

def extract_phone(text: str) -> str:
    match = re.search(r'(\+62|62|0)?[\s\-\.]?\d{8,15}', text)
    return match.group().replace(" ", "").replace("-", "").replace(".", "") if match else ""

def extract_name(text: str) -> str:
    lines = text.strip().split("\n")
    for i, line in enumerate(lines[:7]):
        if re.match(r'^[A-Za-z\s\-\.]+$', line) and 3 < len(line.strip()) < 50:
            if not any(c.isdigit() for c in line):
                return line.strip()
    match = re.search(r'(Name|Nama)\s*[:\-]\s*([A-Za-z\s\-\.]+)', text, re.I)
    if match:
        return match.group(2).strip()
    return ""

def extract_skills(text: str, skills: List[str]=None) -> List[str]:
    if skills is None:
        skills = DEFAULT_SKILLS
    found = []
    text_lower = text.lower()
    for skill in skills:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            found.append(skill)
    return found

def extract_education(text: str) -> List[Dict[str, str]]:
    """
    Cari pola pendidikan: universitas, gelar, tahun.
    """
    results = []
    edu_pattern = r'(universitas|institute|politeknik|sekolah tinggi|university)[\w\s\-\.]*[, ]+(s\d|sarjana|bachelor|master|magister|ph\.d)[\w\s\-\.]*[, ]+(\d{4})'
    for match in re.finditer(edu_pattern, text, re.I):
        results.append({
            "institution": match.group(0),
            "degree": match.group(2),
            "year": match.group(3)
        })
    for line in text.split("\n"):
        if re.search(r'(s1|s2|sarjana|master|bachelor|magister|ph\.d)', line, re.I) and re.search(r'\d{4}', line):
            results.append({"institution": line.strip()})
    return results

def extract_experience(text: str) -> List[Dict[str, str]]:
    """
    Cari pengalaman kerja berdasarkan pola: [posisi], [perusahaan], [tahun]
    """
    results = []
    exp_pattern = r'([\w\s\-\/]+)\s+(at|di)\s+([\w\s\-\.]+)[, ]+(\d{4})[\-–](\d{4}|present|sekarang)'
    for match in re.finditer(exp_pattern, text, re.I):
        results.append({
            "position": match.group(1).strip(),
            "company": match.group(3).strip(),
            "from": match.group(4),
            "to": match.group(5)
        })
    for line in text.split("\n"):
        if re.search(r'\d{4}[\-–](\d{4}|present|sekarang)', line, re.I):
            results.append({"experience": line.strip()})
    return results

def extract_summary(text: str) -> str:
    lines = text.strip().split("\n")
    buffer = []
    for line in lines[:15]: 
        if re.search(r'pendidikan|education|skill|keahlian|pengalaman|experience', line, re.I):
            break
        if line.strip() and len(line.strip()) > 15:
            buffer.append(line.strip())
    return " ".join(buffer)

def extract_applicant_info(text: str, skills: List[str]=None) -> Dict[str, Any]:
    """
    Ekstrak seluruh data penting dari teks CV.
    """
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text, skills),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "summary": extract_summary(text)
    }

# Contoh penggunaan
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <path_txt_cv>")
        exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()
    info = extract_applicant_info(text)
    from pprint import pprint
    pprint(info)
