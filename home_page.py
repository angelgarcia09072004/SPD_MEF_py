import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QGridLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor

class ImageLoader(QThread):
    image_loaded = pyqtSignal(QPixmap)
    def __init__(self, url):
        super().__init__()
        self.url = url
    def run(self):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            data = requests.get(self.url, headers=headers, verify=False, timeout=5).content
            pix = QPixmap()
            pix.loadFromData(data)
            if not pix.isNull():
                self.image_loaded.emit(pix)
        except: pass

class HomePage(QWidget):
    def __init__(self, username, main_window):
        super().__init__()
        self.main_window = main_window
        self.setObjectName("homePage")
        
        self.init_ui(username)

    def init_ui(self, username):
        stack_layout = QGridLayout(self)
        stack_layout.setContentsMargins(0,0,0,0)

        self.content_widget = QWidget()

        self.content_widget.setStyleSheet("background-color: rgba(5, 5, 5, 0.85);") 
        stack_layout.addWidget(self.content_widget, 0, 0)

        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(50, 60, 50, 50)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- WELCOME SECTION ---
        welcome = QLabel(f"WELCOME BACK, {username.upper()}")
        welcome.setStyleSheet("""
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 42px; 
                font-weight: 900; 
                color: white; 
                margin-bottom: -5px;
                letter-spacing: 1px;
            }
        """)
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)

        subtitle = QLabel("What would you like to explore today?")
        subtitle.setStyleSheet("""
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px; 
                color: #bbbbbb; 
                font-weight: 400;
                margin-top: 0px;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(60)

        # --- CATEGORY CARDS ---
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(40) 
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Card 1: Movies
        cards_layout.addWidget(self.create_card(
            "MOVIES & TV", 
            "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500", 
            self.main_window.show_movie_page,
            "Cinema, Series & More"
        ))
        
        # Card 2: Music
        cards_layout.addWidget(self.create_card(
            "MUSIC LIBRARY", 
            "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500", 
            self.main_window.show_music_page,
            "Listen to your favorites"
        ))
        
        # Card 3: Games
        cards_layout.addWidget(self.create_card(
            "ARCADE GAMES", 
            "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=500", 
            self.main_window.show_games_page,
            "Play & Challenge yourself"
        ))

        layout.addLayout(cards_layout)
        layout.addStretch()

    def create_card(self, title, img_url, func, desc_text):
        card = QFrame()
        card.setFixedSize(320, 420)
        
        # CSS FOR THE CARD
        card.setStyleSheet("""
            QFrame { 
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a1a1a, stop:1 #0d0d0d);
                border: 1px solid #333;
                border-bottom: 3px solid #b30000;
                border-radius: 20px;
            }
            QFrame:hover { 
                background-color: #222;
                border: 1px solid #ff0000;
                border-bottom: 3px solid #ff0000;
                margin-top: -10px; /* Lift Animation */
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 10)
        card.setGraphicsEffect(shadow)

        l = QVBoxLayout(card)
        l.setContentsMargins(15, 15, 15, 20)
        l.setSpacing(10)

        # Image Container
        img_lbl = QLabel()
        img_lbl.setScaledContents(True)
        img_lbl.setFixedHeight(220)
        img_lbl.setStyleSheet("border-radius: 12px; background-color: #000; border: none;")
        
        loader = ImageLoader(img_url)
        loader.image_loaded.connect(img_lbl.setPixmap)
        loader.start()
        setattr(self, f"ldr_{title}", loader)

        l.addWidget(img_lbl)

        # Title
        lbl = QLabel(title)
        lbl.setStyleSheet("""
            font-size: 22px; 
            font-weight: 800; 
            color: white; 
            border: none; 
            background: transparent;
            letter-spacing: 1px;
        """)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addWidget(lbl)

        # Description (Small Text)
        desc = QLabel(desc_text)
        desc.setStyleSheet("""
            font-size: 12px; 
            color: #888; 
            border: none; 
            background: transparent;
            margin-bottom: 5px;
        """)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addWidget(desc)

        # Button
        btn = QPushButton("EXPLORE")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(40)
        btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #990000, stop:1 #cc0000);
                color: white; 
                border-radius: 20px; 
                font-weight: bold; 
                border: none;
                font-size: 13px;
                letter-spacing: 1px;
            }
            QPushButton:hover { 
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #cc0000, stop:1 #ff0000);
                box-shadow: 0 0 10px #ff0000;
            }
        """)
        btn.clicked.connect(func)
        l.addWidget(btn)

        return card