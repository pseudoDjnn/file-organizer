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
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Status for updates

        self.status_label = QLabel("Select a directory to organize.")
        layout.addWidget(self.status_label)
        
        # Browse button for selecting a directory
        
        browse_button = QPushButton("Browse Directory")
        browse_button.clicked.connect(self.browse_directory)
        layout.addWidget(browse_button)
        
        # Run organizer button
        
        run_button = QPushButton("Run Organizer")
        run_button.clicked.connect(self.run_organizer)
        layout.addWidget(run_button)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.apply_styles()
        
    def browse_directory(self):
        pass
    
    def run_organizer(self):
        pass

    def apply_styles(self):
        pass