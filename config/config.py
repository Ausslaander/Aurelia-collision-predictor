from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / 'data'
LOGS_PATH = PROJECT_ROOT / 'logs'
BASE_SATELLITE_DATA_URL = "https://celestrak.org/NORAD/elements/gp.php"
