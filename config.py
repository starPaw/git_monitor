import os
from pathlib import Path
import dotenv

BASE_DIR = Path(__file__).resolve().parent
# load environment
dotenv.load_dotenv(f"{BASE_DIR}/.env")

API_KEY = os.getenv('TOKEN')

mongodb_config = {
    "username": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "hostname": os.getenv('DB_HOST'),
    "database": os.getenv('DB_NAME')
}
