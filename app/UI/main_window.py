from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget, QLabel, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from app.application.import_handler import ImportHandler
from qasync import asyncSlot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aurelia Collision Predictor")
        self.setFixedSize(800, 500)

        # главный контейнер
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # панель слева
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)

        self.import_button = QPushButton("Import")
        self.calc_button = QPushButton("Calculation")

        self.import_button.setFixedSize(180, 40)
        self.calc_button.setFixedSize(180, 40)

        left_layout.addWidget(self.import_button)
        left_layout.addWidget(self.calc_button)
        left_layout.addStretch() # эта хня нужна для того, чтобы кнопки были сверху панели

        # правая панель
        tabs = QTabWidget()
        tabs.addTab(self.create_tab_placeholder("General"), "General")
        tabs.addTab(self.create_tab_placeholder("Data"), "Data")
        tabs.addTab(self.create_tab_placeholder("Settings"), "Settings")
        tabs.addTab(self.create_tab_placeholder("Terminal"), "Terminal")
        tabs.addTab(self.create_visual_tab(), "Visual")

        # сборка в layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(tabs, 4)

        #TODO: подключить обработчики событий
        self.import_button.clicked.connect(self.on_import_clicked)

    # TODO: эти отдельные вкладки надо будет реализовать в виде отдельных модулей с подключением в этот, основной
    # TODO: пока плейсхолдер 3D окна визуализации
    def create_visual_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        globe_placeholder = QFrame()
        globe_placeholder.setStyleSheet("background-color: #1E1E2E; border-radius: 8px;")
        globe_placeholder.setFixedSize(400, 400)
        globe_label = QLabel("3D Earth Placeholder", alignment=Qt.AlignmentFlag.AlignCenter)
        globe_label.setStyleSheet("color: white; font-size: 16px;")

        frame_layout = QVBoxLayout(globe_placeholder)
        frame_layout.addWidget(globe_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(globe_placeholder, alignment=Qt.AlignmentFlag.AlignCenter)
        return tab

    # TODO: пока просто плейсхолдер для остальных вкладок
    def create_tab_placeholder(self, name):
        tab = QWidget()
        label = QLabel(f"{name} content coming soon...", alignment=Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(tab)
        layout.addWidget(label)
        return tab

    @asyncSlot()
    async def on_import_clicked(self):
        handler = ImportHandler()
        result = await handler.handle()
        QMessageBox.information(self, "Import", result["message"])