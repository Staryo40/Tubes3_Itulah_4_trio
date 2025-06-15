import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QHBoxLayout, QMainWindow, QSpinBox, QGridLayout, QFrame, QScrollArea,
    QToolBar, QAction, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QSize
from PyQt5.QtGui import QPixmap, QFont, QCursor, QPainter, QPen
from .card_detail_dialog import CardDetailDialog
from local_enum import *

class MainView(QMainWindow):
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
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setup_left_panel()
        self.setup_right_panel()

        self.main_layout.addWidget(self.left_panel, 1)  # 25% width
        self.main_layout.addWidget(self.main_area, 3)   # 75% width

        self.setWindowTitle("CVSearch")
        self.setMinimumSize(800, 600)  
        self.resize(1200, 800)  
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    
    def setup_left_panel(self):
        self.left_panel = QWidget()
        self.left_panel.setMinimumWidth(250)  # Minimum width
        self.left_panel.setMaximumWidth(350)  # Maximum width
        self.left_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.left_panel.setStyleSheet("""
            QWidget {
                background-color: #e8e7e3;
                border-right: 1px solid #e0e0e0;
            }
        """)
        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.left_panel_layout.setContentsMargins(15, 15, 15, 15)  # Responsive margins
        self.left_panel_layout.setSpacing(10)

        self.setAppLogo(self.left_panel_layout)
        self.setSearchBar(self.left_panel_layout)
        self.setAlgorithmOptions(self.left_panel_layout)
        self.set_top_match_option(self.left_panel_layout)
        self.setSearchButton(self.left_panel_layout)
        
        self.left_panel_layout.addStretch()
    
    def setup_right_panel(self):
        self.main_area = QWidget()
        self.main_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_layout = QVBoxLayout(self.main_area)
        
        margin = max(10, min(30, self.width() // 40))
        self.result_layout.setContentsMargins(margin, margin, margin, margin)
        self.result_layout.setSpacing(15)

        self.welcome_label = QLabel("Welcome to CVMatcher!")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.welcome_label.setWordWrap(True)
        self.update_welcome_font()
        self.result_layout.addWidget(self.welcome_label)

    def update_welcome_font(self):
        if hasattr(self, 'welcome_label'):
            font_size = max(20, min(35, self.width() // 25))
            self.welcome_label.setStyleSheet(f"font-size: {font_size}px; font-weight: bold; color: #a7afb6;")

    def cleanup_right_panel(self):
        """Clear the right panel content"""
        while self.result_layout.count():
            item = self.result_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                # Handle nested layouts
                layout = item.layout()
                while layout.count():
                    child_item = layout.takeAt(0)
                    child_widget = child_item.widget()
                    if child_widget is not None:
                        child_widget.deleteLater()
        
        self.cards_container = None
        self.cards_layout = None
        self.result_title = None
        self.result_subtitle = None
        self.result_header_card = None
        self.pagination_layout = None
        self.welcome_label = None

    def update_header_card_responsive(self):
        """Update header card styling based on window size"""
        if hasattr(self, 'result_header_card'):
            max_width = min(600, int(self.width() * 0.8))
            self.result_header_card.setMaximumWidth(max_width)
            
            title_font_size = max(20, min(28, self.width() // 30))
            subtitle_font_size = max(12, min(14, self.width() // 60))
            
            if hasattr(self, 'result_title'):
                self.result_title.setStyleSheet(f"""
                    QLabel {{
                        font-size: {title_font_size}px;
                        font-weight: bold;
                        color: #2c2c2c;
                        background-color: transparent;
                        margin: 0px;
                        padding: 0px;
                    }}
                """)
            
            if hasattr(self, 'result_subtitle'):
                self.result_subtitle.setStyleSheet(f"""
                    QLabel {{
                        font-size: {subtitle_font_size}px;
                        color: #555555;
                        background-color: transparent;
                        font-weight: 500;
                        margin: 0px;
                        padding: 0px;
                    }}
                """)

    def setup_right_panel_content(self, result_count, execution_time):
        self.cleanup_right_panel()
        
        self.result_header_card = QFrame()
        self.result_header_card.setFrameShape(QFrame.StyledPanel)
        self.result_header_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.result_header_card.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border-radius: 15px;
                padding: 20px;
                margin: 0px 0px;
            }
        """)
        
        header_card_layout = QVBoxLayout(self.result_header_card)
        header_card_layout.setContentsMargins(20, 15, 20, 15)
        header_card_layout.setSpacing(0)
        header_card_layout.setAlignment(Qt.AlignCenter)
        
        self.result_title = QLabel("Search Results")
        self.result_title.setAlignment(Qt.AlignCenter)
        self.result_title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #000;
                background-color: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """)
        header_card_layout.addWidget(self.result_title)
        
        self.result_subtitle = QLabel(f"{result_count} CVs scanned in {execution_time:.2f}s")
        self.result_subtitle.setAlignment(Qt.AlignCenter)
        self.result_subtitle.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #808080;
                background-color: transparent;
                font-weight: 500;
                margin: 0px;
                padding: 0px;
            }
        """)
        header_card_layout.addWidget(self.result_subtitle)
        
        header_container = QHBoxLayout()
        header_container.addStretch()
        header_container.addWidget(self.result_header_card, 0)
        header_container.addStretch()
        
        self.result_layout.addLayout(header_container)
        
        spacer = QWidget()
        spacer.setFixedHeight(15)
        self.result_layout.addWidget(spacer)

        self.cards_container = QWidget()
        self.cards_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        
        spacing = self.get_card_spacing()
        self.cards_layout.setSpacing(spacing)
        
        self.result_layout.addWidget(self.cards_container, 1)  # Give it stretch factor

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
        
        logo_height = min(100, self.height() // 8)  # Max 100px or 1/8 of window height
        scaled_pixmap = self.pixmap.scaledToHeight(logo_height, Qt.SmoothTransformation)
        
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(self.image_label)
        layout.setAlignment(self.image_label, Qt.AlignCenter)

    def get_responsive_columns(self):
        return 3

    def get_max_cards_per_page(self):
        return 6

    def get_responsive_card_size(self):
        available_width = self.main_area.width() - 60  # Account for margins (30px each side)
        available_height = self.main_area.height() - 200  # Account for header, margins, and pagination
        
        card_width = int(available_width * 0.30)  # 30% of available width
        card_width = max(250, min(400, card_width))  # Min 250px, max 400px
        
        card_height = int(available_height * 0.40)  # 40% of available height
        card_height = max(180, min(300, card_height))  # Min 180px, max 300px
        
        return QSize(card_width, card_height)

    def get_card_spacing(self):
        available_width = self.main_area.width() - 60
        card_width = self.get_responsive_card_size().width()
        
        total_card_width = card_width * 3  # 3 columns
        remaining_space = available_width - total_card_width
        spacing = max(10, remaining_space // 4)  # Divide remaining space
        
        return min(30, spacing)  # Max 30px spacing

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


    def show_error_dialog(self, title, message):
        """Show error dialog with custom styling"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f0f0f0;
                color: #333333;
                font-size: 14px;
                border: 2px solid #cccccc;
            }
            QMessageBox QLabel {
                background-color: transparent;
                color: #333333;
                font-size: 14px;
                padding: 10px;
            }
            QMessageBox QPushButton {
                background-color: #808080;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #707070;
            }
            QMessageBox QPushButton:pressed {
                background-color: #606060;
            }
        """)
        
        msg_box.exec_()

    def show_validation_error(self, message):
        self.show_error_dialog("Input Error", message)

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
        keywords_text = self.search_bar.text().strip()
        
        if not keywords_text:
            self.show_validation_error("Please enter at least one keyword to search.")
            self.search_bar.setFocus()  # Focus back to search bar
            return
        
        keywords = [word.strip() for word in keywords_text.split(",") if word.strip()]
        
        if not keywords:
            self.show_validation_error("Please enter valid keywords separated by commas.\nExample: React, Python, JavaScript")
            self.search_bar.setFocus()
            return
        
        
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
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        max_cards = self.get_max_cards_per_page()
        display_data = candidates_data[:max_cards]
        
        cols = 3  
        card_size = self.get_responsive_card_size()
        spacing = self.get_card_spacing()
        
        self.cards_layout.setSpacing(spacing)
        
        for index, candidate in enumerate(display_data):
            row = index // cols  # 0 or 1 (max 2 rows)
            col = index % cols   # 0, 1, or 2 (3 columns)
            
            card = self.create_card(candidate, card_size)
            self.cards_layout.addWidget(card, row, col)
        
        for col in range(cols):
            self.cards_layout.setColumnStretch(col, 1)
        
        self.cards_layout.setRowStretch(0, 1)
        self.cards_layout.setRowStretch(1, 1)
        
        total_cards = len(display_data)
        if total_cards < max_cards:
            # Fill remaining cells with spacers to maintain layout
            for i in range(total_cards, max_cards):
                row = i // cols
                col = i % cols
                spacer = QWidget()
                spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.cards_layout.addWidget(spacer, row, col)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        if hasattr(self, 'result_layout'):
            margin = max(10, min(30, self.width() // 40))
            self.result_layout.setContentsMargins(margin, margin, margin, margin)
        
        if hasattr(self, 'left_panel_layout'):
            margin = max(10, min(20, self.width() // 60))
            self.left_panel_layout.setContentsMargins(margin, margin, margin, margin)
        
        self.update_header_card_responsive()
        
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.resize(self.main_area.size())
        
        if hasattr(self, 'cards_layout') and hasattr(self, 'model'):
            if not hasattr(self, 'resize_timer'):
                self.resize_timer = QTimer()
                self.resize_timer.setSingleShot(True)
                self.resize_timer.timeout.connect(self.update_cards_layout)
            self.resize_timer.start(100)

    def update_cards_layout(self):
        """Update cards layout after window resize"""
        if hasattr(self, 'model') and hasattr(self.model, 'get_card_result_for_current_page'):
            current_data = self.model.get_card_result_for_current_page()
            if current_data:
                if hasattr(self, 'cards_layout'):
                    spacing = self.get_card_spacing()
                    self.cards_layout.setSpacing(spacing)
                
                self.update_cards(current_data)

    def create_card(self, candidate_data, card_size=None):
        if card_size is None:
            card_size = self.get_responsive_card_size()
        
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        
        card.setMinimumSize(card_size)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        name_font_size = max(9, min(14, card_size.width() // 25))
        content_font_size = max(8, min(11, card_size.width() // 30))
        small_font_size = max(7, min(9, card_size.width() // 35))
        
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #e6e6e6;
                border-radius: 12px;
                padding: 15px;
                border: 2px solid transparent;
                margin: 5px;
            }}
            QFrame:hover {{
                background-color: #d6d6d6;
                cursor: pointer;
                border: 2px solid #c0c0c0;
            }}
            QFrame:hover QLabel {{
                background-color: transparent;
            }}
            QFrame:hover QLabel[class="keyword"] {{
                color: #333333;
            }}
            QFrame:hover QLabel[class="more"] {{
                color: #555555;
            }}
            QFrame:hover QLabel[class="click"] {{
                color: #555555;
            }}
        """)
        
        card.setCursor(QCursor(Qt.PointingHandCursor))
        card.mousePressEvent = lambda event: self.show_card_detail(candidate_data)
        
        card_layout = QVBoxLayout(card)
        margin = max(8, card_size.width() // 35)
        card_layout.setContentsMargins(margin, margin, margin, margin)
        card_layout.setSpacing(max(6, card_size.height() // 35))
        
        header_layout = QHBoxLayout()
        name_label = QLabel(candidate_data["name"])
        name_label.setStyleSheet(f"""
            QLabel {{
                font-size: {name_font_size}pt;
                font-weight: bold;
                color: #2c2c2c;
            }}
        """)
        name_label.setWordWrap(True)
        
        matches_text = f"{candidate_data['total_match']} match"
        if candidate_data['total_match'] != 1:
            matches_text += "es"
        matches_label = QLabel(matches_text)
        matches_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        matches_label.setStyleSheet(f"""
            QLabel {{
                font-size: {content_font_size}pt;
                color: #666666;
                font-weight: 600;
            }}
        """)
        
        header_layout.addWidget(name_label, 2)  # Give more space to name
        header_layout.addWidget(matches_label, 1)
        card_layout.addLayout(header_layout)
        
        keywords_label = QLabel("Matched keywords:")
        keywords_label.setStyleSheet(f"""
            QLabel {{
                font-size: {content_font_size}pt;
                font-weight: 600;
                color: #444444;
                margin-top: 5px;
            }}
        """)
        card_layout.addWidget(keywords_label)
        
        keywords_preview_layout = QVBoxLayout()
        keywords_preview_layout.setContentsMargins(margin//2, 0, 0, 0)
        keywords_preview_layout.setSpacing(3)
        
        max_preview = 3 if card_size.height() > 200 else 2
        max_preview = min(max_preview, len(candidate_data["search_res"]))
        
        for i in range(max_preview):
            keyword = list(candidate_data["search_res"].keys())[i]
            occurrences = candidate_data["search_res"][keyword]["occurrence"]
            keyword_text = f"• {keyword}: {occurrences} "
            keyword_text += "occurrence" if occurrences == 1 else "occurrences"
            
            keyword_label = QLabel(keyword_text)
            keyword_label.setProperty("class", "keyword")
            keyword_label.setStyleSheet(f"""
                QLabel {{
                    padding: 2px 0px;
                    font-size: {small_font_size}pt;
                    background-color: transparent;
                    color: #555555;
                }}
            """)
            keyword_label.setWordWrap(True)
            keywords_preview_layout.addWidget(keyword_label)

        if len(candidate_data["search_res"]) > max_preview:
            more_count = len(candidate_data['search_res']) - max_preview
            more_label = QLabel(f"• ... and {more_count} more keyword{'s' if more_count > 1 else ''}")
            more_label.setProperty("class", "more")
            more_label.setStyleSheet(f"""
                QLabel {{
                    padding: 2px 0px;
                    font-size: {small_font_size}pt;
                    font-style: italic;
                    color: #777777;
                    background-color: transparent;
                }}
            """)
            keywords_preview_layout.addWidget(more_label)
        
        card_layout.addLayout(keywords_preview_layout)
        card_layout.addStretch()
        
        
        return card


    def show_card_detail(self, candidate_data):
        dialog = CardDetailDialog(candidate_data, self)
        dialog.summary_requested.connect(self.summary_requested.emit)
        dialog.cv_requested.connect(self.cv_requested.emit)
        dialog.exec_()

    def update_pagination_buttons(self, can_previous, can_next):
        self.prev_button.setEnabled(can_previous)
        self.next_button.setEnabled(can_next)

    def show_loading_animation(self):
        self.search_button.setEnabled(False)
        self.search_button.setText("Searching...")
        
        self.loading_overlay = QWidget(self.main_area)
        self.loading_overlay.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border-radius: 10px;
            }
        """)
        
        overlay_layout = QVBoxLayout(self.loading_overlay)
        overlay_layout.setAlignment(Qt.AlignCenter)
        
        self.loading_widget = LoadingWidget()
        overlay_layout.addWidget(self.loading_widget, alignment=Qt.AlignCenter)
        
        loading_label = QLabel("Searching CVs...")
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #666666;
                margin-top: 10px;
            }
        """)
        overlay_layout.addWidget(loading_label)
        
        self.loading_overlay.resize(self.main_area.size())
        self.loading_overlay.show()
        
        self.loading_widget.start_animation()
        
        self.fade_in_animation = QPropertyAnimation(self.loading_overlay, b"windowOpacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_in_animation.start()

    def hide_loading_animation(self):
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            if hasattr(self, 'loading_widget'):
                self.loading_widget.stop_animation()
            
            self.fade_out_animation = QPropertyAnimation(self.loading_overlay, b"windowOpacity")
            self.fade_out_animation.setDuration(300)
            self.fade_out_animation.setStartValue(1.0)
            self.fade_out_animation.setEndValue(0.0)
            self.fade_out_animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.fade_out_animation.finished.connect(self.cleanup_loading_overlay)
            self.fade_out_animation.start()
        
        self.search_button.setEnabled(True)
        self.search_button.setText("Search")

    def cleanup_loading_overlay(self):
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.deleteLater()
            self.loading_overlay = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.resize(self.main_area.size())
        

class LoadingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        
    def start_animation(self):
        self.timer.start(50)  # Update every 50ms
        
    def stop_animation(self):
        self.timer.stop()
        
    def rotate(self):
        self.angle = (self.angle + 10) % 360
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw spinning circle
        pen = QPen()
        pen.setWidth(4)
        pen.setColor(Qt.gray)
        painter.setPen(pen)
        
        rect = self.rect().adjusted(10, 10, -10, -10)
        painter.drawArc(rect, self.angle * 16, 120 * 16)  # 120 degree arc