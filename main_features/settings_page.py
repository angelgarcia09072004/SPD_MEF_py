from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, 
    QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class SettingsPage(QWidget):
    def __init__(self, username, main_window):
        super().__init__()
        self.username = username
        self.main_window = main_window
        self.setObjectName("settingsPage")
        
        self.init_ui()

    def init_ui(self):
        # --- MAIN LAYOUT ---
        # This layout centers the card in the middle of the screen
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 1. Page Title (Outside the box)
        page_title = QLabel("SETTINGS")
        page_title.setStyleSheet("""
            font-size: 36px; 
            font-weight: 900; 
            color: #ff0000; 
            letter-spacing: 4px;
            margin-bottom: 20px;
        """)
        page_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(page_title)

        # 2. The Information Card (Container)
        self.card = QFrame()
        self.card.setFixedWidth(700) # Fixed width for readability
        self.card.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 5, 5, 0.95); 
                border: 1px solid #440000;
                border-radius: 25px;
            }
        """)

        # Add Shadow for depth
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(255, 0, 0, 40)) # Subtle red glow
        shadow.setOffset(0, 0)
        self.card.setGraphicsEffect(shadow)

        # Layout INSIDE the card
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(60, 50, 60, 50) # Increased padding
        card_layout.setSpacing(25)

        # --- CONTENT SECTIONS ---

        # About Us
        self.add_section(card_layout, "ABOUT US", 
            "SPD (Stream, Play, Discover) is an all-in-one entertainment platform designed to "
            "bring movies, music, and video games into a single, seamless experience. We aim to "
            "reduce digital clutter by unifying your favorite media."
        )

        self.add_divider(card_layout)

        # Vision
        self.add_section(card_layout, "VISION", 
            "To become the leading offline-first entertainment hub that empowers users to "
            "explore, organize, and enjoy media without boundaries or interruptions."
        )

        self.add_divider(card_layout)

        # Mission
        self.add_section(card_layout, "MISSION", 
            "Our mission is to provide a robust, user-friendly application that integrates high-"
            "quality video streaming, music playback, and interactive gaming into one unified, "
            "aesthetically pleasing interface."
        )

        # Footer (Credits)
        card_layout.addSpacing(20)
        footer = QLabel("Developed by: Angel, Shaine, Lovely  |  Version: 1.0.0")
        footer.setStyleSheet("color: #666; font-size: 12px; font-weight: bold;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(footer)

        # Add card to main layout
        main_layout.addWidget(self.card)

    def add_section(self, layout, title_text, body_text):
        """Helper to create a beautifully styled section."""
        
        # Title
        title = QLabel(title_text)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 22px; 
                font-weight: bold; 
                color: #ff3333; 
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(title)

        # Body Text
        body = QLabel(body_text)
        body.setWordWrap(True)
        body.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.setStyleSheet("""
            QLabel {
                font-size: 15px; 
                color: #e0e0e0; 
                line-height: 140%;
                background: transparent;
                border: none;
                padding-left: 10px;
                padding-right: 10px;
            }
        """)
        layout.addWidget(body)

    def add_divider(self, layout):
        """Helper to add a subtle gradient divider."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedHeight(2)
        line.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 transparent, stop:0.5 #550000, stop:1 transparent);
            border: none;
            margin-top: 10px;
            margin-bottom: 10px;
        """)
        layout.addWidget(line)