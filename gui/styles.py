"""
Стили для GUI
"""
STYLES = {
    "dark_theme": """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #555555;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #88ccff;
        }
        QPushButton {
            background-color: #444444;
            color: white;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 5px 10px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #555555;
        }
        QPushButton:pressed {
            background-color: #666666;
        }
        QPushButton:disabled {
            background-color: #333333;
            color: #666666;
        }
        QTextEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 3px;
            font-family: Consolas, Monaco, monospace;
        }
        QComboBox, QSpinBox, QDoubleSpinBox {
            background-color: #444444;
            color: white;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 2px 5px;
        }
        QProgressBar {
            border: 1px solid #555555;
            border-radius: 3px;
            text-align: center;
            color: white;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            border-radius: 2px;
        }
        QLabel {
            color: #ffffff;
        }
    """,
    
    "button_success": "QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }",
    "button_danger": "QPushButton { background-color: #f44336; color: white; }",
    "button_warning": "QPushButton { background-color: #ff9800; color: white; }"
}