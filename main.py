import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

# импортируем logger раньше других app-модулей, чтобы избежать двойной инициализации логгера
from app.logger.logger import logger

from app.UI.main_window import MainWindow


async def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    logger.write("Application started")

    # Асинхронно запускаем Qt event loop
    with loop:
        try:
            loop.run_forever()
        finally:
            # дождёмся завершения всех запланированных асинхронных записей в лог
            try:
                logger.flush()
            except Exception:
                # на shutdown не хотим ломать приложение из-за проблем с логом
                pass


if __name__ == "__main__":
    asyncio.run(main())