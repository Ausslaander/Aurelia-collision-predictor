from app.logger.logger import logger

class BaseAccessor:
    def __init__(self):
        self.logger = logger

    async def connect(self, app):
        pass

    async def disconnect(self, app):
        pass