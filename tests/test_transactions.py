import pytest
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from ..geo_app.db.models import City
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parent
load_dotenv()
env_path = BASE_DIR/'.env'
load_dotenv(dotenv_path=env_path)
