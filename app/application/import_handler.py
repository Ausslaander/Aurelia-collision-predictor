from app.application.base_handler import BaseHandler

from app.backend.views import SatelliteDataView


class ImportHandler(BaseHandler):
    def __init__(self):  # Инициализация обработчика импорта, указание нужной view
        super().__init__()
        self.view = SatelliteDataView()

    async def handle(self):
        self.logger.write("Starting import process")
        result = await self.view.get_data(group="starlink")  # TODO пока по дефолту импортируется starlink, надо будет потом добавить выбор из UI
        self.logger.write(f"Finished import process with status: {result.get('status')}")
        return result
