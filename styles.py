BG_LOGIN    = "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?q=80&w=1920&auto=format&fit=crop" 
BG_HOME     = "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1920&auto=format&fit=crop" 
BG_MOVIES   = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=1920&auto=format&fit=crop" 
BG_MUSIC    = "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1920&auto=format&fit=crop" 
BG_GAMES    = "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=1920&auto=format&fit=crop" 
BG_SETTINGS = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1920&auto=format&fit=crop" 

QSS_THEME = f"""
/* --- GLOBAL --- */
QMainWindow {{ background-color: #050505; }}
QWidget {{ font-family: 'Segoe UI', sans-serif; }}

/* --- PAGE BACKGROUNDS --- */
QWidget#loginPage {{ border-image: url("{BG_LOGIN}") 0 0 0 0 stretch stretch; }}
QWidget#homePage {{ border-image: url("{BG_HOME}") 0 0 0 0 stretch stretch; }}
QWidget#moviesPage {{ border-image: url("{BG_MOVIES}") 0 0 0 0 stretch stretch; }}
QWidget#musicPage {{ border-image: url("{BG_MUSIC}") 0 0 0 0 stretch stretch; }}
QWidget#gamesPage {{ border-image: url("{BG_GAMES}") 0 0 0 0 stretch stretch; }}
QWidget#settingsPage {{ border-image: url("{BG_SETTINGS}") 0 0 0 0 stretch stretch; }}

/* --- SIDEBAR --- */
QWidget#sidebar {{
    background-color: rgba(10, 0, 0, 0.95); 
    border-right: 2px solid #550000;
}}

QPushButton#toggleButton {{
    background-color: transparent;
    color: #ff0000;
    font-weight: 900;
    font-size: 16px;
    border: none;
    text-align: left;
    padding-left: 10px;
}}
QPushButton#toggleButton:hover {{ color: white; }}

QPushButton#sidebarButton {{
    background-color: rgba(255, 255, 255, 0.05);
    color: #cccccc;
    text-align: left;
    padding: 12px 20px;
    border: 1px solid transparent;
    border-radius: 8px;
    font-weight: 600;
}}

QPushButton#sidebarButton:hover {{
    background-color: rgba(200, 0, 0, 0.4);
    border: 1px solid #ff0000;
    color: white;
}}

QPushButton#sidebarButton[active="true"] {{
    background-color: #b30000; 
    border: 1px solid #ff0000;
    color: white;
    font-weight: bold;
}}

QPushButton#logoutButton {{
    background-color: transparent;
    color: #888;
    border: 1px solid #333;
    border-radius: 5px;
    padding: 8px;
}}
QPushButton#logoutButton:hover {{
    background-color: #330000;
    color: red;
    border-color: red;
}}

/* --- SCROLL BARS --- */
QScrollArea {{ background: transparent; border: none; }}
QScrollBar:vertical {{ background: #111; width: 10px; margin: 0px; }}
QScrollBar::handle:vertical {{ background: #550000; min-height: 20px; border-radius: 5px; }}
QScrollBar::handle:vertical:hover {{ background: #ff0000; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}

/* --- MESSAGE BOX --- */
QMessageBox {{ background-color: #1a0505; border: 2px solid #ff0000; }}
QMessageBox QLabel {{ color: white; }}
QMessageBox QPushButton {{
    background-color: #b30000; color: white;
    border: 1px solid #ff0000; border-radius: 4px; padding: 5px 15px;
}}
"""