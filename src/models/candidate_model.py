class CandidateModel:
    def __init__(self):
        self.candidates_data = []
        self.current_page = 0
        self.cards_per_page = 6
        
    def load_sample_data(self):
        """Load sample candidate data"""
        self.candidates_data = [
            {
                "name": "Farhan",
                "birthdate": "1995-05-15",
                "Address": "Jl. Merdeka No. 10, Jakarta",
                "Phone": "0812-3456-7890",
                "matches": 4,
                "matches_keywords": [
                    {"keyword": "React", "occurrences": 1},
                    {"keyword": "Express", "occurrences": 2},
                    {"keyword": "HTML", "occurrences": 1}
                ],
                "summary": [
                    {
                        "header": "Skill",
                        "type": "Bullet",
                        "content": [
                            "React",
                            "Express",
                            "HTML"
                        ]
                    },
                    {
                        "header": "Job History",
                        "type": "List",
                        "content": [
                            "Software Engineer at ABC Corp",
                            "Frontend Developer at XYZ Ltd"
                        ]
                    },
                    {
                        "header": "Education",
                        "type": "List",
                        "content": [
                            "Bachelor's \nDegree in Computer Science, University of Technology"
                        ]
                    }
                ],
                "view_path": "D:\Repository\Tubes3_Itulah_4_trio\data\pdf\dummy.pdf"
            },
            {
                "name": "Aland",
                "matches": 1,
                "matches_keywords": [
                    {"keyword": "React", "occurrences": 1}
                ],
                "summary": {
                    "Skill": ["React"],
                    "Job History": ["Junior Developer at XYZ Corp"],
                    "Education": ["Informatics Engineering, Institute of Technology"]
                },
                "view_path": "../../data/pdf/dummy.pdf"
            },
            {
                "name": "Ariel",
                "matches": 1,
                "matches_keywords": [
                    {"keyword": "Express", "occurrences": 1}
                ],
                "summary_path": "path/to/summary_ariel.json",
                "view_path": "path/to/view_ariel.json"
            },
            {
                "name": "Alice",
                "matches": 4,
                "matches_keywords": [
                    {"keyword": "React", "occurrences": 2},
                    {"keyword": "JavaScript", "occurrences": 1},
                    {"keyword": "CSS", "occurrences": 2}
                ],
                "summary_path": "path/to/summary_alice.json",
                "view_path": "path/to/view_alice.json"
            },
            {
                "name": "Bob",
                "matches": 3,
                "matches_keywords": [
                    {"keyword": "Python", "occurrences": 1},
                    {"keyword": "C++", "occurrences": 2}
                ],
                "summary_path": "path/to/summary_bob.json",
                "view_path": "path/to/view_bob.json"
            },
            {
                "name": "Charlie",
                "matches": 5,
                "matches_keywords": [
                    {"keyword": "Java", "occurrences": 3},
                    {"keyword": "SQL", "occurrences": 2}
                ],
                "summary_path": "path/to/summary_charlie.json",
                "view_path": "path/to/view_charlie.json"
            },
            # TAMBAHAN DUA CANDIDATE BARU
            {
                "name": "Diana",
                "matches": 6,
                "matches_keywords": [
                    {"keyword": "React", "occurrences": 2},
                    {"keyword": "Node.js", "occurrences": 3},
                    {"keyword": "MongoDB", "occurrences": 1}
                ],
                "summary_path": "path/to/summary_diana.json",
                "view_path": "path/to/view_diana.json"
            },
            {
                "name": "Edward",
                "matches": 2,
                "matches_keywords": [
                    {"keyword": "Vue.js", "occurrences": 1},
                    {"keyword": "TypeScript", "occurrences": 1}
                ],
                "summary_path": "path/to/summary_edward.json",
                "view_path": "path/to/view_edward.json"
            },
            # CANDIDATE DENGAN BANYAK KEYWORDS UNTUK TESTING SCROLL
            {
                "name": "Sarah",
                "matches": 15,
                "matches_keywords": [
                    {"keyword": "React", "occurrences": 3},
                    {"keyword": "Vue.js", "occurrences": 2},
                    {"keyword": "Angular", "occurrences": 1},
                    {"keyword": "JavaScript", "occurrences": 4},
                    {"keyword": "TypeScript", "occurrences": 2},
                    {"keyword": "Node.js", "occurrences": 3},
                    {"keyword": "Express", "occurrences": 2},
                    {"keyword": "MongoDB", "occurrences": 1},
                    {"keyword": "PostgreSQL", "occurrences": 2},
                    {"keyword": "HTML", "occurrences": 1},
                    {"keyword": "CSS", "occurrences": 2},
                    {"keyword": "SASS", "occurrences": 1},
                    {"keyword": "Docker", "occurrences": 1},
                    {"keyword": "AWS", "occurrences": 1},
                    {"keyword": "Git", "occurrences": 1}
                ],
                "summary_path": "path/to/summary_sarah.json",
                "view_path": "path/to/view_sarah.json"
            },
            {
                "name": "Michael",
                "matches": 12,
                "matches_keywords": [
                    {"keyword": "Python", "occurrences": 5},
                    {"keyword": "Django", "occurrences": 3},
                    {"keyword": "Flask", "occurrences": 2},
                    {"keyword": "FastAPI", "occurrences": 1},
                    {"keyword": "PostgreSQL", "occurrences": 2},
                    {"keyword": "Redis", "occurrences": 1},
                    {"keyword": "Docker", "occurrences": 2},
                    {"keyword": "Kubernetes", "occurrences": 1},
                    {"keyword": "AWS", "occurrences": 2},
                    {"keyword": "Linux", "occurrences": 1},
                    {"keyword": "Git", "occurrences": 1},
                    {"keyword": "CI/CD", "occurrences": 1}
                ],
                "summary_path": "path/to/summary_michael.json",
                "view_path": "path/to/view_michael.json"
            }
        ]
    
    # ... rest of the methods remain the same
    def get_candidates_for_page(self):
        """Get candidates for current page"""
        start = self.current_page * self.cards_per_page
        end = min(start + self.cards_per_page, len(self.candidates_data))
        return self.candidates_data[start:end]
    
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
        return self.candidates_data


