import os
from pathlib import Path
import dotenv

BASE_DIR = Path(__file__).resolve().parent
# load environment
dotenv.load_dotenv(f"{BASE_DIR}/.env")

API_KEY = os.getenv('TOKEN')

mongodb_config = {
    "username": os.getenv('USER'),
    "password": os.getenv('PASSWORD'),
    "hostname": os.getenv('HOST'),
    "database": os.getenv('DB_NAME')
}
