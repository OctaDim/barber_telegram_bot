import os

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = load_dotenv(os.path.join(BASE_DIR, ".env"))

DB_USER = os.getenv('POSTGRES_DB_USER')
DB_PASSWORD = os.getenv('POSTGRES_DB_PASSWORD')
DB_HOST = os.getenv('POSTGRES_DB_HOST')
DB_PORT = os.getenv('POSTGRES_DB_PORT')
DB_NAME = os.getenv('POSTGRES_DB_NAME')

db_engine_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
