import sys
from PyQt5.QtWidgets import QApplication

from views.main_view import MainView
from models.candidate_model import CandidateModel
from controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    
    # Create MVC components
    model = CandidateModel()
    view = MainView()
    controller = MainController(view, model)
    
    # Show the application
    view.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()