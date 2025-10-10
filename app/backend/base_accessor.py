from app.logger.logger import Logger

class BaseAccessor:
    def __init__(self):
        self.logger = Logger()

    async def connect(self, app):
        pass

    async def disconnect(self, app):
        pass