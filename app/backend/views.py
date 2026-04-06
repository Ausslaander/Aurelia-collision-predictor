from app.backend.base_view import View
from config.config import DATA_PATH
from app.backend.accessors import SatelliteAccessor, MathModuleAccessor
from datetime import datetime
import json
import numpy as np


class SatelliteDataView(View):
    def __init__(self):
        super().__init__()
        self.accessor = SatelliteAccessor()

    async def get_data(self, group: str = None) -> dict:
        # TODO в group тем или иным образом должна поступать информация с UI
        self.accessor.group = group
        data = await self.accessor.connect()
        if not data:
            self.logger.write("Satellite data import failed: empty response")
            return {"status": "error", "message": "Import failed: data source returned no data"}

        file_path = self.save_data(data)
        return {"status": "ok", "message": f"Import completed: {file_path.name}"}

    def save_data(self, data: list[dict]):
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        satellites_dir = DATA_PATH / "satellites_data"
        satellites_dir.mkdir(parents=True, exist_ok=True)
        file_path = satellites_dir / f"{current_time}.json"

        payload = {
            "format": "OMM",
            "group": self.accessor.group,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "records": data,
        }

        with file_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
        self.logger.write(f"Satellite data saved to {file_path}")
        return file_path


class CollisionPredictionView(View):
    def __init__(self):
        super().__init__()
        self.accessor = MathModuleAccessor()  # TODO Потом тут будет матмодуль
        self.covariance_matrix = np.zeros((3, 3))
        self.constaint_level = 0

    def predict_collisions(self):
        pass
    # TODO Надо будет реализовать окно с выбором файла данных для анализа
    # TODO Также надо реализовать окно с заполнением данных матрицы и константы уровня для характеристики эллипса

