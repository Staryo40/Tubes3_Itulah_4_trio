from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QWidget, QScrollArea, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor

from local_enum import TextFormat

class CVSummaryDialog(QDialog):
    def __init__(self, candidate_data, parent=None):
        super().__init__(parent)
        self.candidate_data = candidate_data
        self.setWindowTitle("")  # Remove title
        self.setModal(True)
        self.setFixedSize(650, 700)
        
        # Remove window frame for modern look
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setup_ui()
        self.add_shadow_effect()
        self.animate_entrance()
    
    def setup_ui(self):
        # Main layout with margins for shadow
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Create the modern card container
        self.card_container = QFrame()
        self.card_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 24px;
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
        header_frame.setFixedHeight(140)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #8e9aaf, stop:1 #6c757d);
                border-top-left-radius: 24px;
                border-top-right-radius: 24px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(35, 30, 35, 25)
        header_layout.setSpacing(12)
        
        # Title with modern typography
        title_label = QLabel("📋 CV Summary")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: 700;
                letter-spacing: -0.3px;
                background-color: transparent;
            }
        """)
        header_layout.addWidget(title_label)
        
        # Candidate name
        name_label = QLabel(self.candidate_data["name"])
        name_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 32px;
                font-weight: 800;
                letter-spacing: -0.8px;
                margin-top: 5px;
                background-color: transparent;
            }
        """)
        header_layout.addWidget(name_label)
        
        # Info pills container
        info_container = QHBoxLayout()
        info_container.setContentsMargins(0, 8, 0, 0)
        info_container.setSpacing(12)
    
        
        
        info_container.addStretch()
        header_layout.addLayout(info_container)
        
        layout.addWidget(header_frame)
    
    def create_content_section(self, layout):
        """Create scrollable content section with modern cards"""
        # Scrollable container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 8px;
                border-radius: 4px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #6c757d;
                border-radius: 4px;
                min-height: 30px;
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
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(35, 30, 35, 20)
        content_layout.setSpacing(25)
        
        # Personal Information Section
        self.create_personal_info_section(content_layout)
        
        # Dynamic sections based on summary data
        self.create_dynamic_sections(content_layout)
        
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

    def create_dynamic_sections(self, layout):
        """Create sections dynamically based on summary data structure"""
        summary_data = self.candidate_data.get('summary', {})

        if not isinstance(summary_data, dict):
            print("Invalid summary data format. Expected a dictionary.")
            return

        for header, value in summary_data.items():
            if not isinstance(value, dict):
                continue

            section_type = value.get('type', 'list')  # Default to list if no type specified
            content = value.get('content', [])

            # Create section dynamically based on header and type
            self.create_flexible_section(layout, header, content, section_type)
        
        if not header or not content:
        
            print(f"Skipping section with missing header or content: {header}")
            return

    def create_flexible_section(self, layout, header, content, section_type):
        """Create a flexible section that adapts to any header and content"""
        print(f"Creating section: {header} with type {section_type} and content: {content}")
        
        # Map common headers to appropriate icons
        icon_map = {
            'skill': '🛠️',
            'skills': '🛠️',
            'job history': '💼',
            'work experience': '💼',
            'experience': '💼',
            'education': '🎓',
            'projects': '🚀',
            'certifications': '🏆',
            'certificates': '🏆',
            'languages': '🌐',
            'achievements': '⭐',
            'awards': '🏅',
            'interests': '🎯',
            'hobbies': '🎨',
            'publications': '📚',
            'research': '🔬',
            'volunteer': '🤝',
            'references': '👥',
            'contact': '📞',
            'personal': '👤',
            'summary': '📝',
            'objective': '🎯',
            'profile': '👤'
        }
        
        # Get icon for the header (case insensitive)
        icon = icon_map.get(header.lower(), '📋')
        
        # Create section header
        layout.addWidget(self.create_section_header(header, icon))
        
        # Create section card
        section_card = QFrame()
        section_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        
        section_layout = QVBoxLayout(section_card)
        section_layout.setContentsMargins(25, 20, 25, 20)
        section_layout.setSpacing(15)

        if len(content) > 10:
            content = content[:10]  
        
        # Handle different section types
        if section_type == TextFormat.Bullet:
            self.create_bullet_content(section_layout, content, header)
        else:  # Default to list type
            self.create_list_content(section_layout, content, header)
        
        layout.addWidget(section_card)

    def create_bullet_content(self, layout, content, header):
        """Create bullet-style content with tags/pills"""
        
        # Determine styling based on header type
        if header.lower() in ['skill', 'skills']:  
            # Skills get special dark gray styling 
            tag_style = """
                QLabel {
                    background-color: #6c757d;
                    color: white;
                    padding: 10px 18px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 600;
                }
            """
            tag_height = 40
            items_per_row = 4
        else:
            # Other bullet items get lighter styling
            tag_style = """
                QLabel {
                    background-color: #e9ecef;
                    color: #495057;
                    padding: 8px 16px;
                    border-radius: 16px;
                    font-size: 12px;
                    font-weight: 600;
                }
            """
            tag_height = 32
            items_per_row = 3
        
        # Create tags in rows
        current_row = QHBoxLayout()
        current_row.setSpacing(10)
        items_in_current_row = 0
        
        for item in content:
            if items_in_current_row >= items_per_row:
                current_row.addStretch()
                layout.addLayout(current_row)
                current_row = QHBoxLayout()
                current_row.setSpacing(10)
                items_in_current_row = 0
            
            item_tag = QLabel(str(item))
            item_tag.setStyleSheet(tag_style)
            item_tag.setFixedHeight(tag_height)
            
            current_row.addWidget(item_tag)
            items_in_current_row += 1
        
        if items_in_current_row > 0:
            current_row.addStretch()
            layout.addLayout(current_row)

    def create_list_content(self, layout, content, header):
        for i, exp in enumerate(content):
            exp_container = QFrame()
            exp_container.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    border: none;
                    padding: 0px;
                    margin-bottom: 8px;
                }
            """)
            
            exp_layout = QHBoxLayout(exp_container)
            exp_layout.setContentsMargins(15, 12, 15, 12)
            exp_layout.setSpacing(12)
            
            # Number badge
            number_badge = QLabel(str(i + 1))
            number_badge.setFixedSize(24, 24)
            number_badge.setAlignment(Qt.AlignCenter)
            number_badge.setStyleSheet("""
                QLabel {
                    background-color: #6c757d;
                    color: white;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 600;
                }
            """)
            
            # Experience text
            exp_text = str(exp)
            exp_label = QLabel(exp_text)
            exp_label.setWordWrap(True)
            exp_label.setStyleSheet("""
                QLabel {
                    color: #495057;
                    font-size: 14px;
                    line-height: 1.4;
                }
            """)
            if (len(content) > 1):
                exp_layout.addWidget(number_badge)
            exp_layout.addWidget(exp_label, 1)
            
            layout.addWidget(exp_container)

    def create_section_header(self, title, icon=""):
        """Create consistent section headers"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                border: none;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        title_label = QLabel(f"{icon} {title}")
        title_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 16px;
                font-weight: 700;
                letter-spacing: -0.2px;
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        return header_frame
    
    def create_personal_info_section(self, layout):
        """Create personal information section"""
        layout.addWidget(self.create_section_header("Personal Information", "👤"))
        
        info_card = QFrame()
        info_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(25, 20, 25, 20)
        info_layout.setSpacing(12)

        print(f"Creating personal info section with data: {self.candidate_data}")
        
        # Phone
        if 'phone' in self.candidate_data:
            phone_label = QLabel(f"📱 {self.candidate_data['phone']}")
            phone_label.setStyleSheet("""
                QLabel {
                    color: #495057;
                    font-size: 14px;
                    padding: 8px 0px;
                }
            """)
            info_layout.addWidget(phone_label)
        
        # Address
        if 'address' in self.candidate_data:
            address_label = QLabel(f"📍 {self.candidate_data['address']}")
        if 'address' in self.candidate_data:
            address_label = QLabel(f"📍 {self.candidate_data['address']}")
            address_label.setStyleSheet("""
                QLabel {
                    color: #495057;
                    font-size: 14px;
                    padding: 8px 0px;
                }
            """)
            info_layout.addWidget(address_label)
        
        # Birthdate
        if 'dob' in self.candidate_data:
            birthdate_label = QLabel(f"📅 {self.candidate_data['dob']}")
            birthdate_label.setStyleSheet("""
                QLabel {
                    color: #495057;
                    font-size: 14px;
                    padding: 8px 0px;
                }
            """)
            info_layout.addWidget(birthdate_label)
        
        layout.addWidget(info_card)
    
    def create_footer_section(self, layout):
        """Create modern footer with action buttons"""
        footer_frame = QFrame()
        footer_frame.setFixedHeight(80)
        footer_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-bottom-left-radius: 24px;
                border-bottom-right-radius: 24px;
                border-top: 1px solid #e9ecef;
            }
        """)
        
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(35, 20, 35, 20)
        footer_layout.setSpacing(15)
        
        # Close button
        close_btn = QPushButton("✕ Close")
        close_btn.setFixedHeight(44)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e9ecef;
                color: #495057;
                border: none;
                border-radius: 22px;
                padding: 0px 28px;
                font-size: 14px;
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
        
        layout.addWidget(footer_frame)
    
    def add_shadow_effect(self):
        """Add modern drop shadow effect"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.card_container.setGraphicsEffect(shadow)
    
    def animate_entrance(self):
        """Add entrance animation"""
        self.setWindowOpacity(0)
        
        # Fade in animation
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(250)
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
