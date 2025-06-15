from model import *  
from controller import *
from views import *
import sys
from PyQt5.QtWidgets import QApplication


def main():
    data = get_data()
    data_path = os.path.join(os.getcwd(), "data", "data")

    app = QApplication(sys.argv)
    
    model = MainModel()
    view = MainView()
    controller = MainController(view, model, data, data_path)
    
    view.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()