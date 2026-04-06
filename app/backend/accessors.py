import json
from pathlib import Path

import aiohttp

from app.backend.base_accessor import BaseAccessor
from config.config import BASE_SATELLITE_DATA_URL, DATA_PATH


class SatelliteAccessor(BaseAccessor):
    def __init__(self, url: str = BASE_SATELLITE_DATA_URL, format: str = "json", group: str = None):
        super().__init__()
        self.url = url
        self.format = format
        self.group = group

    def _extract_omm_records(self, payload):
        # CelesTrak может вернуть список или объект с полями data/member/omm
        if isinstance(payload, list):
            return payload
        if not isinstance(payload, dict):
            return []

        for key in ("data", "member", "omm"):
            value = payload.get(key)
            if isinstance(value, list):
                return value

        if payload.get("OBJECT_NAME") or payload.get("NORAD_CAT_ID"):
            return [payload]
        return []

    async def connect(self) -> list[dict] | None:
        self.logger.write(f"Connecting to satellite at {self.url}")

        params = {
            "GROUP": self.group or "STARLINK",
            "FORMAT": self.format,
        }
        headers = {
            "User-Agent": "AureliaCollisionPredictor/0.1",
            "Accept": "application/json, */*",
        }

        try:
            timeout = aiohttp.ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.url, params=params, headers=headers) as response:
                    if response.status != 200:
                        self.logger.write(
                            f"Failed to fetch satellite data. Status: {response.status}, params: {params}"
                        )
                        return None

                    payload = await response.json(content_type=None)
                    records = self._extract_omm_records(payload)
                    if not records:
                        self.logger.write("Got OMM response, but no records were found")
                        return None

                    self.logger.write(f"Got OMM response with {len(records)} records")
                    return records
        except aiohttp.ClientError as exc:
            self.logger.write(f"HTTP error while fetching satellite data: {exc}")
            return None
        except json.JSONDecodeError as exc:
            self.logger.write(f"Failed to decode OMM JSON response: {exc}")
            return None
        except Exception as exc:
            self.logger.write(f"Unexpected error while fetching satellite data: {exc}")
            return None


class MathModuleAccessor(BaseAccessor):
    def __init__(self):
        super().__init__()


class InternalDataAccessor(BaseAccessor):
    def __init__(self):
        super().__init__()

    def get_latest_satellite_data(self, path: Path | str = DATA_PATH / "satellites_data"):
        self.logger.write(f"Fetching data from {path}")
        file_path = Path(path).resolve()
        latest_file_path = self.get_latest_file_path(file_path)
        if latest_file_path is None:
            self.logger.write(f"No latest file found at {path}")
            return None

        self.logger.write(f"Latest file path: {latest_file_path}")
        try:
            with latest_file_path.open("r", encoding="utf-8") as f:
                payload = json.load(f)

            if isinstance(payload, list):
                data = payload
            elif isinstance(payload, dict):
                data = self._extract_omm_records(payload)
            else:
                data = None

            if not data:
                self.logger.write(f"No OMM records found in {latest_file_path}")
                return None

            self.logger.write(f"Read {len(data)} records from {latest_file_path}")
            return data
        except Exception as exc:
            self.logger.write(f"Error reading file {latest_file_path}: {exc}")
            return None

    def _extract_omm_records(self, payload):
        if isinstance(payload, list):
            return payload
        if not isinstance(payload, dict):
            return []

        for key in ("data", "member", "omm"):
            value = payload.get(key)
            if isinstance(value, list):
                return value

        if payload.get("OBJECT_NAME") or payload.get("NORAD_CAT_ID"):
            return [payload]
        return []

    def get_latest_file_path(self, path: Path | str):
        self.logger.write(f"Fetching latest file from {path}")
        files = [p.resolve() for p in Path(path).glob("*.json")]
        if not files:
            self.logger.write(f"No file found in {path}")
            return None

        self.logger.write(f"Found {len(files)} files in {path}")
        return max(files, key=lambda p: p.stem)


if __name__ == "__main__":
    accessor = InternalDataAccessor()
    print(accessor.get_latest_satellite_data())
