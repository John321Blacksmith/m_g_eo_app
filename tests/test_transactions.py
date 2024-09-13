import pytest
from sqlalchemy.engine import URL
from ..geo_app.db.models import City
from sqlalchemy import create_engine
from geo_app.utils import get_env_vars

# the test coverage will be here