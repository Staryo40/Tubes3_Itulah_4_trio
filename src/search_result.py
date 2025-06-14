from search_algorithm import *
import time

# Asumsi cv_dic
# id : {"name": val, "dob": val, "text": val, "path": val}

# Struktur Result
# {
#   "time": val,
#   "cv_num": val, -> total number of cv scanned
#   "result": {
#              "cv_id": {
#                        "name": val,
#                        "total_match": val,
#                        "exact_match": val,
#                        "fuzzy_match": val,
#                        "path": val,
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

class search_result:
    def __init__(self, cv_dic, keywords, top_n, lev_threshold, lev_method: levenshtein_method, match_algo: matching_algorithm):
        self.cv_dic = cv_dic
        self.keywords = keywords
        self.top_n = top_n
        self.lev_threshold = lev_threshold
        self.lev_method = lev_method
        self.match_algo = match_algo
    
    def search_result(self):
        result = {"time": 0, "cv_num": len(self.cv_dic), "result": {}}

        # Getting keyword matches
        start = time.time()
        for id in self.cv_dic:
            print(id)

    def flatten_text(self, text):
        pass