import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QStackedWidget, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer

# Import modules
from database import create_users_table
from login_page import LoginPage
from home_page import HomePage
from main_features.movie_page import MoviePage
from main_features.music_page import MusicPage
from main_features.games_page import GamesPage
from main_features.settings_page import SettingsPage
from styles import QSS_THEME

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPD - Stream, Play, Discover")
        self.setMinimumSize(1280, 720)
        self.setStyleSheet(QSS_THEME)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout(self.central)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        self.login = LoginPage(self)
        self.login.login_successful.connect(self.on_login)
        self.stack.addWidget(self.login)

        create_users_table()

    def on_login(self, username):
        self.user_data = {'username': username}
        self.setup_main_interface()
        self.stack.setCurrentWidget(self.app_container)

    def setup_main_interface(self):
        self.app_container = QWidget()
        layout = QHBoxLayout(self.app_container)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # --- SIDEBAR ---
        self.sidebar_container = QFrame()
        self.sidebar_container.setObjectName("sidebar")
        self.sidebar_container.setFixedWidth(250)
        sb_layout = QVBoxLayout(self.sidebar_container)
        sb_layout.setContentsMargins(10, 20, 10, 20)
        sb_layout.setSpacing(10)

        # Hamburger Menu Button
        self.toggle_btn = QPushButton("☰ MENU")
        self.toggle_btn.setObjectName("toggleButton")
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        sb_layout.addWidget(self.toggle_btn)

        sb_layout.addSpacing(20)

        # Navigation Buttons (Label, Function, IconPlaceholder)
        self.menu_items = [
            ("Home", self.show_home, "🏠"), 
            ("Movies & TV", self.show_movie_page, "🎬"), 
            ("Music", self.show_music_page, "🎵"), 
            ("Video Games", self.show_games_page, "🎮"), 
            ("Settings", self.show_settings_page, "⚙️")
        ]
        
        self.btns = []
        for text, func, icon in self.menu_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setObjectName("sidebarButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(func)
            # Store the full text for later use
            btn.full_text = f"{icon}  {text}"
            btn.icon_text = icon
            sb_layout.addWidget(btn)
            self.btns.append(btn)

        sb_layout.addStretch()

        self.logout_btn = QPushButton("🚪  Log Out")
        self.logout_btn.setObjectName("logoutButton")
        self.logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_btn.clicked.connect(self.logout)
        sb_layout.addWidget(self.logout_btn)

        # --- CONTENT AREA ---
        self.pg_stack = QStackedWidget()
        self.pg_home = HomePage(self.user_data['username'], self)
        self.pg_mov = MoviePage(self)
        self.pg_mus = MusicPage(self)
        self.pg_gam = GamesPage(self)
        self.pg_set = SettingsPage(self.user_data['username'], self)

        for p in [self.pg_home, self.pg_mov, self.pg_mus, self.pg_gam, self.pg_set]:
            self.pg_stack.addWidget(p)

        layout.addWidget(self.sidebar_container)
        layout.addWidget(self.pg_stack)
        
        self.stack.addWidget(self.app_container)
        self.highlight(0)
        self.is_collapsed = False

    def toggle_sidebar(self):
        width = self.sidebar_container.width()
        
        if not self.is_collapsed:
            # COLLAPSE: Hide text FIRST, then shrink
            self.new_width = 70
            self.toggle_btn.setText("☰")
            for btn in self.btns:
                btn.setText(btn.icon_text) # Show only icon
            self.logout_btn.setText("🚪")
            self.is_collapsed = True
        else:
            # EXPAND: Grow FIRST, then show text (handled in animation finished)
            self.new_width = 250
            self.toggle_btn.setText("☰ MENU")
            self.is_collapsed = False

        self.anim = QPropertyAnimation(self.sidebar_container, b"minimumWidth")
        self.anim.setDuration(250)
        self.anim.setStartValue(width)
        self.anim.setEndValue(self.new_width)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.finished.connect(self.animation_finished)
        self.anim.start()

    def animation_finished(self):
        # If we just finished expanding, restore the text
        if not self.is_collapsed:
            for btn in self.btns:
                btn.setText(btn.full_text)
            self.logout_btn.setText("🚪  Log Out")

    def show_home(self): self.pg_stack.setCurrentWidget(self.pg_home); self.highlight(0)
    def show_movie_page(self): self.pg_stack.setCurrentWidget(self.pg_mov); self.highlight(1)
    def show_music_page(self): self.pg_stack.setCurrentWidget(self.pg_mus); self.highlight(2)
    def show_games_page(self): self.pg_stack.setCurrentWidget(self.pg_gam); self.highlight(3)
    def show_settings_page(self): self.pg_stack.setCurrentWidget(self.pg_set); self.highlight(4)

    def highlight(self, idx):
        for b in self.btns:
            b.setProperty("active", False); b.style().polish(b)
        if 0 <= idx < len(self.btns):
            self.btns[idx].setProperty("active", True); self.btns[idx].style().polish(self.btns[idx])

    def logout(self):
        if QMessageBox.question(self, "Logout", "Exit application?", QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.stack.setCurrentWidget(self.login); self.login.enable_input()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())