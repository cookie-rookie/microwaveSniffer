import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPainterPath
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from datetime import datetime
from utils.checker import CheckerInit
from utils.themes import light_theme, dark_theme
from utils.styles import button_style, statusbar_style
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class DynamicGraphGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.x = np.linspace(0, 10, 800)
        self.ys = [np.sin(self.x *random.random()) for _ in range(7)]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(10)
        self.aspect_ratio = 1
    
    def initializeGL(self):
        glColorMask(True,True,True,True)
        glClearColor(0.15,0.15,0.15,0)
        glClear(GL_COLOR_BUFFER_BIT)
        
    
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
       
        self.aspect_ratio = w / h
        glOrtho(-10 * self.aspect_ratio, 10 * self.aspect_ratio, -1, 1, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth(2)

        
        for y in self.ys:
            glBegin(GL_LINE_STRIP)
            color = [random.random() for _ in range(3)]
            glColor3f(color[0], color[1], color[2])
            for i, value in enumerate(y):
                
                x_coord = (self.x[i] / 5-.5) * 20 * self.aspect_ratio
                y_coord = value
                glVertex2f(x_coord, y_coord)
            glEnd()

    def animate(self):
      
        self.ys = [np.roll(y, -1) for y in self.ys]
        self.update()  


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("microwaveSniffer")
        self.setGeometry(100, 100, 800, 600)
        self.current_theme = dark_theme
        self.initUI() 
        self.initStatusBar()  
        self.apply_theme(self.current_theme)  
        self.checker_init = CheckerInit()
        self.checker_init.internet_finished.connect(self.handle_internet_check_result)
        self.checker_init.hardware_finished.connect(self.handle_hardware_check_result)
        self.checker_init.start()
        
    def closeEvent(self, event):
        self.checker_init.stop() 
        self.checker_init.wait() 
        super().closeEvent(event)

    def initStatusBar(self):
        self.statusbar = self.statusBar()
        self.internetlabel = QLabel("Internet: Checking...")
        self.hardwarelabel = QLabel("Hardware: Checking...")
        self.statusbar.addPermanentWidget(self.internetlabel)
        self.statusbar.addPermanentWidget(self.hardwarelabel)
        self.last_update_label = QLabel("Last Update: Never")
        self.statusbar.addPermanentWidget(self.last_update_label)

    def handle_hardware_check_result(self, connected):
        self.hardwarelabel.setText("Hardware: Connected" if connected else "Hardware: Disconnected")
        self.hardwarelabel.setStyleSheet("color: lightgreen;" if connected else "color: red;")

    def handle_internet_check_result(self, connected):
        self.internetlabel.setText("Internet: Connected" if connected else "Internet: Disconnected")
        self.internetlabel.setStyleSheet("color: lightgreen;" if connected else "color: red;")
        self.last_update_label.setText(f"Last Update: {datetime.now().strftime('%H:%M')}")

    def initUI(self):
        
        self.graphWidget = DynamicGraphGLWidget(self)
        self.setCentralWidget(self.graphWidget)
        self.layout = QGridLayout(self.graphWidget)
        self.signalListBtn = QPushButton("Signal List")
        self.signalListBtn.clicked.connect(self.showSignalList)
        self.layout.addWidget(self.signalListBtn, 0, 0)
        self.realTimeBtn = QPushButton("Real-Time Monitoring")
        self.realTimeBtn.clicked.connect(self.showRealTimeMonitoring)
        self.layout.addWidget(self.realTimeBtn, 0, 1)
        self.hardwareEditorBtn = QPushButton("Hardware Editor")
        self.hardwareEditorBtn.clicked.connect(self.showHardwareEditor)
        self.layout.addWidget(self.hardwareEditorBtn, 1, 0)
        self.settingsBtn = QPushButton("Settings")
        self.settingsBtn.clicked.connect(self.showSettings)
        self.layout.addWidget(self.settingsBtn, 1, 1)

      
        self.styleUI()


    def showSignalList(self):
        print("Signal List Button Clicked")
      
        # signalListWindow = SignalListWindow()
        # signalListWindow.show()

    def showRealTimeMonitoring(self):
        print("Real-Time Monitoring Button Clicked")
   
        # realTimeMonitoringWindow = RealTimeMonitoringWindow()
        # realTimeMonitoringWindow.show()

    def showHardwareEditor(self):
        print("Hardware Editor Button Clicked")

        # codeEditorWindow = CodeEditorWindow()
        # codeEditorWindow.show()

    def showSettings(self):
        print("Settings Button Clicked")

        # settingsWindow = SettingsWindow()
        # settingsWindow.show()


    # APPLICATION OF THEME AND STYLES
    def styleUI(self):
     
        self.signalListBtn.setStyleSheet(button_style)
        self.realTimeBtn.setStyleSheet(button_style)
        self.hardwareEditorBtn.setStyleSheet(button_style)
        self.settingsBtn.setStyleSheet(button_style)
        #self.statusbar.setStyleSheet(statusbar_style)
            
    def apply_theme(self, theme):
       
        self.setStyleSheet(theme["main_background"])
        self.signalListBtn.setStyleSheet(theme["button_style"])
        self.realTimeBtn.setStyleSheet(theme["button_style"])
        self.hardwareEditorBtn.setStyleSheet(theme["button_style"])
        self.settingsBtn.setStyleSheet(theme["button_style"])
        self.internetlabel.setStyleSheet(theme["label_style"])
        self.hardwarelabel.setStyleSheet(theme["label_style"])
        self.last_update_label.setStyleSheet(theme["label_style"])
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

