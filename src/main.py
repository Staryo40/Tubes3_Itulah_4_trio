from model import *  
from controller import *
from views import *
import sys
from PyQt5.QtWidgets import QApplication
# data = get_data()
# data_path = os.path.join(os.getcwd(), "data", "cv")
# res_gen = search_result(data_path, data, ["managed", "efficiency", "Presenter"], 1, 2, levenshtein_method.WORD, matching_algorithm.BM)
# result = res_gen.search_result()

# print(result["time"])
# print(result["cv_num"])
# for key, content in result["result"].items():
#     print("name:", content["name"])
#     print("dob:", content["dob"])
#     print("address:", content["address"])
#     print("phone:", content["phone"])
#     print("role:", content["role"])
#     print("path:", content["path"])
#     print("total_match:", content["total_match"])
#     print("exact_match:", content["exact_match"])
#     print("fuzzy_match:", content["fuzzy_match"])
#     print("search_res:", content["search_res"])
#     print("summary:", content["summary"])

#     print()


def main():
    data = get_data()
    # i = 0
    # for key, value in data.items():
    #     i += 1
    #     # print(F"Applicant number {i+1} with key {key}: {value}")
    #     # if i == 5:
    #     #     break
    # print(f"Number of applicants: {i}")
    data_path = os.path.join(os.getcwd(), "data", "data")

    app = QApplication(sys.argv)
    
    # Create MVC components
    model = MainModel()
    view = MainView()
    controller = MainController(view, model, data, data_path)
    
    # Show the application
    view.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()