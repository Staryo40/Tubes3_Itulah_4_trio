import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox, QRadioButton, QButtonGroup, QHBoxLayout, QMainWindow, QSpinBox
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
        self.image_label.setScaledContents(True)  # Supaya gambar bisa diskalakan

        self.image_label.setMaximumSize(240, 80)
        self.image_label.setMinimumSize(240, 80)
        layout.addWidget(self.image_label)
        layout.setAlignment(self.image_label, Qt.AlignCenter)

    def setSearchBar(self, layout):
        self.search_layout = QVBoxLayout()
        self.search_layout.setSpacing(10)

        self.search_label = QLabel("Keywords:", self)
        self.search_label.setAlignment(Qt.AlignLeft)
        self.search_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #000000;
                padding: 0px;
                margin: 0px;            
            }
        """)
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("e.g. React, Python, Java")
        self.search_bar.textChanged.connect(self.on_search)
        self.search_bar.setMaximumWidth(220)
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
        self.option_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #000000;
                padding: 0px;
                margin: 0px;
            }
        """)
        # Pilihan algoritma KMP
        self.kmp_option = QRadioButton("KMP (Knuth-Morris-Pratt)")
        self.kmp_option.setChecked(True)  # Pilihan default
        self.kmp_option.setStyleSheet("""
            QRadioButton {
                font-size: 14px;
                color: #000;
            }
        """)

        # Pilihan algoritma BM
        self.bm_option = QRadioButton("BM (Boyer-Moore)")
        self.bm_option.setStyleSheet("""
            QRadioButton {
                font-size: 14px;
                color: #000;
            }
        """)

        # Grup tombol untuk memastikan hanya satu pilihan aktif
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.kmp_option)
        self.button_group.addButton(self.bm_option)

        # Tombol konfirmasi
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

        # Layout horizontal untuk pilihan algoritma
        self.selection_layout = QVBoxLayout()
        self.selection_layout.addWidget(self.kmp_option)
        self.selection_layout.addWidget(self.bm_option)
        self.selection_layout.setSpacing(20)
        layout.addWidget(self.option_label)
        layout.addLayout(self.selection_layout)

    def setTopMatchOption(self, layout):
        label = QLabel("Top Matches:")
        label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #000000;
                padding: 0px;
                margin: 0px;
            }
        """)
        layout.addWidget(label)

        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(0)   # nilai minimal
        self.spin_box.setMaximum(100) # nilai maksimal
        self.spin_box.setValue(1)    # nilai default
        self.spin_box.setStyleSheet("""
            QSpinBox {
                background-color: #d3d3d3;       /* abu-abu muda */
                border: 1px solid #888888;       /* border abu-abu agak gelap */
                border-radius: 8px;              /* sudut membulat */
                padding: 2px 5px;                /* padding dalam spinbox */
                font-size: 14px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #888888;
                background-color: #b0b0b0;       /* tombol panah abu */
                border-radius: 0 8px 0 0;
            }
            QSpinBox::down-button {
                subcontrol-position: bottom right;
                border-radius: 0 0 8px 0;
            }
        """)


        layout.addWidget(self.spin_box)

    def setSearchButton(self, layout):
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.do_search)
        layout.addWidget(self.search_button)

    def do_search(self):
        # Saat tombol diklik, update teks di main_area
        self.main_area.setText("Search button clicked! Menampilkan hasil...")

    def on_search(self, text):
        self.main_area.setText(f"Searching for: {text}")

    def confirm_selection(self):
        # Menentukan pilihan algoritma
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
        self.setTopMatchOption(self.left_panel_layout)
        self.setSearchButton(self.left_panel_layout)

        self.main_area = QLabel("CVSearch")
        self.main_area.setAlignment(Qt.AlignCenter)
        self.main_area.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #555;
            }
        """)

        # Set layout utama
        self.main_layout.addWidget(self.left_panel, 1)
        self.main_layout.addWidget(self.main_area, 3)
        self.setWindowTitle("CVSearch")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())


