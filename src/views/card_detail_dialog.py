from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QWidget, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QColor, QPixmap, QIcon

from views.cv_summary_dialog import CVSummaryDialog

class CardDetailDialog(QDialog):
    summary_requested = pyqtSignal(str)
    cv_requested = pyqtSignal(str)
    
    def __init__(self, candidate_data, parent=None):
        super().__init__(parent)
        self.candidate_data = candidate_data
        self.setWindowTitle("")  # Remove title
        self.setModal(True)
        self.setFixedSize(600, 500)
        
        # Remove window frame for modern look
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setup_ui()
        self.add_shadow_effect()
        self.animate_entrance()
    
    def setup_ui(self):
        # Main layout with margins for shadow
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create the modern card container
        self.card_container = QFrame()
        self.card_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: none;
            }
        """)
        
        # Card layout
        card_layout = QVBoxLayout(self.card_container)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        
        # Header section with gray gradient background
        self.create_header_section(card_layout)
        
        # Content section
        self.create_content_section(card_layout)
        
        # Footer section with buttons
        self.create_footer_section(card_layout)
        
        main_layout.addWidget(self.card_container)
    
    def create_header_section(self, layout):
        """Create modern header with gray gradient background"""
        header_frame = QFrame()
        header_frame.setFixedHeight(120)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #8e9aaf, stop:1 #6c757d);
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 25, 30, 25)
        header_layout.setSpacing(8)
        
        # Candidate name with modern typography
        name_label = QLabel(self.candidate_data["name"])
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
        """)
        header_layout.addWidget(name_label)
        
        # Matches info with pill design
        matches_container = QHBoxLayout()
        matches_container.setContentsMargins(0, 0, 0, 0)
        
        matches_count = self.candidate_data['total_match']
        matches_pill = QLabel(f"{matches_count} {'match' if matches_count == 1 else 'matches'}")
        matches_pill.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                padding: 8px 16px;
                border-radius: 15px;
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)
        matches_pill.setFixedHeight(30)
        
        matches_container.addWidget(matches_pill)
        matches_container.addStretch()
        header_layout.addLayout(matches_container)
        
        layout.addWidget(header_frame)
    
    def create_content_section(self, layout):
        """Create content section with gray styling"""
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
            }
        """)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(30, 25, 30, 20)
        content_layout.setSpacing(20)
        
        # Keywords section title
        keywords_title = QLabel("Matched Skills")
        keywords_title.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 5px;
            }
        """)
        content_layout.addWidget(keywords_title)
        
        # Keywords with modern card design
        self.create_keywords_section(content_layout)
        
        layout.addWidget(content_frame)
    
    def create_keywords_section(self, layout):
        """Create modern keywords section with gray cards"""
        # Scrollable container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setMaximumHeight(200)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f8f9fa;
                border-radius: 12px;
            }
            QScrollBar:vertical {
                background-color: #e9ecef;
                width: 6px;
                border-radius: 3px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #6c757d;
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #495057;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
        """)
        
        # Keywords container
        keywords_widget = QWidget()
        keywords_layout = QVBoxLayout(keywords_widget)
        keywords_layout.setContentsMargins(20, 15, 20, 15)
        keywords_layout.setSpacing(12)
        
        # Create keyword cards
        i = 0
        for key, keyword_data in (self.candidate_data["search_res"].items()):
            keyword_card = self.create_keyword_card(keyword_data, key, i)
            keywords_layout.addWidget(keyword_card)
            i += 1
        
        scroll_area.setWidget(keywords_widget)
        layout.addWidget(scroll_area)
    
    def create_keyword_card(self, keyword_data, name, index):
        """Create individual keyword card with gray theme"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 0px;
            }
            QFrame:hover {
                background-color: #f8f9fa;
            }
        """)
        
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(16, 12, 16, 12)
        card_layout.setSpacing(12)
        
        # Index number with gray circle background
        index_label = QLabel(str(index))
        index_label.setFixedSize(24, 24)
        index_label.setAlignment(Qt.AlignCenter)
        index_label.setStyleSheet("""
            QLabel {
                background-color: #6c757d;
                color: white;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
            }
        """)
        card_layout.addWidget(index_label)
        
        # Keyword info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        keyword_name = QLabel(name)
        keyword_name.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        
        occurrences = keyword_data["occurrence"]
        occurrence_text = f"{occurrences} {'occurrence' if occurrences == 1 else 'occurrences'}"
        occurrence_label = QLabel(occurrence_text)
        occurrence_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
            }
        """)
        
        info_layout.addWidget(keyword_name)
        info_layout.addWidget(occurrence_label)
        card_layout.addLayout(info_layout)
        
        # Occurrence count badge
        count_badge = QLabel(str(occurrences))
        count_badge.setFixedSize(32, 20)
        count_badge.setAlignment(Qt.AlignCenter)
        count_badge.setStyleSheet("""
            QLabel {
                background-color: #e9ecef;
                color: #495057;
                border-radius: 10px;
                font-size: 11px;
                font-weight: 600;
            }
        """)
        card_layout.addWidget(count_badge)
        
        return card

    def add_shadow_effect(self):
        """Add modern drop shadow effect"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.card_container.setGraphicsEffect(shadow)
    
    def animate_entrance(self):
        """Add entrance animation"""
        self.setWindowOpacity(0)
        
        # Fade in animation
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(200)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_animation.start()
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def create_footer_section(self, layout):
        """Create modern footer with gray-themed action buttons"""
        footer_frame = QFrame()
        footer_frame.setFixedHeight(80)
        footer_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
                border-top: 1px solid #e9ecef;
            }
        """)
        
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(30, 20, 30, 20)
        footer_layout.setSpacing(15)
        
        # Close button (secondary)
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e9ecef;
                color: #495057;
                border: none;
                border-radius: 20px;
                padding: 0px 24px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #dee2e6;
            }
            QPushButton:pressed {
                background-color: #ced4da;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        footer_layout.addStretch()
        footer_layout.addWidget(close_btn)
        
        # Summary button - Open CV Summary Dialog
        summary_btn = QPushButton("📄 Summary")
        summary_btn.setFixedHeight(40)
        summary_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 0px 24px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        summary_btn.clicked.connect(self.show_cv_summary)
        
        # View CV button (darker gray primary)
        cv_btn = QPushButton("📋 View CV")
        cv_btn.setFixedHeight(40)
        cv_btn.setStyleSheet("""
            QPushButton {
                background-color: #495057;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 0px 24px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3d4449;
            }
            QPushButton:pressed {
                background-color: #343a40;
            }
        """)
        cv_btn.clicked.connect(lambda: self.cv_requested.emit(self.candidate_data["path"]))
        
        footer_layout.addWidget(summary_btn)
        footer_layout.addWidget(cv_btn)
        
        layout.addWidget(footer_frame)
    
    def show_cv_summary(self):
        """Show CV Summary dialog"""
        summary_dialog = CVSummaryDialog(self.candidate_data, self)
        summary_dialog.exec_()