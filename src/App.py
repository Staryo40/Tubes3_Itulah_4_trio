import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QRadioButton, QButtonGroup, QHBoxLayout, QMainWindow, QSpinBox,
    QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


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
        self.search_layout = QVBoxLayout()
        self.search_layout.setSpacing(0)

        self.search_label = QLabel("Keywords:", self)
        self.search_label.setFixedHeight(40)
        self.search_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #000000;
                padding: 0px 0px;
                margin: 0px 0px;
            }
        """)
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("e.g. React, Python, Java")
        self.search_bar.textChanged.connect(self.on_search)
        self.search_bar.setMaximumWidth(300)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #C5CFD1;
                border-radius: 12px;
                padding: 8px 15px;
                background-color: #C5CFD1;
                font-size: 16px;
            }
        """)
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_bar)
        layout.addLayout(self.search_layout)

    def setAlgorithmOptions(self, layout):
        self.option_label = QLabel("Select Algorithm:", self)
        self.option_label.setFixedHeight(40)
        self.option_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #000000;
                padding: 0px 0px;
                margin: 0px 0px;
            }
        """)
        self.kmp_option = QRadioButton("KMP (Knuth-Morris-Pratt)")
        self.kmp_option.setChecked(True)
        self.kmp_option.setStyleSheet("""
            QRadioButton {
                font-size: 14px;
                color: #000;
            }
        """)
        self.bm_option = QRadioButton("BM (Boyer-Moore)")
        self.bm_option.setStyleSheet("""
            QRadioButton {
                font-size: 14px;
                color: #000;
            }
        """)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.kmp_option)
        self.button_group.addButton(self.bm_option)
        self.confirm_button = QPushButton("Confirm Selection")
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                font-size: 14px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.selection_layout = QVBoxLayout()
        self.selection_layout.addWidget(self.kmp_option)
        self.selection_layout.addWidget(self.bm_option)
        self.selection_layout.setSpacing(20)
        layout.addWidget(self.option_label)
        layout.addLayout(self.selection_layout)

    def set_top_match_option(self, layout):
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 50)
        container_layout.setSpacing(0)

        self.count_label = QLabel("Top Matches:")
        self.count_label.setFixedHeight(40)
        self.count_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #000000;
                padding: 0px 0px;
                margin: 0px 0px;
            }
        """)
        container_layout.addWidget(self.count_label)

        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(0)
        self.spin_box.setMaximum(100)
        self.spin_box.setValue(1)
        self.spin_box.setStyleSheet("""
            QSpinBox {
                background-color: #C5CFD1;
                border: 1px solid #888888;
                border-radius: 8px;
                padding: 2px 5px;
                font-size: 14px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #888888;
                background-color: #b0b0b0;
                border-radius: 0 8px 0 0;
            }
            QSpinBox::down-button {
                subcontrol-position: bottom right;
                border-radius: 0 0 8px 0;
            }
        """)
        container_layout.addWidget(self.spin_box)

        layout.addWidget(container)

    def setSearchButton(self, layout):
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #A0A9AD;
                color: black;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8B9194;
            }
            QPushButton:pressed {
                background-color: #6C7376;
            }
        """)
        self.search_button.clicked.connect(self.do_search)
        layout.addWidget(self.search_button)

    def do_search(self):
        self.main_area.setText("Search button clicked! Menampilkan hasil...")

    def on_search(self, text):
        self.main_area.setText(f"Searching for: {text}")

    def confirm_selection(self):
        if self.kmp_option.isChecked():
            print("KMP (Knuth-Morris-Pratt) selected.")
        elif self.bm_option.isChecked():
            print("BM (Boyer-Moore) selected.")

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.left_panel = QWidget()
        self.left_panel.setStyleSheet("""
            QWidget {
                background-color: #e8e7e3;
                border-right: 1px solid #d3d3d3;
            }
        """)
        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.left_panel_layout.setContentsMargins(10, 10, 10, 10)
        self.left_panel_layout.setSpacing(10)

        self.setAppLogo(self.left_panel_layout)
        self.setSearchBar(self.left_panel_layout)
        self.setAlgorithmOptions(self.left_panel_layout)
        self.set_top_match_option(self.left_panel_layout)
        self.setSearchButton(self.left_panel_layout)

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

        # Contoh data card (50 card)
        self.cards_data = [f"Card content #{i + 1}" for i in range(50)]

        self.current_page = 0
        self.cards_per_page = 6  # 3 cols x 6 rows

        self.update_cards()

    # def create_card(self, text):
    #     card = QWidget()
    #     card.setStyleSheet("""
    #         QWidget {
    #             background-color: #f0f0f0;
    #             border: 1px solid #ccc;
    #             border-radius: 8px;
    #         }
    #     """)
    #     card_layout = QVBoxLayout(card)
    #     card_layout.setContentsMargins(10, 10, 10, 10)
    #     card_layout.setAlignment(Qt.AlignCenter)

    #     label = QLabel(text)
    #     label.setWordWrap(True)
    #     label.setAlignment(Qt.AlignCenter)
    #     label.setStyleSheet("font-size: 14px; color: #333;")
    #     card_layout.addWidget(label)

    #     card.setFixedSize(250, 200)
    #     return card

    def create_card(self, header_text, description_text):
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(10)

        # Header
        header = QLabel(header_text)
        header.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #222;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(header)

        # Description
        description = QLabel(description_text)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #555;
            }
        """)
        card_layout.addWidget(description)

        # Button Container
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Summary Button
        summary_button = QPushButton("Summary")
        summary_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f7f;
            }
        """)
        button_layout.addWidget(summary_button)

        # View CV Button
        view_button = QPushButton("View CV")
        view_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        button_layout.addWidget(view_button)

        card_layout.addWidget(button_container)

        # Fix Card Size
        card.setFixedSize(250, 250)

        return card


    def update_cards(self):
        # Clear existing widgets in the cards layout
        while self.cards_layout.count():
            widget = self.cards_layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

        # Calculate start and end indices for the current page
        start = self.current_page * self.cards_per_page
        end = min(start + self.cards_per_page, len(self.cards_data))  # Prevent overflow

        # Add cards for the current page
        cols = 3
        for index, text in enumerate(self.cards_data[start:end]):
            row = index // cols
            col = index % cols
            card = self.create_card(text, "ini nigga saya")  # Ensure create_card is implemented correctly
            self.cards_layout.addWidget(card, row, col)

        # Update pagination buttons
        self.prev_button.setEnabled(self.current_page > 0)
        max_page = (len(self.cards_data) + self.cards_per_page - 1) // self.cards_per_page - 1
        self.next_button.setEnabled(self.current_page < max_page)




    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_cards()

    def show_next_page(self):
        max_page = (len(self.cards_data) - 1) // self.cards_per_page
        if self.current_page < max_page:
            self.current_page += 1
            self.update_cards()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
