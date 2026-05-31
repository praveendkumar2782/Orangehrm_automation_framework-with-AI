from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "reports"
TRACES_DIR = REPORTS_DIR / "traces"

BASE_URL = "https://opensource-demo.orangehrmlive.com"
LOGIN_URL = f"{BASE_URL}/web/index.php/auth/login"
DASHBOARD_URL = f"{BASE_URL}/web/index.php/dashboard/index"

DEFAULT_USERNAME = "Admin"
DEFAULT_PASSWORD = "admin123"

VIEWPORT = {"width": 1920, "height": 1080}
DEFAULT_TIMEOUT = 60_000
