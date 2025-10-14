import sys
from PyQt6.QtWidgets import QApplication
import main_window

def ShowMainWindow():
    app = QApplication(sys.argv)
    window = main_window.MainWindow()
    window.show()
    sys.exit(app.exec())

ShowMainWindow()