import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

# импортируем logger раньше других app-модулей, чтобы избежать двойной инициализации логгера
from app.logger.logger import logger

from app.UI.main_window import MainWindow


async def main(app: QApplication):
    window = MainWindow()
    window.show()

    logger.write("Application started")

    # Асинхронно ждём закрытия Qt-приложения
    app_closed = asyncio.Event()
    app.aboutToQuit.connect(app_closed.set)
    await app_closed.wait()

    try:
        logger.flush()
    except Exception:
        # на shutdown не хотим ломать приложение из-за проблем с логом
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    asyncio.run(main(app), loop_factory=QEventLoop)
