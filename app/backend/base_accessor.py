from app.logger.logger import logger


class BaseAccessor:
    def __init__(self):
        self.logger = logger

    async def connect(self):
        raise NotImplementedError

    async def disconnect(self):
        raise NotImplementedError
