import os
from pathlib import Path
from dotenv import load_dotenv
import pytest

# Load environment variables from .env file (if it exists). This is for local development convenience.
load_dotenv()

@pytest.fixture(scope="session", autouse=True)
def set_test_environment():
    os.environ["SECRET_KEY"] = "test_secret_key"
    os.environ["QR_CODE_DIR"] = "./test_qr_codes"
    os.environ["SERVER_BASE_URL"] = "http://testserver"
    os.environ["SERVER_DOWNLOAD_FOLDER"] = "test_downloads"
    yield

    from app import config  
    
    try:
        import shutil
        shutil.rmtree("./test_qr_codes")
    except FileNotFoundError:
        pass

os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["QR_CODE_DIR"] = "./test_qr_codes"
os.environ["SERVER_BASE_URL"] = "http://testserver"
os.environ["SERVER_DOWNLOAD_FOLDER"] = "test_downloads"

# Configuration settings
QR_DIRECTORY = Path(os.getenv('QR_CODE_DIR', './qr_codes'))
QR_DIRECTORY.mkdir(parents=True, exist_ok=True)

FILL_COLOR = os.getenv('FILL_COLOR', 'red')
BACK_COLOR = os.getenv('BACK_COLOR', 'white')

SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', 'http://localhost:80')
SERVER_DOWNLOAD_FOLDER = os.getenv('SERVER_DOWNLOAD_FOLDER', 'downloads')

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required.")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
except ValueError:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be an integer.")

ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'secret')

if not ADMIN_USER or not ADMIN_PASSWORD:
    print("WARNING: ADMIN_USER and ADMIN_PASSWORD environment variables are not set. Basic authentication will not function. This is highly discouraged in production.")
