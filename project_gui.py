import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QWidget, QFileDialog
)

from file_organizer import organize_files
import logging

logger = logging.getLogger(__name__)

class GuiForProject(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setMinimumSize(800, 600)
        self.selected_directory = None
        self.initUI()
        
    
    def initUI(self):
        pass