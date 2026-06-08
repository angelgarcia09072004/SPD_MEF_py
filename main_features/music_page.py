import os
import shutil
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QGridLayout, QFileDialog, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

# --- HELPERS ---
def get_music_path(filename):
    """Finds the audio file in the music folder."""
    return os.path.join(os.getcwd(), "music", filename)

def get_cover_image():
    """Finds the default musicbg.jpg image."""
    # Look in the 'music' folder first, then the main folder
    path = os.path.join(os.getcwd(), "music", "musicbg.jpg")
    if not os.path.exists(path):
        path = os.path.join(os.getcwd(), "musicbg.jpg")
    return path

# --- MUSIC DATA (No internet links needed anymore) ---
MUSIC_DATA = [
    {"title": "Elesi", "artist": "Rivermaya", "file": "Elesi.mp3"},
    {"title": "Ang Huling El Bimbo", "artist": "Eraserheads", "file": "El Bimbo.mp3"},
    {"title": "With A Smile", "artist": "Eraserheads", "file": "With A Smile.mp3"},
    {"title": "Killing Me Softly", "artist": "Fugees", "file": "Killing Me Softly.mp3"},
    {"title": "Waterfalls", "artist": "TLC", "file": "Waterfalls.mp3"},
    {"title": "No Scrubs", "artist": "TLC", "file": "No Scrubs.mp3"},
    {"title": "Wonderwall", "artist": "Oasis", "file": "Wonderwall.mp3"},
    {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "file": "Nirvana.mp3"}
]

class MusicPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("musicPage")
        
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.5)
        self.current_file = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40,40,40,40)

        # Title
        header = QLabel("MUSIC LIBRARY")
        header.setStyleSheet("font-size: 32px; font-weight: bold; color: #ff0000; letter-spacing: 2px;")
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

        # Search Bar
        self.search_inp = QLineEdit()
        self.search_inp.setPlaceholderText("🎵 Search songs or artists...")
        self.search_inp.setFixedSize(600, 50)
        self.search_inp.setStyleSheet("""
            QLineEdit { 
                background: rgba(0,0,0,0.7); 
                color: white; 
                border: 1px solid #550000; 
                border-radius: 25px; 
                padding-left: 20px; 
                font-size: 16px; 
            }
            QLineEdit:focus { border: 1px solid #ff0000; background: black; }
        """)
        self.search_inp.textChanged.connect(self.filter_music)
        layout.addWidget(self.search_inp, alignment=Qt.AlignmentFlag.AlignCenter)

        # Status Label
        self.status_lbl = QLabel("Select a track to play")
        self.status_lbl.setStyleSheet("color: #ccc; font-size: 16px; margin: 10px 0 20px 0; font-weight: bold;")
        layout.addWidget(self.status_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(container)
        self.grid.setSpacing(25)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.cards = []
        self.load_music()

    def load_music(self):
        # Load the default image ONCE to save memory
        default_pixmap = QPixmap(get_cover_image())
        
        row, col = 0, 0
        for m in MUSIC_DATA:
            card = self.create_card(m, default_pixmap)
            self.grid.addWidget(card, row, col)
            self.cards.append((m['title'], m['artist'], card))
            col += 1
            if col >= 4: col = 0; row += 1

    def create_card(self, data, pixmap):
        card = QFrame()
        card.setFixedSize(230, 420)
        card.setStyleSheet("""
            QFrame { background: rgba(10,0,0,0.9); border: 1px solid #440000; border-radius: 12px; }
            QFrame:hover { border: 1px solid #ff0000; background: rgba(20,0,0,0.95); }
        """)

        l = QVBoxLayout(card)
        l.setContentsMargins(10,10,10,10)

        # Image (Uses the local 'musicbg.jpg')
        img = QLabel()
        img.setFixedSize(205, 205)
        img.setStyleSheet("background: #200; color: #555; border-radius: 8px;")
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setScaledContents(True)
        
        if not pixmap.isNull():
            img.setPixmap(pixmap)
        else:
            img.setText("🎵") # Fallback if musicbg.jpg is missing
            
        l.addWidget(img)

        # Title
        t = QLabel(data['title'])
        t.setStyleSheet("color: white; font-weight: bold; font-size: 15px; background: transparent; border: none;")
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        t.setWordWrap(True)
        l.addWidget(t)

        # Artist
        a = QLabel(data['artist'])
        a.setStyleSheet("color: #999; font-size: 13px; background: transparent; border: none;")
        a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addWidget(a)
        
        l.addStretch()

        # --- CONTROLS ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)

        # PLAY
        btn_play = QPushButton("▶")
        btn_play.setToolTip("Play")
        btn_play.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_play.setFixedSize(60, 35)
        btn_play.setStyleSheet("QPushButton { background: #008800; color: white; border: none; border-radius: 5px; font-size: 16px; } QPushButton:hover { background: #00aa00; }")
        btn_play.clicked.connect(lambda _, f=data['file'], t=data['title']: self.play_song(f, t))
        btn_layout.addWidget(btn_play)

        # PAUSE
        btn_pause = QPushButton("⏸")
        btn_pause.setToolTip("Pause")
        btn_pause.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_pause.setFixedSize(60, 35)
        btn_pause.setStyleSheet("QPushButton { background: #aa8800; color: white; border: none; border-radius: 5px; font-size: 16px; } QPushButton:hover { background: #ccaa00; }")
        btn_pause.clicked.connect(self.pause_song)
        btn_layout.addWidget(btn_pause)

        # SAVE
        btn_save = QPushButton("⬇")
        btn_save.setToolTip("Save")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedSize(60, 35)
        btn_save.setStyleSheet("QPushButton { background: #880000; color: white; border: none; border-radius: 5px; font-size: 16px; } QPushButton:hover { background: #aa0000; }")
        btn_save.clicked.connect(lambda _, f=data['file']: self.save_song(f))
        btn_layout.addWidget(btn_save)

        l.addLayout(btn_layout)
        return card

    def play_song(self, filename, title):
        path = get_music_path(filename)
        if not os.path.exists(path):
            QMessageBox.warning(self, "Error", f"File not found: {filename}")
            return

        if self.current_file != filename:
            self.player.setSource(QUrl.fromLocalFile(path))
            self.current_file = filename
        
        self.player.play()
        self.status_lbl.setText(f"Playing Now: {title} 🎵")
        self.status_lbl.setStyleSheet("color: #00ff00; font-size: 16px; margin: 10px 0 20px 0; font-weight: bold;")

    def pause_song(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.status_lbl.setText("Paused ⏸")
            self.status_lbl.setStyleSheet("color: #ffa500; font-size: 16px; margin: 10px 0 20px 0; font-weight: bold;")

    def save_song(self, filename):
        src = get_music_path(filename)
        if not os.path.exists(src):
            QMessageBox.warning(self, "Error", "File missing.")
            return
        dst, _ = QFileDialog.getSaveFileName(self, "Save MP3", filename, "Audio (*.mp3)")
        if dst:
            try:
                shutil.copy(src, dst)
                QMessageBox.information(self, "Success", "Saved!")
            except: pass

    def filter_music(self):
        txt = self.search_inp.text().lower()
        for title, artist, widget in self.cards:
            widget.setVisible(txt in title.lower() or txt in artist.lower())