"""
Рабочие потоки для GUI
"""
import asyncio
import sys
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal

# Добавляем корневую директорию проекта в путь поиска модулей
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# from main import main_single, main_continuous


class ParserWorker(QThread):
    """Поток для выполнения парсинга"""
    
    log_signal = pyqtSignal(str, str)  # message, color
    finished_signal = pyqtSignal(bool)  # success
    progress_signal = pyqtSignal(int)   # progress
    
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._is_running = True
        
    def run(self):
        """Запуск асинхронной задачи"""
        try:
            asyncio.run(self._run_async())
        except Exception as e:
            self.log_signal.emit(f"Ошибка потока: {e}", "#FF4444")
            self.finished_signal.emit(False)
            
    async def _run_async(self):
        """Асинхронная задача"""
        pass
        # try:
        #     # Здесь можно передавать настройки в парсер
        #     if self.settings['mode'] == 'single':
        #         success = await main_single()
        #     else:
        #         success = await main_continuous()
                
        #     self.finished_signal.emit(success)
            
        # except Exception as e:
        #     self.log_signal.emit(f"Ошибка выполнения: {e}", "#FF4444")
        #     self.finished_signal.emit(False)
            
    def stop(self):
        """Остановка потока"""
        self._is_running = False
        self.terminate()