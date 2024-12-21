import os
import pytest
from pathlib import Path
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True) # autouse=True ensures it runs for all tests
def set_test_environment():
    os.environ["SECRET_KEY"] = "test_secret_key"  # Set a test-specific key
    # Add other necessary env vars here too
    os.environ["QR_CODE_DIR"] = "./test_qr_codes" #set QR_CODE_DIR for tests
    os.environ["SERVER_BASE_URL"] = "http://testserver"
    os.environ["SERVER_DOWNLOAD_FOLDER"] = "test_downloads"
    yield #important for teardown
    try:
        import shutil
        shutil.rmtree("./test_qr_codes")
    except FileNotFoundError:
        pass

# Load environment variables from .env file
load_dotenv()
SECRET_KEY="your_development_secret_key"


# QR Code Directory
QR_DIRECTORY = Path(os.getenv('QR_CODE_DIR', './qr_codes'))
QR_DIRECTORY.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

# QR Code Colors
FILL_COLOR = os.getenv('FILL_COLOR', 'red')
BACK_COLOR = os.getenv('BACK_COLOR', 'white')

# Server Configuration
SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', 'http://localhost:80')
SERVER_DOWNLOAD_FOLDER = os.getenv('SERVER_DOWNLOAD_FOLDER', 'downloads')

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY")

export SECRET_KEY="your_development_secret_key"  # Set the variable
pytest  # Run your tests

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required.")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
except ValueError:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be an integer.")

# Admin Credentials (Use with extreme caution in production - prefer more secure methods)
ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Check if admin credentials are set, if not, print a warning
if not ADMIN_USER or not ADMIN_PASSWORD:
    print("WARNING: ADMIN_USER and ADMIN_PASSWORD environment variables are not set. Basic authentication will not function. This is highly discouraged in production.")
