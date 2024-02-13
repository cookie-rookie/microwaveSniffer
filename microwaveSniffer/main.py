# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.updater import run_updater

def main():
    
    run_updater('cookie-rookie', 'microwaveSniffer', '1.0.0', 'your_token_here')
    
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()  
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
