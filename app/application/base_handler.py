import asyncio
from abc import ABC, abstractmethod

from app.logger.logger import logger


class BaseHandler(ABC):
    def __init__(self):
        # Используем модульный экземпляр logger, чтобы не создавать несколько файлов/инстансов
        self.logger = logger
        self.view = None  # Placeholder для view, которая будет указана в дочернем классе

    @abstractmethod
    async def handle(self, *args, **kwargs):
        # Абстракция, реализуется в конкретном методе
        pass