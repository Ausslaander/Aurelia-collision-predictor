from app.application.base_handler import BaseHandler
import asyncio

class ImportHandler(BaseHandler):
    async def handle(self):
        print("Importing data...")
        await asyncio.sleep(2)
        print("Import finished successfully!")
        return {"status": "ok", "message": "Mock import completed"}
