import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
from app.UI.main_window import MainWindow


async def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    # Асинхронно запускаем Qt event loop
    with loop:
        await loop.run_forever()


if __name__ == "__main__":
    asyncio.run(main())