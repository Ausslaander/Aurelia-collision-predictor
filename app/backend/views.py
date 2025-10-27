from app.backend.base_view import View
from config.config import DATA_PATH
from app.backend.accessors import SatelliteAccessor
from datetime import datetime

class SatelliteDataView(View):
    def __init__(self):
        super().__init__()
        self.accessor = SatelliteAccessor()

    async def get_data(self, group: str = None):
        #TODO в group тем или иным образом должна поступать информация с UI
        self.accessor.group = group
        data = await self.accessor.connect()
        self.save_data(data)


    def save_data(self, data):
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        satellites_dir = DATA_PATH / 'satellites_data'
        satellites_dir.mkdir(parents=True, exist_ok=True)
        file_path = satellites_dir / f"{current_time}.csv"
        with file_path.open('w', encoding='utf-8') as f:
            f.write(data)
        self.logger.write(f"Satellite data saved to {file_path}")


