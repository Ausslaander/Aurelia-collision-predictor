from config.config import LOGS_PATH
import inspect
from datetime import datetime
import threading
from typing import Optional


class Logger:
    """Очень простой логгер: один метод `write`, выполняющий синхронную запись.

    Это убирает асинхронные сложности и исключения, связанные с планированием тасков в event loop.
    """

    def __init__(self):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.filename = f"log_{timestamp}.txt"
        self.log_file = LOGS_PATH / self.filename
        LOGS_PATH.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.touch()
        self._lock = threading.Lock()

    def _detect_source(self) -> str:
        for frame_info in inspect.stack()[2:]:
            frame = frame_info.frame
            module = inspect.getmodule(frame)
            module_name = module.__name__ if module and module.__name__ != '__main__' else None
            # пропустить кадры из этого модуля
            if module_name and module_name.startswith('app.logger'):
                continue

            func_name = frame_info.function
            cls = frame.f_locals.get('self') or frame.f_locals.get('cls')
            if cls:
                class_name = cls.__class__.__name__ if not isinstance(cls, type) else cls.__name__
                src = f"{module.__name__}.{class_name}.{func_name}" if module else f"{class_name}.{func_name}"
            else:
                src = f"{module.__name__}.{func_name}" if module else f"{frame_info.filename}:{func_name}"
            return src
        return "unknown"

    def _format_line(self, data: str, source: Optional[str]) -> str:
        if source is None:
            try:
                source = self._detect_source()
            except Exception:
                source = 'unknown'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"[{timestamp}] {source}: {data}"

    def _sync_write_to_file(self, line: str):
        with self._lock:
            with self.log_file.open('a', encoding='utf-8') as f:
                f.write(line + '\n')

    def write(self, data: str, to_terminal: bool = False, source: Optional[str] = None):
        """Единый метод записи: всегда выполняет синхронную запись и возвращает None."""
        line = self._format_line(data, source)
        if to_terminal:
            print(line)
        self._sync_write_to_file(line)
        return None

    def flush(self):
        """Нейтральный flush для совместимости — ничего не делает (запись синхронна)."""
        return None


# модульный (дефолтный) экземпляр для простого импорта
logger = Logger()
