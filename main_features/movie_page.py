import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QGridLayout, QDialog, QMessageBox, QLineEdit, QStyle,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QUrl, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

def get_trailer_path(filename):
    """Finds the video file comfortably."""
    base_dir = os.getcwd() 
    possible_paths = [
        os.path.join(base_dir, "main_features", "trailers", filename),
        os.path.join(base_dir, "trailers", filename),
        os.path.join(base_dir, filename)
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

MY_MOVIES = [
    {
        "title": "Frozen", 
        "desc": "Anna sets out on a journey with an iceman, his reindeer, and a snowman to find her sister Elsa.", 
        "image": "https://upload.wikimedia.org/wikipedia/en/0/05/Frozen_%282013_film%29_poster.jpg", 
        "trailer": "Frozen.mp4" 
    },
    {
        "title": "Moana 2", 
        "desc": "Moana must journey to the far seas.", 
        "image": "https://upload.wikimedia.org/wikipedia/en/7/73/Moana_2_poster.jpg", 
        "trailer": "Moana2.mp4"
    },
    {
        "title": "Toy Story", 
        "desc": "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him.", 
        "image": "https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg", 
        "trailer": "ToyStory.mp4"
    },
    {
        "title": "The Lion King", 
        "desc": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.", 
        "image": "https://upload.wikimedia.org/wikipedia/en/3/3d/The_Lion_King_poster.jpg", 
        "trailer": "LionKing.mp4"
    },
    {
        "title": "Finding Nemo", 
        "desc": "After his son is captured in the Great Barrier Reef and taken to Sydney, a timid clownfish sets out to bring him home.", 
        "image": "https://upload.wikimedia.org/wikipedia/en/2/29/Finding_Nemo.jpg", 
        "trailer": "FindingNemo.mp4"
    },
    {
        "title": "Deadpool & Wolverine", 
        "desc": "Changing the history of the MCU.", 
        "image": "https://upload.wikimedia.org/wikipedia/en/4/4c/Deadpool_%26_Wolverine_poster.jpg", 
        "trailer": "Deadpool.mp4"
    },
    {
        "title": "Venom 3", 
        "desc": "Eddie and Venom are on the run.", 
        "image": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/aosm8NMQ3UyoBVpSxyimorCQykC.jpg", 
        "trailer": "Venom.mp4"
    },
    {
        "title": "Inside Out 2", 
        "desc": "New Emotions arrive in Riley's mind.", 
        "image": "https://upload.wikimedia.org/wikipedia/en/f/f7/Inside_Out_2_poster.jpg", 
        "trailer": "InsideOut2.mp4"
    }
]

class TrailerWindow(QDialog):
    def __init__(self, video_path, title):
        super().__init__()
        self.setWindowTitle(f"Watching: {title}")
        self.resize(1000, 700) 
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.video_widget = QVideoWidget()
        self.video_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.video_widget)

        self.controls = QFrame()
        self.controls.setFixedHeight(80)
        self.controls.setStyleSheet("background-color: #111; border-top: 2px solid #550000;")
        
        ctrl_layout = QHBoxLayout(self.controls)
        ctrl_layout.setContentsMargins(20, 10, 20, 10)

        btn_back = QPushButton(" BACK")
        btn_back.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack))
        btn_back.setFixedSize(120, 45)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #333; color: white; border-radius: 5px; font-weight: bold; border: 1px solid #555; }
            QPushButton:hover { background-color: #555; border-color: white; }
        """)
        btn_back.clicked.connect(self.close)
        ctrl_layout.addWidget(btn_back)

        ctrl_layout.addStretch()

        self.play_btn = QPushButton(" PAUSE")
        self.play_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        self.play_btn.setFixedSize(150, 50)
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.setStyleSheet("""
            QPushButton { 
                background-color: #b30000; 
                color: white; 
                border-radius: 25px; 
                font-weight: bold; 
                font-size: 16px; 
                border: 2px solid #ff0000; 
            }
            QPushButton:hover { background-color: #ff0000; box-shadow: 0 0 10px red; }
        """)
        self.play_btn.clicked.connect(self.toggle_play)
        ctrl_layout.addWidget(self.play_btn)

        ctrl_layout.addStretch()
        
        # Spacer for balance
        spacer = QWidget(); spacer.setFixedWidth(120)
        ctrl_layout.addWidget(spacer)

        layout.addWidget(self.controls)

        # Player Logic
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(video_path))
        self.audio.setVolume(1.0)
        self.player.play()

    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.play_btn.setText(" RESUME")
            self.play_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        else:
            self.player.play()
            self.play_btn.setText(" PAUSE")
            self.play_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))

    def closeEvent(self, event):
        self.player.stop()
        super().closeEvent(event)

class ImageLoader(QThread):
    image_loaded = pyqtSignal(str, QPixmap)
    def __init__(self, url, title):
        super().__init__()
        self.url = url; self.title = title

    def run(self):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            d = requests.get(self.url, headers=headers, verify=False, timeout=5).content
            p = QPixmap(); p.loadFromData(d)
            if not p.isNull():
                self.image_loaded.emit(self.title, p)
        except: pass

class MoviePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("moviesPage")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("MOVIES & TV SHOWS")
        title.setStyleSheet("font-size: 32px; font-weight: 900; color: #ff0000; letter-spacing: 2px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Search
        self.search_inp = QLineEdit()
        self.search_inp.setPlaceholderText("🔍 Search movies...")
        self.search_inp.setFixedSize(600, 50)
        self.search_inp.setStyleSheet("""
            QLineEdit { background: rgba(0,0,0,0.7); color: white; border: 1px solid #550000; border-radius: 25px; padding-left: 20px; font-size: 16px; }
            QLineEdit:focus { border: 1px solid #ff0000; background: black; }
        """)
        self.search_inp.textChanged.connect(self.filter_movies)
        layout.addWidget(self.search_inp, alignment=Qt.AlignmentFlag.AlignCenter)

        # Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(30)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(self.container)
        layout.addWidget(scroll)

        self.cards = []
        self.img_labels = {}
        self.load_movies()

    def load_movies(self):
        row, col = 0, 0
        for data in MY_MOVIES:
            card = self.create_card(data)
            self.grid.addWidget(card, row, col)
            self.cards.append((data['title'], card))
            col += 1
            if col >= 4: col = 0; row += 1

    def create_card(self, data):
        card = QFrame()
        card.setFixedSize(240, 460)
        card.setStyleSheet("""
            QFrame { background: rgba(10,0,0,0.85); border: 1px solid #440000; border-radius: 15px; } 
            QFrame:hover { border: 1px solid #ff0000; background: rgba(30,0,0,0.95); margin-top: -5px; }
        """)
        
        l = QVBoxLayout(card)
        l.setContentsMargins(12, 12, 12, 12)

        # Image
        img = QLabel()
        img.setFixedSize(215, 300)
        img.setStyleSheet("background: #200; border-radius: 8px; color: #aaa;")
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setScaledContents(True)
        img.setText("Loading Image...")
        l.addWidget(img)
        
        self.img_labels[data['title']] = img
        loader = ImageLoader(data['image'], data['title'])
        loader.image_loaded.connect(self.set_image)
        loader.start()
        setattr(self, f"ldr_{data['title']}", loader)

        t = QLabel(data['title'])
        t.setWordWrap(True)
        t.setStyleSheet("color: white; font-weight: bold; font-size: 16px; border: none; background: transparent; margin-top: 5px;")
        l.addWidget(t)

        btn = QPushButton("WATCH")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton { background: #990000; color: white; border: none; padding: 10px; border-radius: 5px; font-weight: bold; } 
            QPushButton:hover { background: #ff0000; }
        """)
        btn.clicked.connect(lambda _, f=data['trailer'], t=data['title']: self.play_trailer(f, t))
        l.addWidget(btn)

        return card

    def set_image(self, title, pix):
        if title in self.img_labels: self.img_labels[title].setPixmap(pix)

    def play_trailer(self, file, title):
        path = get_trailer_path(file)
        
        if path:
            win = TrailerWindow(path, title)
            win.exec()
        else:
            QMessageBox.critical(self, "Error", f"Video file not found: {file}\n\nPlease ensure it is in the 'trailers' folder.")

    def filter_movies(self):
        txt = self.search_inp.text().lower()
        for title, widget in self.cards:
            widget.setVisible(txt in title.lower())