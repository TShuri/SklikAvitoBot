"""
Кастомные виджеты
"""
from PyQt6.QtWidgets import (QTextEdit, QVBoxLayout, QWidget, QGroupBox, QLabel, 
                            QLineEdit, QHBoxLayout, QComboBox, QSpinBox, 
                            QDoubleSpinBox, QCheckBox, QPushButton, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor, QPalette, QColor
import logging


class LogHandler(logging.Handler):
    """Кастомный обработчик логов для LogTextEdit"""
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        ))
    
    def emit(self, record):
        msg = self.format(record)
        
        # Определяем цвет в зависимости от уровня
        if record.levelno >= logging.ERROR:
            color = "#FF4444"  # Красный для ошибок
        elif record.levelno >= logging.WARNING:
            color = "#FFAA00"  # Оранжевый для предупреждений
        elif record.levelno >= logging.INFO:
            color = "#44FF44"  # Зеленый для информации
        else:
            color = "#888888"  # Серый для отладки
            
        self.text_widget.append_log(msg, color)


class LogTextEdit(QTextEdit):
    """Кастомный TextEdit для логов"""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 9))
        
        # Темная тема для логов
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 240))
        self.setPalette(palette)
        
    def append_log(self, message, color="#FFFFFF"):
        """Добавляет сообщение с цветом"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Форматируем сообщение
        html = f'<span style="color: {color};">{message}</span><br>'
        self.append(html)
        
        # Автопрокрутка
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)
        
        # Ограничение размера логов (последние 1000 строк)
        if self.document().lineCount() > 1000:
            cursor.setPosition(0)
            cursor.movePosition(QTextCursor.MoveOperation.Down, 
                              QTextCursor.MoveMode.KeepAnchor, 100)
            cursor.removeSelectedText()


class ProxySettingsGroup(QGroupBox):
    """Группа настроек прокси"""
    
    def __init__(self):
        super().__init__("Настройки прокси")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Чекбокс использования прокси
        self.proxy_check = QCheckBox("Использовать прокси (ротация IP)")
        self.proxy_check.setChecked(True)
        self.proxy_check.toggled.connect(self.toggle_proxy_fields)
        layout.addWidget(self.proxy_check)
        
        # Поля для прокси (изначально видимые)
        self.proxy_server_layout = QHBoxLayout()
        self.proxy_server_layout.addWidget(QLabel("Прокси сервер:"))
        self.proxy_server_input = QLineEdit()
        self.proxy_server_input.setPlaceholderText("http://proxy.example.com:8080")
        self.proxy_server_layout.addWidget(self.proxy_server_input)
        layout.addLayout(self.proxy_server_layout)
        
        self.proxy_auth_layout = QHBoxLayout()
        self.proxy_auth_layout.addWidget(QLabel("Логин:"))
        self.proxy_username_input = QLineEdit()
        self.proxy_username_input.setPlaceholderText("username")
        self.proxy_auth_layout.addWidget(self.proxy_username_input)
        
        self.proxy_auth_layout.addWidget(QLabel("Пароль:"))
        self.proxy_password_input = QLineEdit()
        self.proxy_password_input.setPlaceholderText("password")
        self.proxy_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.proxy_auth_layout.addWidget(self.proxy_password_input)
        layout.addLayout(self.proxy_auth_layout)
        
        # Кнопка тестирования прокси
        self.test_proxy_btn = QPushButton("🔍 Тестировать прокси")
        self.test_proxy_btn.clicked.connect(self.test_proxy)
        layout.addWidget(self.test_proxy_btn)
        
    def toggle_proxy_fields(self, enabled):
        """Включает/выключает поля прокси"""
        self.proxy_server_input.setEnabled(enabled)
        self.proxy_username_input.setEnabled(enabled)
        self.proxy_password_input.setEnabled(enabled)
        self.test_proxy_btn.setEnabled(enabled)
        
    def test_proxy(self):
        """Тестирование прокси соединения"""
        # Здесь можно добавить логику тестирования прокси
        print("Тестирование прокси...")
        
    def get_proxy_settings(self):
        """Возвращает настройки прокси"""
        if not self.proxy_check.isChecked():
            return None
            
        return {
            'server': self.proxy_server_input.text().strip(),
            'username': self.proxy_username_input.text().strip(),
            'password': self.proxy_password_input.text().strip()
        }
        
    def set_proxy_settings(self, server, username="", password=""):
        """Устанавливает настройки прокси"""
        self.proxy_server_input.setText(server)
        self.proxy_username_input.setText(username)
        self.proxy_password_input.setText(password)


class ControlPanel(QGroupBox):
    """Панель управления"""
    
    start_signal = pyqtSignal(dict)  # settings dict
    stop_signal = pyqtSignal()
    test_proxy_signal = pyqtSignal(dict)  # proxy settings for testing
    
    def __init__(self):
        super().__init__("Настройки парсера")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Режим работы
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Режим работы:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Одиночный запуск", "Непрерывный режим"])
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)
        
        # Количество сессий
        sessions_layout = QHBoxLayout()
        sessions_layout.addWidget(QLabel("Количество сессий:"))
        self.sessions_spin = QSpinBox()
        self.sessions_spin.setRange(1, 1000)
        self.sessions_spin.setValue(10)
        self.sessions_spin.setSuffix(" (0 = бесконечно)")
        sessions_layout.addWidget(self.sessions_spin)
        sessions_layout.addStretch()
        layout.addLayout(sessions_layout)
        
        # Задержки
        delays_layout = QHBoxLayout()
        delays_layout.addWidget(QLabel("Задержка между сессиями:"))
        self.delay_min_spin = QDoubleSpinBox()
        self.delay_min_spin.setRange(1, 60)
        self.delay_min_spin.setValue(2)
        self.delay_min_spin.setSuffix(" мин")
        delays_layout.addWidget(self.delay_min_spin)
        
        delays_layout.addWidget(QLabel("до"))
        self.delay_max_spin = QDoubleSpinBox()
        self.delay_max_spin.setRange(1, 120)
        self.delay_max_spin.setValue(10)
        self.delay_max_spin.setSuffix(" мин")
        delays_layout.addWidget(self.delay_max_spin)
        delays_layout.addStretch()
        layout.addLayout(delays_layout)
        
        # Настройки прокси
        self.proxy_group = ProxySettingsGroup()
        layout.addWidget(self.proxy_group)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🚀 Запуск")
        self.start_btn.clicked.connect(self.start_clicked)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Остановить")
        self.stop_btn.clicked.connect(self.stop_signal.emit)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(button_layout)
        
    def start_clicked(self):
        """Обработчик нажатия кнопки запуска"""
        settings = {
            'mode': 'continuous' if self.mode_combo.currentText() == "Непрерывный режим" else 'single',
            'sessions': self.sessions_spin.value(),
            'delay_min': self.delay_min_spin.value(),
            'delay_max': self.delay_max_spin.value(),
            'proxy': self.proxy_group.get_proxy_settings()
        }
        self.start_signal.emit(settings)
        
    def set_running_state(self, running):
        """Устанавливает состояние кнопок"""
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)
        self.mode_combo.setEnabled(not running)
        self.sessions_spin.setEnabled(not running)
        self.delay_min_spin.setEnabled(not running)
        self.delay_max_spin.setEnabled(not running)
        self.proxy_group.setEnabled(not running)
        
    def load_proxy_from_env(self):
        """Загружает настройки прокси из переменных окружения"""
        import os
        proxy_server = os.getenv('PROXY_SERVER', '')
        proxy_username = os.getenv('PROXY_USERNAME', '')
        proxy_password = os.getenv('PROXY_PASSWORD', '')
        
        if proxy_server:
            self.proxy_group.set_proxy_settings(proxy_server, proxy_username, proxy_password)


class StatusBar(QWidget):
    """Строка статуса"""
    
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        
        self.status_label = QLabel("Готов к работе")
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
    def set_status(self, text, is_working=False):
        """Устанавливает статус"""
        self.status_label.setText(text)
        self.progress_bar.setVisible(is_working)
        
    def set_progress(self, value):
        """Устанавливает прогресс"""
        self.progress_bar.setValue(value)