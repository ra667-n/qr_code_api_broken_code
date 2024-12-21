import logging.config
import os
import base64
from typing import List
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta
from app.config import ADMIN_PASSWORD, ADMIN_USER, ALGORITHM, SECRET_KEY
import validators  # Make sure to install this package
from urllib.parse import urlparse, urlunparse

load_dotenv()

def setup_logging():
    """Sets up logging from a configuration file."""
    logging_config_path = os.path.join(os.path.dirname(__file__), '..', 'logging.conf')
    normalized_path = os.path.normpath(logging_config_path)
    try:  # Handle potential FileNotFoundError
        logging.config.fileConfig(normalized_path, disable_existing_loggers=False)
    except FileNotFoundError:
        logging.basicConfig(level=logging.INFO) # Basic logging if config not found
        logging.warning(f"Logging config file not found at {normalized_path}. Using basic configuration.")


def authenticate_user(username: str, password: str) -> Optional[dict]: # Type hint return value
    """Authenticates a user."""
    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        return {"username": username}
    logging.warning(f"Authentication failed for user: {username}")
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None): # Type hint and default None
    """Generates a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta is not None else timedelta(minutes=15)) # Corrected logic
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_and_sanitize_url(url_str: str) -> Optional[str]: # Type hint return value
    """Validates and sanitizes a URL."""
    if validators.url(url_str):
        parsed_url = urlparse(url_str)
        sanitized_url = urlunparse(parsed_url)
        return sanitized_url
    else:
        logging.error(f"Invalid URL provided: {url_str}")
        return None

def encode_url_to_filename(url: str) -> str: # Type hint url parameter
    """Encodes a URL to a filename-safe base64 string."""
    sanitized_url = validate_and_sanitize_url(url) # No need to convert to string here
    if sanitized_url is None:
        raise ValueError("Provided URL is invalid and cannot be encoded.")
    encoded_bytes = base64.urlsafe_b64encode(sanitized_url.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8').rstrip('=')
    return encoded_str

def decode_filename_to_url(encoded_str: str) -> str:
    """Decodes a filename-safe base64 string back to a URL."""
    padding_needed = 4 - (len(encoded_str) % 4)
    if padding_needed:
        encoded_str += "=" * padding_needed
    decoded_bytes = base64.urlsafe_b64decode(encoded_str)
    return decoded_bytes.decode('utf-8')

def generate_links(action: str, qr_filename: str, base_api_url: str, download_url: str) -> List[dict]:
    """Generates HATEOAS links."""
    links = []
    original_url = decode_filename_to_url(qr_filename[:-4]) # Decode here
    if action in ["list", "create"]:
        links.append({"rel": "view", "href": download_url + f"/{qr_filename}", "action": "GET", "type": "image/png"}) # correct href
    if action in ["list", "create", "delete"]:
        delete_url = f"{base_api_url}/qr-codes/{qr_filename}"
        links.append({"rel": "delete", "href": delete_url, "action": "DELETE", "type": "application/json"})
    return links
