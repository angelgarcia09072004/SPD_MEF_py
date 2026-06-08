import sys
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QFrame, QMessageBox, QGridLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap, QColor
from database import authenticate_user

# --- 1. IMAGE DOWNLOADER ---
class ImageLoader(QThread):
    image_loaded = pyqtSignal(str, QPixmap)

    def __init__(self, url, img_type):
        super().__init__()
        self.url = url
        self.img_type = img_type

    def run(self):
        try:
            # Download image securely
            response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            pix = QPixmap()
            pix.loadFromData(response.content)
            self.image_loaded.emit(self.img_type, pix)
        except Exception as e:
            print(f"Error loading {self.img_type}: {e}")

# --- 2. LOGIN PAGE ---
class LoginPage(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("loginPage")
        
        # Image Links
        self.bg_url = "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?q=80&w=1920&auto=format&fit=crop" 
        self.icon_url = "https://cdn-icons-png.flaticon.com/512/9187/9187604.png"

        self.init_ui()
        
        # Start Downloading
        self.bg_loader = ImageLoader(self.bg_url, "bg")
        self.bg_loader.image_loaded.connect(self.set_image)
        self.bg_loader.start()

        self.icon_loader = ImageLoader(self.icon_url, "icon")
        self.icon_loader.image_loaded.connect(self.set_image)
        self.icon_loader.start()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.left_frame = QFrame()
        self.left_frame.setStyleSheet("background-color: #1a1a1a; border-right: 2px solid #550000;")
        
        # Use Grid to stack
        left_stack = QGridLayout(self.left_frame)
        left_stack.setContentsMargins(0, 0, 0, 0)

        # Layer 1: Background Image
        self.bg_label = QLabel()
        self.bg_label.setScaledContents(True)
        left_stack.addWidget(self.bg_label, 0, 0)

        # Layer 2: Text Overlay
        text_container = QWidget()
        text_container.setStyleSheet("background: transparent;")
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(60, 0, 60, 0) # Add side margins
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        # --- BIG TITLE ---
        self.header_label = QLabel("STREAM.\nPLAY.\nDISCOVER.", self)
        # Increased Size + Bold
        self.header_label.setStyleSheet("font-size: 80px; font-weight: 900; color: white; line-height: 100px;")
        
        # Add Shadow to make it readable
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 255)) # Black shadow
        shadow.setOffset(5, 5)
        self.header_label.setGraphicsEffect(shadow)
        
        text_layout.addWidget(self.header_label)

        # --- SUBTITLE ---
        self.subtitle_label = QLabel("Your ultimate entertainment hub.", self)
        self.subtitle_label.setStyleSheet("font-size: 24px; color: #ffdddd; font-weight: bold; margin-top: 10px;")
        
        # Add Shadow to subtitle too
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(15)
        shadow2.setColor(QColor(0, 0, 0, 255))
        shadow2.setOffset(3, 3)
        self.subtitle_label.setGraphicsEffect(shadow2)

        text_layout.addWidget(self.subtitle_label)
        
        left_stack.addWidget(text_container, 0, 0)

        main_layout.addWidget(self.left_frame, 65) 

        right_frame = QFrame()
        right_frame.setStyleSheet("background-color: #050505;")
        right_layout = QVBoxLayout(right_frame)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icon
        self.logo_label = QLabel("👤")
        self.logo_label.setFixedSize(100, 100)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("font-size: 60px; color: #ff0000; background: transparent;")
        right_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Welcome
        welcome = QLabel("WELCOME BACK")
        welcome.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff8888; margin-bottom: 20px; background: transparent;")
        right_layout.addWidget(welcome, alignment=Qt.AlignmentFlag.AlignCenter)

        # Form Container
        form_box = QFrame()
        form_box.setFixedWidth(350)
        form_box.setStyleSheet("background: transparent;")
        fb_layout = QVBoxLayout(form_box)
        
        # Username
        fb_layout.addWidget(QLabel("USERNAME", styleSheet="color:#888; font-weight:bold; font-size:12px;"))
        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("Enter username")
        self.user_in.setFixedHeight(45)
        self.user_in.setStyleSheet("background-color: #1a1a1a; border: 1px solid #333; color: white; border-radius: 5px; padding: 10px;")
        fb_layout.addWidget(self.user_in)

        fb_layout.addSpacing(15)

        # Password
        fb_layout.addWidget(QLabel("PASSWORD", styleSheet="color:#888; font-weight:bold; font-size:12px;"))
        self.pass_in = QLineEdit()
        self.pass_in.setPlaceholderText("Enter password")
        self.pass_in.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_in.setFixedHeight(45)
        self.pass_in.setStyleSheet(self.user_in.styleSheet())
        self.pass_in.returnPressed.connect(self.login)
        fb_layout.addWidget(self.pass_in)

        fb_layout.addSpacing(30)

        # Login Button
        btn = QPushButton("LOGIN")
        btn.setFixedHeight(50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton { background-color: #b30000; color: white; font-weight: bold; border-radius: 5px; font-size: 16px; }
            QPushButton:hover { background-color: #ff0000; }
        """)
        btn.clicked.connect(self.login)
        fb_layout.addWidget(btn)

        # Go Back
        back = QPushButton("Welcome Back!")
        back.setStyleSheet("color: #666; background: transparent; margin-top: 10px; border: none;")
        fb_layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)

        right_layout.addWidget(form_box, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(right_frame, 35)

    def set_image(self, typ, pix):
        if typ == "bg":
            self.bg_label.setPixmap(pix)
        elif typ == "icon":
            self.logo_label.setPixmap(pix.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def login(self):
        u = self.user_in.text().strip()
        p = self.pass_in.text().strip()
        if not u or not p:
            QMessageBox.warning(self, "Input", "Enter username and password")
            return
        if authenticate_user(u, p):
            self.login_successful.emit(u)
            self.user_in.clear()
            self.pass_in.clear()
        else:
            QMessageBox.critical(self, "Error", "Invalid Credentials")

    def enable_input(self):
        self.user_in.setFocus()