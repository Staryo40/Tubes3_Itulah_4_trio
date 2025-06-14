from model import get_data  
from search_result import *

data = get_data()
data_path = os.path.join(os.getcwd(), "data", "cv")
res_gen = search_result(data_path, data, ["managed", "efficiency", "Presenter"], 1, 2, levenshtein_method.WORD, matching_algorithm.BM)
result = res_gen.search_result()
# print(result["result"][])
print(result["time"])
print(result["cv_num"])
for key, content in result["result"].items():
    print("name:", content["name"])
    print("dob:", content["dob"])
    print("address:", content["address"])
    print("email:", content["email"])
    print("phone:", content["phone"])
    print("role:", content["role"])
    print("path:", content["path"])
    print("total_match:", content["total_match"])
    print("exact_match:", content["exact_match"])
    print("fuzzy_match:", content["fuzzy_match"])
    print("search_res:", content["search_res"])
    print("summary:", content["summary"])

    print()
