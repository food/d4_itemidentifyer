from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

class Overlay(QWidget):
    """
    Overlay widget for displaying squares.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.showFullScreen()
        self.initOverlay()
        self.squares = []

    def initOverlay(self):
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for square in self.squares:
            print(square)
            painter.fillRect(square.x, square.y, square.width, square.height, square.color)

    def foo(self, square):
        print(square)
        self.squares.append(square)
        self.update()