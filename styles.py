qss = f"""
    QLineEdit{{
        background-color: #F0F8FF;
        border: 2px solid #000;
        border-radius: 5px;
    }}
    QWidget {{
        background-color: #F0F8FF;
    }}
    QPushButton[cssClass="normalButton"] {{
        color: #fff;
        background: {'#4F4F4F'};
        border-radius: 5px;
    }}
    QPushButton[cssClass="normalButton"]:hover {{
        color: #fff;
        background: {'#696969'};
    }}
    QPushButton[cssClass="normalButton"]:pressed {{
        color: #fff;
        background: {'#A9A9A9'};
    }}
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {'#1C1C1C'};
        border-radius: 5px;
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {'#363636'};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {'#808080'};
    }}
"""

def setupTheme(app):
    app.setStyleSheet(app.styleSheet() + qss)
