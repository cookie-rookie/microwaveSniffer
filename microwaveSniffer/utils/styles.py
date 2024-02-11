# Define button styles
button_style = """
QPushButton {
    font: bold 14px;
    border: 2px solid #8f8f91;
    border-radius: 6px;
    min-width: 80px;
    max-width: 150px;
    min-height: 40px;
    max-height: 40px;
    padding: 6px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f6f7fa, stop:1 #dadbde);
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #dadbde, stop:1 #f6f7fa);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #dadbde, stop:1 #f6f7fa);
    padding-top: -15px;
    padding-bottom: -17px;
}
"""

# Define status bar styles
statusbar_style = """
QStatusBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f6f7fa, stop:1 #dadbde);
    color: black;
}
"""


