from app.backend.base_accessor import BaseAccessor
from datetime import datetime
import requests
import aiohttp

from config.config import DATA_PATH, BASE_SATELLITE_DATA_URL


class SatelliteAccessor(BaseAccessor):
    def __init__(self, url: str = None, format: str = 'csv', group: str = None):
        super().__init__()
        self.url = url
        self.format = format
        self.group = group

    async def get_site_status(self) -> int | None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, timeout=5) as response:
                    return response.status
        except Exception:
            return None

    async def connect(self):
        self.logger.write(f"Connecting to satellite at {self.url}")
        status = await self.get_site_status()

        if status is None:
            self.logger.write(f"Failed to connect to {self.url}.")
        if status is not None:
            self.logger.write(f"Connected to {self.url}. Status code: {status}")
            if status == 200:
                current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                resp = requests.get(f"{BASE_SATELLITE_DATA_URL}?GROUP={self.group}&FORMAT={self.format}")
                resp.raise_for_status()
                satellites_dir = DATA_PATH / 'satellites_data'
                satellites_dir.mkdir(parents=True, exist_ok=True)
                file_path = satellites_dir / f"{current_time}.csv"
                with file_path.open('w', encoding='utf-8') as f:
                    f.write(resp.text)
                self.logger.write(f"Satellite data saved to {file_path}")


if __name__ == "__main__":
    accessor = SatelliteAccessor(
        url=BASE_SATELLITE_DATA_URL,
        group='starlink'
    )
    import asyncio
    asyncio.run(accessor.connect())
