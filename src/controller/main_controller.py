import os, subprocess, platform, webbrowser, threading
from model import *
from controller import *
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

global_levenshtein_threshold = 2

class SearchThread(QThread):
    search_completed = pyqtSignal(dict)
    
    def __init__(self, data_path, data, keywords, top_matches, threshold, method, algorithm):
        super().__init__()
        self.data_path = data_path
        self.data = data
        self.keywords = keywords
        self.top_matches = top_matches
        self.threshold = threshold
        self.method = method
        self.algorithm = algorithm
    
    def run(self):
        res_gen = SearchResult(self.data_path, self.data, self.keywords, 
                              self.top_matches, self.threshold, self.method, self.algorithm)
        results = res_gen.search_result()
        self.search_completed.emit(results)

class MainController:
    def __init__(self, view, model, data, data_path):
        self.view = view
        self.model = model
        self.data = data
        self.data_path = data_path
        self.connect_signals()
        self.results = {}
        self.data = data
        self.data_path = data_path
        # self.initialize()
    
    def connect_signals(self):
        """Connect view signals to controller methods"""
        self.view.search_requested.connect(self.handle_search)
        self.view.algorithm_changed.connect(self.handle_algorithm_change)
        self.view.previous_page_requested.connect(self.handle_previous_page)
        self.view.next_page_requested.connect(self.handle_next_page)
        self.view.summary_requested.connect(self.handle_summary_request)
        self.view.cv_requested.connect(self.handle_cv_request)
    
    def initialize(self):
        self.model.load_sample_data()
        self.update_view()
    
    def handle_search(self, keywords, algorithm: MatchingAlgorithm, top_matches):
        print(f"Controller: Searching for '{keywords}' using {algorithm}, top {top_matches} matches")
        self.model.current_page = 0
        self.view.cleanup_right_panel()
        
        # Show loading animation
        self.view.show_loading_animation()
        
        # Create and start search thread
        self.search_thread = SearchThread(
            self.data_path, self.data, keywords, top_matches, 
            global_levenshtein_threshold, LevenshteinMethod.WORD, algorithm
        )
        self.search_thread.search_completed.connect(self.on_search_completed)
        self.search_thread.start()

    def on_search_completed(self, results):
        self.results = results
        self.model.set_card_result(self.results['result'])
        self.view.hide_loading_animation()
        self.view.setup_right_panel_content(self.results['cv_num'], self.results['time'])
        self.update_view()
    
    def handle_algorithm_change(self, algorithm_state):
        algorithms = ["KMP", "Aho-Corasick", "BM"]
        selected_algorithm = algorithms[algorithm_state]
        print(f"Controller: Algorithm changed to {selected_algorithm}")
    
    def handle_previous_page(self):
        if self.model.go_previous_page():
            self.update_view()
            print(f"Controller: Moved to page {self.model.current_page + 1}")
    
    def handle_next_page(self):
        if self.model.go_next_page():
            self.update_view()
            print(f"Controller: Moved to page {self.model.current_page + 1}")
    
    def handle_summary_request(self, path):
        print(f"Controller: Opening summary from {path}")
        # Implement summary opening logic here
        self.open_file(path)
    
    def handle_cv_request(self, path):
        full_path = os.path.join(self.data_path, path)
        print(f"Controller: Opening CV PDF from {full_path}")
        self.open_pdf_file(full_path)
    
    def open_pdf_file(self, file_path):
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"Error: File not found - {file_path}")
                # For demo purposes, create a sample message
                self.show_file_not_found_message(file_path)
                return
            
            # Cross-platform file opening
            system = platform.system()
            
            if system == "Windows":
                os.startfile(file_path)
            elif system == "Darwin":  # macOS
                subprocess.call(["open", file_path])
            elif system == "Linux":
                subprocess.call(["xdg-open", file_path])
            else:
                # Fallback: use webbrowser module
                webbrowser.open(f"file://{os.path.abspath(file_path)}")
            
            print(f"Successfully opened PDF: {file_path}")
            
        except Exception as e:
            print(f"Error opening PDF file: {e}")
            self.show_error_message(f"Could not open PDF file: {str(e)}")
    
    def open_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                print(f"Error: File not found - {file_path}")
                self.show_file_not_found_message(file_path)
                return
            
            system = platform.system()
            
            if system == "Windows":
                os.startfile(file_path)
            elif system == "Darwin":  # macOS
                subprocess.call(["open", file_path])
            elif system == "Linux":
                subprocess.call(["xdg-open", file_path])
            else:
                webbrowser.open(f"file://{os.path.abspath(file_path)}")
            
            print(f"Successfully opened file: {file_path}")
            
        except Exception as e:
            print(f"Error opening file: {e}")
            self.show_error_message(f"Could not open file: {str(e)}")
    
    def show_file_not_found_message(self, file_path):
        print(f"File not found: {file_path}")
        
        # You can implement a proper message dialog here if needed
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("File Not Found")
        msg.setText(f"Could not find file:\n{file_path}")
        msg.exec_()
    
    def show_error_message(self, message):
        print(f"Error: {message}")
        
        # You can implement a proper error dialog here if needed
        # from PyQt5.QtWidgets import QMessageBox
        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Critical)
        # msg.setWindowTitle("Error")
        # msg.setText(message)
        # msg.exec_()
    
    def update_view(self):
        self.view.update_cards(self.model.get_card_result_for_current_page())

        can_previous = self.model.can_go_previous()
        can_next = self.model.can_go_next()
        self.view.update_pagination_buttons(can_previous, can_next)