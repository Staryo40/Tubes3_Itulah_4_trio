from model import get_data  
from search_result import *


# # print(result["result"][])
# print(result["time"])
# print(result["cv_num"])
# for key, content in result["result"].items():
#     print("name:", content["name"])
#     print("dob:", content["dob"])
#     print("address:", content["address"])
#     print("email:", content["email"])
#     print("phone:", content["phone"])
#     print("role:", content["role"])
#     print("path:", content["path"])
#     print("total_match:", content["total_match"])
#     print("exact_match:", content["exact_match"])
#     print("fuzzy_match:", content["fuzzy_match"])
#     print("search_res:", content["search_res"])
#     print("summary:", content["summary"])

#     print()

import sys
from PyQt5.QtWidgets import QApplication

from views.main_view import MainView
from models.candidate_model import CandidateModel
from controllers.main_controller import MainController

def main():
    data = get_data()
    data_path = os.path.join(os.getcwd(), "data", "cv")

    
    app = QApplication(sys.argv)
    
    # Create MVC components
    model = CandidateModel()
    view = MainView()
    controller = MainController(view, model, data, data_path)
    
    # Show the application
    view.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()