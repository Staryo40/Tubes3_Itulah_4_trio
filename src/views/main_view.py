import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QHBoxLayout, QMainWindow, QSpinBox, QGridLayout, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QCursor
from .card_detail_dialog import CardDetailDialog
from local_enum import *

class MainView(QMainWindow):
    # Signals untuk komunikasi dengan controller
    search_requested = pyqtSignal(list, MatchingAlgorithm, int)  # keywords, algorithm, top_matches
    algorithm_changed = pyqtSignal(int)  # algorithm state
    previous_page_requested = pyqtSignal()
    next_page_requested = pyqtSignal()
    summary_requested = pyqtSignal(str)  # path
    cv_requested = pyqtSignal(str)  # path
    
    def __init__(self):
        super().__init__()
        self.toggle_state = 0
        self.initUI()
    
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.setup_left_panel()
        self.setup_right_panel()

        self.main_layout.addWidget(self.left_panel, 1)
        self.main_layout.addWidget(self.main_area, 3)

        self.setWindowTitle("CVSearch")
        self.showFullScreen()
    
    def setup_left_panel(self):
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
        
        self.left_panel_layout.addStretch()
    
    def setup_right_panel(self):
        self.main_area = QWidget()
        self.result_layout = QVBoxLayout(self.main_area)
        self.result_layout.setContentsMargins(20, 20, 20, 20)
        self.result_layout.setSpacing(15)

    def cleanup_right_panel(self):
        """Clear the right panel content"""
        while self.result_layout.count():
            item = self.result_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        self.cards_container = None
        self.cards_layout = None
        self.result_title = None
        self.result_subtitle = None
        self.pagination_layout = None

    def setup_right_panel_content(self, result_count, execution_time):
        self.cleanup_right_panel()
        # Main title
        self.result_title = QLabel("Results")
        self.result_title.setAlignment(Qt.AlignCenter)
        self.result_title.setStyleSheet("font-size: 35px; font-weight: bold; color: black;")
        self.result_layout.addWidget(self.result_title)

        # Subtitle with result count and execution time
        self.result_subtitle = QLabel(f"{result_count} CVs scanned in {execution_time:.2f}s")
        self.result_subtitle.setAlignment(Qt.AlignCenter)
        self.result_subtitle.setStyleSheet("font-size: 14px; color: #666666; margin-top: 5px;")
        self.result_layout.addWidget(self.result_subtitle)

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(20)
        self.result_layout.addWidget(self.cards_container)

        self.setup_pagination()
        self.result_layout.addLayout(self.pagination_layout)
    
    def setup_pagination(self):
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page_requested.emit)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page_requested.emit)
        self.pagination_layout.addStretch()
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.next_button)
        self.pagination_layout.addStretch()

    def setAppLogo(self, layout):
        self.image_label = QLabel(self)
        self.pixmap = QPixmap("img/CVSearch_logo.png")
        scaled_pixmap = self.pixmap.scaledToHeight(100, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setScaledContents(True)
        layout.addWidget(self.image_label)
        layout.setAlignment(self.image_label, Qt.AlignCenter)

    def setSearchBar(self, layout):
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
        
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("React, Express, HTML")
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
                border-radius: 20px;
                padding: 10px;
            }
        """)
        
        container_layout = QVBoxLayout(toggle_container)
        container_layout.setContentsMargins(5, 5, 5, 5)
        container_layout.setSpacing(8)
        
        # Top row: KMP - Toggle - BM
        top_row = QFrame()
        top_row.setStyleSheet("QFrame { background-color: transparent; }")
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(10)
        
        self.kmp_label = QLabel("KMP")
        self.kmp_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #333333;
            }
        """)
        top_layout.addWidget(self.kmp_label)
        
        # Toggle switch
        self.algorithm_toggle = QFrame()
        self.algorithm_toggle.setFixedSize(120, 30)
        self.algorithm_toggle.setStyleSheet("""
            QFrame {
                background-color: #cccccc;
                border-radius: 15px;
                border: none;
            }
        """)
        
        self.toggle_button = QFrame(self.algorithm_toggle)
        self.toggle_button.setFixedSize(36, 26)
        self.toggle_button.move(2, 2)
        self.toggle_button.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 13px;
                border: none;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
        """)
        
        self.algorithm_toggle.mousePressEvent = self.toggle_algorithm
        top_layout.addWidget(self.algorithm_toggle)
        
        self.bm_label = QLabel("BM")
        self.bm_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #333333;
            }
        """)
        top_layout.addWidget(self.bm_label)
        
        container_layout.addWidget(top_row)
        
        # Bottom row: Aho-Corasick
        bottom_row = QFrame()
        bottom_row.setStyleSheet("QFrame { background-color: transparent; }")
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        bottom_layout.addStretch()
        self.ac_label = QLabel("Aho-Corasick")
        self.ac_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #333333;
            }
        """)
        bottom_layout.addWidget(self.ac_label)
        bottom_layout.addStretch()
        
        container_layout.addWidget(bottom_row)
        layout.addWidget(toggle_container)
        
        spacer = QWidget()
        spacer.setFixedHeight(20)
        layout.addWidget(spacer)



    def toggle_algorithm(self, event):
        self.toggle_state = (self.toggle_state + 1) % 3
        
        if self.toggle_state == 0:  # KMP
            self.toggle_button.move(2, 2)
        elif self.toggle_state == 1:  # Aho-Corasick
            self.toggle_button.move(42, 2)
        else:  # BM
            self.toggle_button.move(82, 2)
            
        self.algorithm_changed.emit(self.toggle_state)

    def set_top_match_option(self, layout):
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
        """)
        layout.addWidget(self.spin_box)

    def setSearchButton(self, layout):
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
        self.search_button.clicked.connect(self.on_search_clicked)
        layout.addWidget(self.search_button)
    
    def on_search_clicked(self):
        keywords = [word.strip() for word in self.search_bar.text().split(",") if word.strip()]
        algorithms = ["KMP", "Aho-Corasick", "BM"]
        algorithm = algorithms[self.toggle_state]
        top_matches = self.spin_box.value()
        algo_enum = MatchingAlgorithm.KMP
        if algorithm == "KMP":
            algo_enum = MatchingAlgorithm.KMP
        elif algorithm == "BM":
            algo_enum = MatchingAlgorithm.BM
        elif algorithm == "Aho-Corasick":
            algo_enum = MatchingAlgorithm.AC
        else:
            algo_enum = MatchingAlgorithm.KMP
        self.search_requested.emit(keywords, algo_enum, top_matches)

    def update_cards(self, candidates_data):
        # Clear existing cards
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Add new cards
        cols = 3
        for index, candidate in enumerate(candidates_data):
            row = index // cols
            col = index % cols
            card = self.create_card(candidate)
            self.cards_layout.addWidget(card, row, col)

    def create_card(self, candidate_data):
        # print(f"Creating card for candidate: {candidate_data}")
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #e6e6e6;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid transparent;
            }
            QFrame:hover {
                background-color: #d6d6d6;
                cursor: pointer;
            }
            QFrame:hover QLabel {
                color: #2c3e50;
            }
        """)
        
        card.setCursor(QCursor(Qt.PointingHandCursor))
        card.mousePressEvent = lambda event: self.show_card_detail(candidate_data)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(10)
        
        # Header (name and matches)
        header_layout = QHBoxLayout()
        name_label = QLabel(candidate_data["name"])
        name_font = QFont()
        name_font.setBold(True)
        name_font.setPointSize(12)
        name_label.setFont(name_font)
        
        matches_text = f"{candidate_data['total_match']} match"
        if candidate_data['total_match'] != 1:
            matches_text += "es"
        matches_label = QLabel(matches_text)
        matches_label.setAlignment(Qt.AlignRight)
        
        header_layout.addWidget(name_label)
        header_layout.addWidget(matches_label)
        card_layout.addLayout(header_layout)
        
        # Keywords section
        keywords_label = QLabel("Matched keywords:")
        card_layout.addWidget(keywords_label)
        
        keywords_preview_layout = QVBoxLayout()
        keywords_preview_layout.setContentsMargins(10, 0, 0, 0)
        keywords_preview_layout.setSpacing(2)
        
        max_preview = min(3, len(candidate_data["search_res"]))
        for i in range(max_preview):
            keyword = list(candidate_data["search_res"].keys())[i]
            occurrences = candidate_data["search_res"][keyword]["occurrence"]
            keyword_text = f"{i+1}. {keyword}: {occurrences} "
            keyword_text += "occurrence" if occurrences == 1 else "occurrences"
            
            keyword_label = QLabel(keyword_text)
            keyword_label.setStyleSheet("""
                QLabel {
                    padding: 1px 0px;
                    font-size: 10px;
                }
            """)
            keywords_preview_layout.addWidget(keyword_label)

        if len(candidate_data["search_res"]) > 3:
            more_label = QLabel(f"... and {len(candidate_data['search_res']) - 3} more")
            more_label.setStyleSheet("""
                QLabel {
                    padding: 1px 0px;
                    font-size: 10px;
                    font-style: italic;
                    color: #666666;
                }
            """)
            keywords_preview_layout.addWidget(more_label)
        
        card_layout.addLayout(keywords_preview_layout)
        card_layout.addStretch()
        
        click_label = QLabel("Click to view details")
        click_label.setAlignment(Qt.AlignCenter)
        click_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #666666;
                font-style: italic;
                padding: 5px;
            }
        """)
        card_layout.addWidget(click_label)
        
        card.setFixedSize(300, 200)
        return card
    
    def show_card_detail(self, candidate_data):
        """Show detailed card popup"""
        dialog = CardDetailDialog(candidate_data, self)
        dialog.summary_requested.connect(self.summary_requested.emit)
        dialog.cv_requested.connect(self.cv_requested.emit)
        dialog.exec_()

    def update_pagination_buttons(self, can_previous, can_next):
        self.prev_button.setEnabled(can_previous)
        self.next_button.setEnabled(can_next)
        