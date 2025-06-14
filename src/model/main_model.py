# Struktur Result
# {
#   "time": val,
#   "cv_num": val, -> total number of cv scanned
#   "result": {
#              "cv_id": {
#                        "name": val,
#                        "dob": val,
#                        "address": val,
#                        "phone": val,
#                        "role": val,
#                        "path": val,
#                        "total_match": val,
#                        "exact_match": val,
#                        "fuzzy_match": val,
#                        "search_res": {
#                                       "keyword": { 
#                                                    "type": tval, -> tval = keyword_result ENUM
#                                                    "occurrence": val
#                                                  }
#                                      }
#                        "summary": summarystruct,
#                       }
#              }
# }


class MainModel:
    def __init__(self):
        self.candidates_data = []
        self.current_page = 0
        self.cards_per_page = 6
        
    def load_sample_data(self):
        """Load sample candidate data"""
        return  {
            "time": 100,
            "cv_num": 8,
            "result": {
                1: {
                    "name": "Farhan",
                    "birthdate": "1995-05-15",
                    "Address": "Jl. Merdeka No. 10, Jakarta",
                    "Phone": "0812-3456-7890",
                    "matches": 4,
                    "search_res": {
                        "React": {"type": "exact", "occurrence": 2},
                        "Express": {"type": "fuzzy", "occurrence": 1},
                        "HTML": {"type": "exact", "occurrence": 1}
                    },
                    "summary": [
                        {"header": "Skill", "type": "Bullet", "content": ["React", "Express", "HTML"]},
                        {"header": "Job History", "type": "List", "content": ["Software Engineer at ABC Corp", "Frontend Developer at XYZ Ltd"]},
                        {"header": "Education", "type": "List", "content": ["Bachelor's Degree in Computer Science, University of Technology"]}
                    ],
                    "view_path": "D:\\Repository\\Tubes3_Itulah_4_trio\\data\\pdf\\dummy.pdf"
                },
                2: {
                    "name": "Aulia",
                    "birthdate": "1994-07-20",
                    "Address": "Jl. Sudirman No. 50, Bandung",
                    "Phone": "0813-9876-5432",
                    "matches": 3,
                    "search_res": {
                        "JavaScript": {"type": "exact", "occurrence": 2},
                        "Node.js": {"type": "fuzzy", "occurrence": 1},
                        "CSS": {"type": "exact", "occurrence": 1}
                    },
                    "summary": [
                        {"header": "Skill", "type": "Bullet", "content": ["JavaScript", "Node.js", "CSS"]},
                        {"header": "Job History", "type": "List", "content": ["Backend Developer at DEF Inc", "Fullstack Developer at GHI Ltd"]},
                        {"header": "Education", "type": "List", "content": ["Bachelor's Degree in Information Systems, Institute of Technology"]}
                    ],
                    "view_path": "D:\\Repository\\Tubes3_Itulah_4_trio\\data\\pdf\\dummy2.pdf"
                },
                3: {
                    "name": "Rizky",
                    "birthdate": "1996-09-12",
                    "Address": "Jl. Diponegoro No. 21, Surabaya",
                    "Phone": "0811-2233-4455",
                    "matches": 5,
                    "search_res": {
                        "Python": {"type": "exact", "occurrence": 3},
                        "Django": {"type": "exact", "occurrence": 1},
                        "SQL": {"type": "fuzzy", "occurrence": 1}
                    },
                    "summary": [
                        {"header": "Skill", "type": "Bullet", "content": ["Python", "Django", "SQL"]},
                        {"header": "Job History", "type": "List", "content": ["Data Analyst at JKL Ltd", "Backend Developer at MNO Corp"]},
                        {"header": "Education", "type": "List", "content": ["Master's Degree in Data Science, National University"]}
                    ],
                    "view_path": "D:\\Repository\\Tubes3_Itulah_4_trio\\data\\pdf\\dummy3.pdf"
                },
                4: {
                    "name": "Sarah",
                    "birthdate": "1993-03-08",
                    "Address": "Jl. Gatot Subroto No. 5, Medan",
                    "Phone": "0814-5678-9101",
                    "matches": 2,
                    "search_res": {
                        "C++": {"type": "exact", "occurrence": 2},
                        "OpenGL": {"type": "fuzzy", "occurrence": 1}
                    },
                    "summary": [
                        {"header": "Skill", "type": "Bullet", "content": ["C++", "OpenGL"]},
                        {"header": "Job History", "type": "List", "content": ["Game Developer at PQR Studio"]},
                        {"header": "Education", "type": "List", "content": ["Bachelor's Degree in Game Development, Gaming University"]}
                    ],
                    "view_path": "D:\\Repository\\Tubes3_Itulah_4_trio\\data\\pdf\\dummy4.pdf"
                },
                5: {
                    "name": "Andi",
                    "birthdate": "1992-11-11",
                    "Address": "Jl. Ahmad Yani No. 99, Malang",
                    "Phone": "0815-1122-3344",
                    "matches": 6,
                    "search_res": {
                        "Java": {"type": "exact", "occurrence": 3},
                        "Spring": {"type": "exact", "occurrence": 2},
                        "MySQL": {"type": "fuzzy", "occurrence": 1}
                    },
                    "summary": [
                        {"header": "Skill", "type": "Bullet", "content": ["Java", "Spring", "MySQL"]},
                        {"header": "Job History", "type": "List", "content": ["Software Developer at STU Ltd", "Senior Engineer at VWX Inc"]},
                        {"header": "Education", "type": "List", "content": ["Bachelor's Degree in Software Engineering, Polytechnic University"]}
                    ],
                    "view_path": "D:\\Repository\\Tubes3_Itulah_4_trio\\data\\pdf\\dummy5.pdf"
                },
                6: {
                    "name": "Nina",
                    "birthdate": "1997-06-14",
                    "Address": "Jl. Imam Bonjol No. 45, Yogyakarta",
                    "Phone": "0816-7890-1234",
                    "matches": 4,
                    "search_res": {
                        "Ruby": {"type": "exact", "occurrence": 2},
                        "Rails": {"type": "fuzzy", "occurrence": 1},
                        "JavaScript": {"type": "exact", "occurrence": 1}
                    },
                    "summary": [
                        {"header": "Skill", "type": "Bullet", "content": ["Ruby", "Rails", "JavaScript"]},
                        {"header": "Job History", "type": "List", "content": ["Web Developer at YZA Corp", "Frontend Engineer at BCD Inc"]},
                        {"header": "Education", "type": "List", "content": ["Bachelor's Degree in Computer Engineering, Regional University"]}
                    ],
                    "view_path": "D:\\Repository\\Tubes3_Itulah_4_trio\\data\\pdf\\dummy6.pdf"
                },
                7: {
                    "name": "Budi",
                    "birthdate": "1990-01-22",
                    "Address": "Jl. Pemuda No. 88, Semarang",
                    "Phone": "0817-4444-5555",
                    "matches": 3,
                    "search_res": {
                        "PHP": {"type": "exact", "occurrence": 2},
                        "Laravel": {"type": "fuzzy", "occurrence": 1}
                    },
                    "summary": [
                        {"header": "Skill", "type": "Bullet", "content": ["PHP", "Laravel"]},
                        {"header": "Job History", "type": "List", "content": ["Backend Developer at EFG Studio", "Lead Engineer at HIJ Ltd"]},
                        {"header": "Education", "type": "List", "content": ["Bachelor's Degree in Information Technology, National Institute"]}
                    ],
                    "view_path": "D:\\Repository\\Tubes3_Itulah_4_trio\\data\\pdf\\dummy7.pdf"
                },
                8: {
                    "name": "Siti",
                    "birthdate": "1998-04-18",
                    "Address": "Jl. Gajah Mada No. 56, Bali",
                    "Phone": "0818-2222-6666",
                    "matches": 5,
                    "search_res": {
                        "Kotlin": {"type": "exact", "occurrence": 3},
                        "Android": {"type": "fuzzy", "occurrence": 2}
                    },
                    "summary": [
                        {"header": "Skill", "type": "Bullet", "content": ["Kotlin", "Android"]},
                        {"header": "Job History", "type": "List", "content": ["Mobile Developer at KLM Studio", "Junior Developer at NOP Corp"]},
                        {"header": "Education", "type": "List", "content": ["Bachelor's Degree in Mobile Application Development, International University"]}
                    ],
                    "view_path": "D:\\Repository\\Tubes3_Itulah_4_trio\\data\\pdf\\dummy8.pdf"
                }
            }
        }
            
    # ... rest of the methods remain the same
    def get_candidates_for_page(self):
        """Get candidates for current page"""
        start = self.current_page * self.cards_per_page
        end = min(start + self.cards_per_page, len(self.candidates_data))
        return list(self.candidates_data)[start:end]

    def get_total_pages(self):
        """Get total number of pages"""
        return (len(self.candidates_data) + self.cards_per_page - 1) // self.cards_per_page

    def can_go_previous(self):
        """Check if can go to previous page"""
        return self.current_page > 0
    
    def can_go_next(self):
        """Check if can go to next page"""
        return self.current_page < self.get_total_pages() - 1
    
    def go_previous_page(self):
        """Go to previous page"""
        if self.can_go_previous():
            self.current_page -= 1
            return True
        return False
    
    def go_next_page(self):
        """Go to next page"""
        if self.can_go_next():
            self.current_page += 1
            return True
        return False
    
    def search_candidates(self, keywords, algorithm, top_matches):
        """Perform search with given parameters"""
        # Implement actual search logic here
        print(f"Searching for: {keywords} using {algorithm}, top {top_matches} matches")
        # For now, just return all data
        return self.load_sample_data()


