import sys
import os
import random
from functools import partial

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer

# --- STYLING ---
GAME_CARD_STYLE = """
    /* THE CARD CONTAINER */
    QFrame#gameFrame {
        background-color: rgba(10, 0, 0, 0.85); /* Dark Red/Black Background */
        border: 2px solid #b30000; /* DARK RED BORDER */
        border-radius: 15px;
    }
    QFrame#gameFrame:hover {
        border: 2px solid #ff0000; /* NEON RED BORDER ON HOVER */
        background-color: rgba(30, 0, 0, 0.9);
        box-shadow: 0 0 15px #ff0000;
    }

    /* TITLES INSIDE GAMES */
    QLabel { 
        color: #e0e0e0; 
        font-size: 14px; 
        background: transparent; 
        border: none; 
    }

    /* INPUT FIELDS */
    QLineEdit { 
        background-color: #220000; 
        color: white; 
        padding: 10px; 
        border-radius: 8px; 
        border: 1px solid #550000;
        font-weight: bold;
    }
    QLineEdit:focus { 
        border: 1px solid #ff0000; 
    }

    /* BUTTONS (RED) */
    QPushButton {
        background-color: #660000; /* Dark Red */
        color: white;
        font-weight: bold;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #990000;
    }
    QPushButton:hover { 
        background-color: #ff0000; /* Bright Red */
        border: 1px solid #ff5555;
        color: white;
    }
    QPushButton:pressed {
        background-color: #440000;
    }
    QPushButton:disabled { 
        background-color: #222; 
        color: #555; 
        border: 1px solid #333; 
    }
"""

# ========================================================
# GAME 1: GUESS THE NUMBER
# ========================================================
class GuessNumberGame(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("gameFrame")
        self.setFixedSize(350, 350)
        self.setStyleSheet(GAME_CARD_STYLE)
        
        layout = QVBoxLayout(self)
        
        title = QLabel("🔢 GUESS NUMBER")
        title.setStyleSheet("color: #ff0000; font-size: 20px; font-weight: 900;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.info = QLabel("I'm thinking of 1-100...")
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter number here...")
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input.returnPressed.connect(self.check_guess)
        layout.addWidget(self.input)

        btn = QPushButton("GUESS")
        btn.clicked.connect(self.check_guess)
        layout.addWidget(btn)

        reset = QPushButton("Reset Game")
        reset.setStyleSheet("background-color: transparent; border: 1px solid #550000; color: #888;")
        reset.clicked.connect(self.reset_game)
        layout.addWidget(reset)

        self.secret = random.randint(1, 100)

    def check_guess(self):
        try:
            val = int(self.input.text())
            if val < self.secret: 
                self.info.setText("TOO LOW! ⬆️")
                self.info.setStyleSheet("color: #ffaa00; font-weight: bold;") 
            elif val > self.secret: 
                self.info.setText("TOO HIGH! ⬇️")
                self.info.setStyleSheet("color: #ffaa00; font-weight: bold;") 
            else: 
                self.info.setText("🎉 YOU WON!")
                self.info.setStyleSheet("color: #00ff00; font-weight: bold; font-size: 18px;") 
        except: 
            self.info.setText("Please enter a number.")
        self.input.clear()

    def reset_game(self):
        self.secret = random.randint(1, 100)
        self.info.setText("New number generated (1-100)")
        self.info.setStyleSheet("color: #cccccc;")

# ========================================================
# GAME 2: MOVIE SCRAMBLE
# ========================================================
class MovieScrambleGame(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("gameFrame")
        self.setFixedSize(350, 350)
        self.setStyleSheet(GAME_CARD_STYLE)
        self.movies = ["TITANIC", "AVATAR", "JOKER", "MATRIX", "FROZEN", "ALIEN", "ROCKY", "GLADIATOR"]
        self.current = ""
        
        layout = QVBoxLayout(self)
        
        title = QLabel("🎬 MOVIE SCRAMBLE")
        title.setStyleSheet("color: #ff0000; font-size: 20px; font-weight: 900;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.scrambled = QLabel("")
        self.scrambled.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff; letter-spacing: 5px; background: #220000; border-radius: 10px; padding: 10px;")
        self.scrambled.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.scrambled)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Unscramble...")
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input.returnPressed.connect(self.check)
        layout.addWidget(self.input)

        btn_layout = QHBoxLayout()
        hint_btn = QPushButton("Hint")
        hint_btn.setStyleSheet("background-color: #330000; border: 1px solid #550000;")
        hint_btn.clicked.connect(lambda: self.status.setText(f"Hint: Starts with '{self.current[0]}'"))
        
        check_btn = QPushButton("Check")
        check_btn.clicked.connect(self.check)
        
        btn_layout.addWidget(hint_btn)
        btn_layout.addWidget(check_btn)
        layout.addLayout(btn_layout)

        self.status = QLabel("Guess the movie!")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)
        self.next_round()

    def next_round(self):
        self.current = random.choice(self.movies)
        l = list(self.current)
        random.shuffle(l)
        self.scrambled.setText("".join(l))

    def check(self):
        if self.input.text().upper().strip() == self.current:
            self.status.setText("✅ CORRECT!")
            self.status.setStyleSheet("color: #00ff00; font-weight: bold;")
            QTimer.singleShot(1000, self.next_round)
        else: 
            self.status.setText("❌ WRONG")
            self.status.setStyleSheet("color: #ff0000; font-weight: bold;")
        self.input.clear()

# ========================================================
# GAME 3: TIC TAC TOE
# ========================================================
class TicTacToeGame(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("gameFrame")
        self.setFixedSize(350, 350)
        self.setStyleSheet(GAME_CARD_STYLE)
        self.turn = 'X'
        self.buttons = []
        
        layout = QVBoxLayout(self)
        
        title = QLabel("❌ TIC TAC TOE ⭕")
        title.setStyleSheet("color: #ff0000; font-size: 20px; font-weight: 900;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(8)
        grid_w = QWidget()
        grid_w.setLayout(grid)
        
        for i in range(9):
            btn = QPushButton("")
            btn.setFixedSize(65, 65)
            btn.setStyleSheet("""
                background-color: #1a0505; 
                border: 2px solid #440000; 
                border-radius: 10px;
                font-size: 24px; font-weight: bold;
            """)
            btn.clicked.connect(partial(self.click, i))
            grid.addWidget(btn, i//3, i%3)
            self.buttons.append(btn)
        layout.addWidget(grid_w, alignment=Qt.AlignmentFlag.AlignCenter)

        self.status = QLabel("Player X Turn")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)
        
        reset = QPushButton("Restart")
        reset.setStyleSheet("background-color: transparent; border: 1px solid #550000; color: #888;")
        reset.clicked.connect(self.reset)
        layout.addWidget(reset)

    def click(self, i):
        if self.buttons[i].text() == "":
            self.buttons[i].setText(self.turn)
            
            if self.turn == 'X':
                self.buttons[i].setStyleSheet("background-color: #330000; color: #ff0000; border: 2px solid #ff0000; font-size: 28px; font-weight: bold; border-radius: 10px;")
            else:
                self.buttons[i].setStyleSheet("background-color: #222; color: #ffffff; border: 2px solid #ffffff; font-size: 28px; font-weight: bold; border-radius: 10px;")
            
            self.turn = 'O' if self.turn == 'X' else 'X'
            self.status.setText(f"Player {self.turn} Turn")

    def reset(self):
        self.turn = 'X'
        self.status.setText("Player X Turn")
        for b in self.buttons:
            b.setText("")
            b.setStyleSheet("background-color: #1a0505; border: 2px solid #440000; border-radius: 10px;")

# ========================================================
# GAME 4: QUIZ BEE
# ========================================================
class QuizBeeGame(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("gameFrame")
        self.setFixedSize(350, 350)
        self.setStyleSheet(GAME_CARD_STYLE)
        self.qs = [{"q":"Capital of France?","o":["Berlin","Paris"],"a":"Paris"},
                   {"q":"2 + 2 = ?","o":["3","4"],"a":"4"},
                   {"q":"Red Planet?","o":["Mars","Venus"],"a":"Mars"},
                   {"q":"H2O is?","o":["Water","Air"],"a":"Water"}]
        self.curr = 0
        self.score = 0
        
        layout = QVBoxLayout(self)
        
        title = QLabel("🧠 QUIZ BEE")
        title.setStyleSheet("color: #ff0000; font-size: 20px; font-weight: 900;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.lbl = QLabel()
        self.lbl.setStyleSheet("font-weight: bold; font-size: 16px; background: transparent; margin-bottom: 10px;")
        self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl)

        self.btns = []
        for i in range(2):
            b = QPushButton()
            b.setFixedHeight(45)
            b.clicked.connect(partial(self.ans, i))
            layout.addWidget(b)
            self.btns.append(b)
        
        self.score_lbl = QLabel("Score: 0")
        self.score_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_lbl.setStyleSheet("color: #888;")
        layout.addWidget(self.score_lbl)
        
        self.load()

    def load(self):
        if self.curr < len(self.qs):
            q = self.qs[self.curr]
            self.lbl.setText(q['q'])
            self.btns[0].setText(q['o'][0])
            self.btns[1].setText(q['o'][1])
        else:
            self.lbl.setText(f"DONE! Score: {self.score}/{len(self.qs)}")
            self.btns[0].hide()
            self.btns[1].hide()

    def ans(self, i):
        if self.btns[i].text() == self.qs[self.curr]['a']:
            self.score += 1
        self.score_lbl.setText(f"Score: {self.score}")
        self.curr += 1
        self.load()

# ========================================================
# GAME 5: MINI MAZE
# ========================================================
class MazeGame(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("gameFrame")
        self.setFixedSize(350, 350)
        self.setStyleSheet(GAME_CARD_STYLE)

        layout = QVBoxLayout(self)
        
        title = QLabel("🕹️ MINI MAZE")
        title.setStyleSheet("color: #ff0000; font-size: 20px; font-weight: 900;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 0=Path, 1=Wall, 2=Player, 3=Goal
        self.map = [
            [1,1,1,1,1,1,1],
            [1,2,0,0,1,0,1],
            [1,1,1,0,1,0,1],
            [1,0,0,0,0,0,1],
            [1,0,1,1,1,0,1],
            [1,0,0,0,1,3,1],
            [1,1,1,1,1,1,1]
        ]
        self.px, self.py = 1, 1
        self.labels = []

        grid_w = QWidget()
        self.grid = QGridLayout(grid_w)
        self.grid.setSpacing(1) 
        
        for r in range(7):
            row_lbls = []
            for c in range(7):
                lbl = QLabel()
                lbl.setFixedSize(30, 30)
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl.setStyleSheet("font-size: 16px;") 
                self.grid.addWidget(lbl, r, c)
                row_lbls.append(lbl)
            self.labels.append(row_lbls)
        
        layout.addWidget(grid_w, alignment=Qt.AlignmentFlag.AlignCenter)
        
        controls = QHBoxLayout()
        for txt, d in [("⬅️",(-1,0)), ("⬇️",(0,1)), ("⬆️",(0,-1)), ("➡️",(1,0))]:
            btn = QPushButton(txt)
            btn.setFixedSize(45, 35)
            btn.setStyleSheet("background-color: #220000; border: 1px solid #550000;")
            btn.clicked.connect(partial(self.move, d[0], d[1]))
            controls.addWidget(btn)
        layout.addLayout(controls)

        self.msg = QLabel("Reach the Flag 🏁")
        self.msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.msg)
        self.render()

    def move(self, dx, dy):
        nx, ny = self.px + dx, self.py + dy
        if self.map[ny][nx] != 1:
            self.px, self.py = nx, ny
            if self.map[ny][nx] == 3:
                self.msg.setText("🎉 WIN!")
                self.msg.setStyleSheet("color: #00ff00; font-weight: bold;")
                QTimer.singleShot(1500, self.reset_maze)
            self.render()

    def render(self):
        for r in range(7):
            for c in range(7):
                val = self.map[r][c]
                self.labels[r][c].setText("")
                if val == 1: # Wall
                    self.labels[r][c].setText("🧱")
                    self.labels[r][c].setStyleSheet("background-color: #1a0505; border-radius: 4px;")
                elif val == 3: # Goal
                    self.labels[r][c].setText("🏁")
                    self.labels[r][c].setStyleSheet("background-color: #330000; border-radius: 4px;")
                elif r == self.py and c == self.px: # Player
                    self.labels[r][c].setText("🏃")
                    self.labels[r][c].setStyleSheet("background-color: #330000; border-radius: 4px;")
                else: # Path
                    self.labels[r][c].setStyleSheet("background-color: #2a1a1a; border-radius: 4px;")

    def reset_maze(self):
        self.px, self.py = 1, 1
        self.msg.setText("Reach the Flag 🏁")
        self.msg.setStyleSheet("color: white;")
        self.render()

# ========================================================
# GAME 6: ROCK PAPER SCISSORS
# ========================================================
class RockPaperScissorsGame(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("gameFrame")
        self.setFixedSize(350, 350)
        self.setStyleSheet(GAME_CARD_STYLE)
        self.p_score = 0
        self.b_score = 0
        
        layout = QVBoxLayout(self)
        
        title = QLabel("🪨 RPS BATTLE ✂️")
        title.setStyleSheet("color: #ff0000; font-size: 18px; font-weight: 900;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.score_lbl = QLabel("You: 0  |  Bot: 0")
        self.score_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #888; margin-bottom: 10px;")
        self.score_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.score_lbl)
        
        self.result = QLabel("Select Weapon")
        self.result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.result.setFixedHeight(50)
        layout.addWidget(self.result)
        
        btn_layout = QHBoxLayout()
        for opt, icon in [("Rock", "🪨"), ("Paper", "📄"), ("Scissors", "✂️")]:
            btn = QPushButton(f"{icon}\n{opt}")
            btn.setFixedSize(85, 65)
            btn.setStyleSheet("""
                QPushButton { background-color: #220000; border: 1px solid #550000; color: white; }
                QPushButton:hover { background-color: #ff0000; border: 1px solid white; }
            """)
            btn.clicked.connect(partial(self.play, opt))
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        reset = QPushButton("Reset Score")
        reset.setStyleSheet("background-color: transparent; border: 1px solid #550000; color: #888;")
        reset.clicked.connect(self.reset)
        layout.addWidget(reset)

    def play(self, user):
        opts = ["Rock", "Paper", "Scissors"]
        bot = random.choice(opts)
        
        if user == bot: txt = "IT'S A TIE!"
        elif (user=="Rock" and bot=="Scissors") or (user=="Paper" and bot=="Rock") or (user=="Scissors" and bot=="Paper"):
            txt = "YOU WIN!"
            self.p_score += 1
        else:
            txt = "BOT WINS!"
            self.b_score += 1
            
        self.result.setText(f"You: {user} vs Bot: {bot}\n{txt}")
        self.score_lbl.setText(f"You: {self.p_score}  |  Bot: {self.b_score}")

    def reset(self):
        self.p_score = 0
        self.b_score = 0
        self.score_lbl.setText("You: 0  |  Bot: 0")
        self.result.setText("Select Weapon")

# ========================================================
# MAIN GAMES PAGE CONTAINER
# ========================================================
class GamesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("gamesPage")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Header
        header = QLabel("ARCADE ZONE 🕹️")
        header.setStyleSheet("font-size: 36px; font-weight: 900; color: #ff0000; letter-spacing: 2px; margin-bottom: 10px; text-transform: uppercase;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        # --- SEARCH BAR ---
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search games...")
        self.search_input.setFixedSize(600, 50)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                border: 2px solid #550000;
                border-radius: 25px;
                padding-left: 20px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #ff0000;
                background-color: black;
            }
        """)
        self.search_input.textChanged.connect(self.filter_games)
        main_layout.addWidget(self.search_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(content)
        self.grid.setSpacing(30)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Store games with their names to easily filter them later
        self.game_widgets = []

        # Helper to add game
        def add_game(name, widget, r, c):
            self.grid.addWidget(widget, r, c)
            self.game_widgets.append((name, widget))

        # Add ALL 6 Games with names
        add_game("Guess Number", GuessNumberGame(), 0, 0)
        add_game("Movie Scramble", MovieScrambleGame(), 0, 1)
        add_game("Tic Tac Toe", TicTacToeGame(), 1, 0)
        add_game("Quiz Bee", QuizBeeGame(), 1, 1)
        add_game("Mini Maze", MazeGame(), 2, 0)
        add_game("Rock Paper Scissors", RockPaperScissorsGame(), 2, 1)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def filter_games(self):
        query = self.search_input.text().lower()
        for name, widget in self.game_widgets:
            if query in name.lower():
                widget.show()
            else:
                widget.hide()