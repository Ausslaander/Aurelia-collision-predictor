import asyncio
import logging
from abc import ABC, abstractmethod


class BaseHandler(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def handle(self, *args, **kwargs):
        # Абстракция, реализуется в конкретном методе
        pass