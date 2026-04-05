from app.backend.base_accessor import BaseAccessor
import aiohttp

from config.config import BASE_SATELLITE_DATA_URL


class SatelliteAccessor(BaseAccessor):
    def __init__(self, url: str = BASE_SATELLITE_DATA_URL, format: str = "csv", group: str = None):
        super().__init__()
        self.url = url
        self.format = format
        self.group = group

    async def connect(self) -> str | None:
        self.logger.write(f"Connecting to satellite at {self.url}")

        params = {
            "GROUP": self.group,
            "FORMAT": self.format,
        }
        headers = {
            "User-Agent": "AureliaCollisionPredictor/0.1",
            "Accept": "text/csv,*/*",
        }

        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.url, params=params, headers=headers) as response:
                    if response.status != 200:
                        self.logger.write(
                            f"Failed to fetch satellite data. Status: {response.status}, params: {params}"
                        )
                        return None

                    text = await response.text()
                    self.logger.write("Got response")
                    return text
        except aiohttp.ClientError as exc:
            self.logger.write(f"HTTP error while fetching satellite data: {exc}")
            return None
        except Exception as exc:
            self.logger.write(f"Unexpected error while fetching satellite data: {exc}")
            return None

