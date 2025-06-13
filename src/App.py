import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QRadioButton, QButtonGroup, QHBoxLayout, QMainWindow, QSpinBox,
    QGridLayout, QScrollArea, QFrame, QSlider
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def setAppLogo(self, layout):
        self.image_label = QLabel(self)
        self.pixmap = QPixmap("../img/CVSearch_logo.png")
        scaled_pixmap = self.pixmap.scaledToHeight(100, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setScaledContents(True)
        layout.addWidget(self.image_label)
        layout.setAlignment(self.image_label, Qt.AlignCenter)

    def setSearchBar(self, layout):
        # Keywords label
        self.search_label = QLabel("Keywords:", self)
        self.search_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(self.search_label)
        
        # Modern search input
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("React, Express, HTML")
        self.search_bar.textChanged.connect(self.on_search)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                border: none;
                border-radius: 15px;
                padding: 12px 15px;
                background-color: #f0f0f0;
                font-size: 14px;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(self.search_bar)

    def setAlgorithmOptions(self, layout):
        # Algorithm label
        self.option_label = QLabel("Search Algorithm:", self)
        self.option_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(self.option_label)
        
        # Create toggle container
        toggle_container = QFrame()
        toggle_container.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border-radius: 15px;
                padding: 5px;
            }
        """)
        toggle_layout = QHBoxLayout(toggle_container)
        toggle_layout.setContentsMargins(10, 5, 10, 5)
        toggle_layout.setSpacing(5)
        
        # KMP label
        self.kmp_label = QLabel("KMP")
        self.kmp_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
            }
        """)
        toggle_layout.addWidget(self.kmp_label)
        
        # Custom toggle switch
        self.algorithm_toggle = QFrame()
        self.algorithm_toggle.setFixedSize(60, 30)
        self.algorithm_toggle.setStyleSheet("""
            QFrame {
                background-color: #cccccc;
                border-radius: 15px;
                border: none;
            }
        """)
        
        # Toggle button (slider)
        self.toggle_button = QFrame(self.algorithm_toggle)
        self.toggle_button.setFixedSize(26, 26)
        self.toggle_button.move(2, 2)  # Position for KMP (left)
        self.toggle_button.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 13px;
                border: none;
            }
        """)
        
        # Variable to track toggle state (True = KMP, False = BM)
        self.toggle_state = True
        
        # Make toggle clickable
        self.algorithm_toggle.mousePressEvent = self.toggle_algorithm
        toggle_layout.addWidget(self.algorithm_toggle)
        
        # BM label
        self.bm_label = QLabel("BM")
        self.bm_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
            }
        """)
        toggle_layout.addWidget(self.bm_label)
        
        # Add toggle container to layout
        layout.addWidget(toggle_container)
        
        # Add spacing
        spacer = QWidget()
        spacer.setFixedHeight(20)
        layout.addWidget(spacer)

    def toggle_algorithm(self, event):
        # Toggle the state
        self.toggle_state = not self.toggle_state
        
        # Update toggle button position
        if self.toggle_state:  # KMP
            self.toggle_button.move(2, 2)
            self.algorithm_toggle.setStyleSheet("""
                QFrame {
                    background-color: #cccccc;
                    border-radius: 15px;
                    border: none;
                }
            """)
            print("KMP algorithm selected")
        else:  # BM
            self.toggle_button.move(32, 2)
            self.algorithm_toggle.setStyleSheet("""
                QFrame {
                    background-color: #a0a0a0;
                    border-radius: 15px;
                    border: none;
                }
            """)
            print("BM algorithm selected")

    def set_top_match_option(self, layout):
        # Top Matches label
        self.count_label = QLabel("Top Matches:")
        self.count_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(self.count_label)

        # Modern number input
        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(100)
        self.spin_box.setValue(3)
        self.spin_box.setStyleSheet("""
            QSpinBox {
                background-color: #f0f0f0;
                border: none;
                border-radius: 15px;
                padding: 10px 15px;
                font-size: 14px;
                margin-bottom: 20px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border: none;
                background-color: transparent;
            }
            QSpinBox::up-arrow {
                image: url(../img/up_arrow.png);
                width: 10px;
                height: 10px;
            }
            QSpinBox::down-arrow {
                image: url(../img/down_arrow.png);
                width: 10px;
                height: 10px;
            }
        """)
        layout.addWidget(self.spin_box)

    def setSearchButton(self, layout):
        # Modern search button
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #707070;
            }
            QPushButton:pressed {
                background-color: #606060;
            }
        """)
        self.search_button.clicked.connect(self.do_search)
        layout.addWidget(self.search_button)

    def do_search(self):
        # Load sample data for demonstration
        self.load_candidate_data()
        self.update_cards()

    def on_search(self, text):
        pass

    def load_candidate_data(self):
        # Sample data that matches the structure provided
        self.candidates_data = [
            {
                "name": "Farhan",
                "matches": 4,
                "matches_keywords": [
                    {"keyword": "React", "occurrences": 1},
                    {"keyword": "Express", "occurrences": 2},
                    {"keyword": "HTML", "occurrences": 1}
                ],
                "summary_path": "path/to/summary_farhan.json",
                "view_path": "path/to/view_farhan.json"
            },
            {
                "name": "Aland",
                "matches": 1,
                "matches_keywords": [
                    {"keyword": "React", "occurrences": 1}
                ],
                "summary_path": "path/to/summary_aland.json",
                "view_path": "path/to/view_aland.json"
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
            # Add more sample data to test pagination
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
            }
        ]

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.left_panel = QWidget()
        self.left_panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border-right: 1px solid #e0e0e0;
            }
        """)
        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.left_panel_layout.setContentsMargins(20, 20, 20, 20)
        self.left_panel_layout.setSpacing(15)

        self.setAppLogo(self.left_panel_layout)
        self.setSearchBar(self.left_panel_layout)
        self.setAlgorithmOptions(self.left_panel_layout)
        self.set_top_match_option(self.left_panel_layout)
        self.setSearchButton(self.left_panel_layout)
        
        # Add stretch to push everything to the top
        self.left_panel_layout.addStretch()

        # Result widget with cards and pagination
        self.main_area = QWidget()
        self.result_layout = QVBoxLayout(self.main_area)
        self.result_layout.setContentsMargins(20, 20, 20, 20)
        self.result_layout.setSpacing(15)

        self.result_title = QLabel("Result")
        self.result_title.setAlignment(Qt.AlignCenter)
        self.result_title.setStyleSheet("font-size: 35px; font-weight: bold;")
        self.result_layout.addWidget(self.result_title)

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(20)
        self.result_layout.addWidget(self.cards_container)

        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.show_previous_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next_page)
        self.pagination_layout.addStretch()
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.next_button)
        self.pagination_layout.addStretch()

        self.result_layout.addLayout(self.pagination_layout)

        self.main_layout.addWidget(self.left_panel, 1)
        self.main_layout.addWidget(self.main_area, 3)

        self.setWindowTitle("CVSearch")
        self.setGeometry(100, 100, 800, 600)

        # Initialize with sample data
        self.load_candidate_data()
        
        self.current_page = 0
        self.cards_per_page = 6  # 3 cols x 2 rows

        self.update_cards()

    def create_card(self, candidate_data):
        # Create a card frame with light gray background and rounded corners
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #e6e6e6;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        # Main layout for the card
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(10)
        
        # Header layout (name and matches)
        header_layout = QHBoxLayout()
        
        # Name label
        name_label = QLabel(candidate_data["name"])
        name_font = QFont()
        name_font.setBold(True)
        name_font.setPointSize(12)
        name_label.setFont(name_font)
        
        # Matches label
        matches_text = f"{candidate_data['matches']} match"
        if candidate_data['matches'] != 1:
            matches_text += "es"
        matches_label = QLabel(matches_text)
        matches_label.setAlignment(Qt.AlignRight)
        
        header_layout.addWidget(name_label)
        header_layout.addWidget(matches_label)
        card_layout.addLayout(header_layout)
        
        # Matched keywords section
        keywords_label = QLabel("Matched keywords:")
        card_layout.addWidget(keywords_label)
        
        # List of keywords
        keywords_layout = QVBoxLayout()
        keywords_layout.setContentsMargins(10, 0, 0, 0)
        
        for i, keyword_data in enumerate(candidate_data["matches_keywords"]):
            keyword = keyword_data["keyword"]
            occurrences = keyword_data["occurrences"]
            
            keyword_text = f"{i+1}. {keyword}: {occurrences} "
            keyword_text += "occurrence" if occurrences == 1 else "occurrences"
            
            keyword_label = QLabel(keyword_text)
            keywords_layout.addWidget(keyword_label)
        
        card_layout.addLayout(keywords_layout)
        
        # Add stretch to push buttons to the bottom
        card_layout.addStretch()
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        summary_btn = QPushButton("Summary")
        summary_btn.setStyleSheet("""
            QPushButton {
                background-color: #a0a0a0;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                border: none;
            }
            QPushButton:hover {
                background-color: #808080;
            }
        """)
        summary_btn.clicked.connect(lambda: self.open_summary(candidate_data["summary_path"]))
        
        view_cv_btn = QPushButton("View CV")
        view_cv_btn.setStyleSheet("""
            QPushButton {
                background-color: #a0a0a0;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                border: none;
            }
            QPushButton:hover {
                background-color: #808080;
            }
        """)
        view_cv_btn.clicked.connect(lambda: self.open_cv(candidate_data["view_path"]))
        
        buttons_layout.addWidget(summary_btn)
        buttons_layout.addWidget(view_cv_btn)
        
        card_layout.addLayout(buttons_layout)
        
        # Set fixed size for the card
        card.setFixedSize(300, 200)
        
        return card
    
    def open_summary(self, path):
        print(f"Opening summary from: {path}")
        
    def open_cv(self, path):
        print(f"Opening CV from: {path}")

    def update_cards(self):
        # Clear existing widgets in the cards layout
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Calculate start and end indices for the current page
        start = self.current_page * self.cards_per_page
        end = min(start + self.cards_per_page, len(self.candidates_data))  # Prevent overflow

        # Add cards for the current page
        cols = 3
        for index, candidate in enumerate(self.candidates_data[start:end]):
            row = index // cols
            col = index % cols
            card = self.create_card(candidate)
            self.cards_layout.addWidget(card, row, col)

        # Update pagination buttons
        self.prev_button.setEnabled(self.current_page > 0)
        max_page = (len(self.candidates_data) + self.cards_per_page - 1) // self.cards_per_page - 1
        self.next_button.setEnabled(self.current_page < max_page)

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_cards()

    def show_next_page(self):
        max_page = (len(self.candidates_data) - 1) // self.cards_per_page
        if self.current_page < max_page:
            self.current_page += 1
            self.update_cards()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())