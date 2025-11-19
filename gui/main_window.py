"""
Главное окно приложения
"""
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QSplitter, QFrame, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .widgets import ControlPanel, LogTextEdit, LogHandler, StatusBar
from .workers import ParserWorker
from .styles import STYLES
import logging


class AvitoParserGUI(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.setup_ui()
        self.setup_logging()
        self.apply_styles()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.setWindowTitle("Avito Parser - Накрутка просмотров")
        self.setGeometry(100, 100, 1000, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Заголовок
        title_label = QLabel("🚀 Avito Parser - Накрутка просмотров")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #88ccff; margin: 10px;")
        layout.addWidget(title_label)
        
        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #555555;")
        layout.addWidget(separator)
        
        # Splitter для разделения панели управления и логов
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)
        
        # Верхняя панель - управление
        control_panel = self.create_control_panel()
        splitter.addWidget(control_panel)
        
        # Нижняя панель - логи
        log_panel = self.create_log_panel()
        splitter.addWidget(log_panel)
        
        # Устанавливаем пропорции
        splitter.setSizes([200, 500])
        
        # Строка статуса
        self.status_bar = StatusBar()
        layout.addWidget(self.status_bar)
        
    def create_control_panel(self):
        """Создает панель управления"""
        self.control_panel = ControlPanel()
        self.control_panel.start_signal.connect(self.start_parsing)
        self.control_panel.stop_signal.connect(self.stop_parsing)
        return self.control_panel
        
    def create_log_panel(self):
        """Создает панель логов"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        log_label = QLabel("Логи выполнения:")
        log_label.setStyleSheet("font-weight: bold; color: #88ccff;")
        layout.addWidget(log_label)
        
        self.log_text = LogTextEdit()
        layout.addWidget(self.log_text)
        
        return panel
        
    def setup_logging(self):
        """Настройка системы логирования"""
        log_handler = LogHandler(self.log_text)
        log_handler.setLevel(logging.INFO)
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(log_handler)
        
    def apply_styles(self):
        """Применяет стили к приложению"""
        self.setStyleSheet(STYLES["dark_theme"])
        self.control_panel.start_btn.setStyleSheet(STYLES["button_success"])
        self.control_panel.stop_btn.setStyleSheet(STYLES["button_danger"])
        
    def start_parsing(self, settings):
        """Запуск парсинга"""
        try:
            self.worker = ParserWorker(settings)
            self.worker.log_signal.connect(self.add_log)
            self.worker.finished_signal.connect(self.parsing_finished)
            self.worker.progress_signal.connect(self.status_bar.set_progress)
            self.worker.start()
            
            proxy_settings = settings.get('proxy')
            if proxy_settings and proxy_settings['server']:
                self.add_log(f"Используется прокси: {proxy_settings['server']}")
            else:
                self.add_log("Прокси не используется")

            self.control_panel.set_running_state(True)
            self.status_bar.set_status("Выполняется...", True)
            self.add_log("🚀 Парсинг запущен", "#4CAF50")
            
        except Exception as e:
            self.add_log(f"❌ Ошибка запуска: {e}", "#FF4444")
            self.parsing_finished(False)
            
    def stop_parsing(self):
        """Остановка парсинга"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
            
        self.parsing_finished(False)
        self.add_log("⏹️ Парсинг остановлен пользователем", "#FFAA00")
        
    def parsing_finished(self, success):
        """Завершение парсинга"""
        self.control_panel.set_running_state(False)
        
        if success:
            self.status_bar.set_status("✅ Завершено успешно", False)
            self.add_log("✅ Работа завершена успешно", "#4CAF50")
        else:
            self.status_bar.set_status("❌ Завершено с ошибками", False)
            
    def add_log(self, message, color="#FFFFFF"):
        """Добавляет сообщение в лог"""
        self.log_text.append_log(message, color)
        
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()