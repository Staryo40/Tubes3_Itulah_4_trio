from .search_algorithm import *
from .pdf_text import *
from .summary import *
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import time

class SearchResult:
    def __init__(self, root_data_dir, cv_dic, keywords, top_n, lev_threshold, lev_method: LevenshteinMethod, match_algo: MatchingAlgorithm):
        self.root = root_data_dir
        self.cv_dic = cv_dic
        self.keywords = keywords
        self.top_n = top_n
        self.lev_threshold = lev_threshold
        self.lev_method = lev_method
        self.match_algo = match_algo
    
    def process_cv(self, id, cv_data):
        full_path = os.path.join(self.root, cv_data["cv_path"])
        pdf = PDFExtractor(full_path)
        raw_text = pdf.extract_raw_from_pdf()
        matcher = MultipleKeywordSearch(raw_text, self.keywords)

        keyword_dic = matcher.keywords_search_result(self.lev_threshold, self.lev_method, self.match_algo)
        exact_match = matcher.exact_match_count(keyword_dic)
        fuzzy_match = matcher.similar_match_count(keyword_dic)
        total_match = exact_match + fuzzy_match

        raw_pdf_text = pdf.pdf_pure_text()
        sum_gen = CVSummaryGenerator(raw_pdf_text)
        sum_dic = sum_gen.get_final_summary()

        return id, {
            "name": cv_data["first_name"] + " " + cv_data["last_name"],
            "dob": cv_data["date_of_birth"],
            "address": cv_data["address"],
            "phone": cv_data["phone_number"],
            "role": cv_data["application_role"],
            "path": cv_data["cv_path"],
            "total_match": total_match,
            "exact_match": exact_match,
            "fuzzy_match": fuzzy_match,
            "search_res": keyword_dic,
            "summary": sum_dic
        }

    def search_result(self):
        result = {"time": 0, "cv_num": len(self.cv_dic), "result": {}}

        # cv_transformed_dic = {}
        # for key, content in self.cv_dic.items():
        #     cv_transformed_dic[content["detail_id"]] = content

        start = time.time()

        cv_result = {}
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.process_cv, id, cv_data) for id, cv_data in self.cv_dic.items()]
            for future in as_completed(futures):
                id, res = future.result()
                cv_result[str(id)] = res

        end = time.time()
        exec_time = end - start

        sorted_items = sorted(
            cv_result.items(),
            key=lambda item: -self.compute_priority_index(item[1])
        )
        top_items = sorted_items[:self.top_n]
        sorted_result = dict(top_items)
        result["time"] = exec_time
        result["result"] = sorted_result
        return result
    
    def compute_priority_index(self, cv_data):
        score = 0
        for entry in cv_data["search_res"].values():
            t = entry["type"].name
            occ = entry["occurrence"]
            if t == "Exact":
                score += 1000 + occ
            elif t == "Similar":
                score += 100 +  occ
            # NotFound or other types → score += 0
        return score


if __name__ == "__main__":     
    cv_dic = {
        "001": {
            "name": "Alice Johnson",
            "dob": "1990-04-12",
            "address": "123 Elm Street, Springfield, IL",
            "phone": "555-123-4567",
            "role": "Data Analyst",
            "path": "alice_johnson.pdf"
        },
        "002": {
            "name": "Bob Martinez",
            "dob": "1985-09-30",
            "address": "456 Oak Avenue, Rivertown, NY",
            "phone": "555-987-6543",
            "role": "Operations Manager",
            "path": "bob_martinez.pdf"
        }
    }
    
    data_path = os.path.join(os.getcwd(), "data", "cv")
    res_gen = SearchResult(data_path, cv_dic, ["managed", "efficiency", "Presenter"], 1, 2, LevenshteinMethod.WORD, MatchingAlgorithm.BM)
    result = res_gen.search_result()
    for key, content in result["result"].items():
        print("SEARCH RESULT")
        print(content["search_res"])
        print()
        print("SUMMARY")
        print(content["summary"])
        print()


            