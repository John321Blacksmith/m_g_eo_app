from typing import Coroutine
from pathlib import Path
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy import (select, insert, update, delete)
from sqlalchemy import Engine, create_engine
from .models import CityBase, City
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()
env_path = BASE_DIR/'.env'
load_dotenv(dotenv_path=env_path)


def setup_engine() -> Engine:
    """
    Create an engine object
    """
    return create_engine("sqlite+pysqlite:///cities1.db", echo=True)


def create_table():
    """
    Create a table scheme for
    the first time.
    """
    engine = setup_engine()
    CityBase.metadata.create_all(engine)
    

async def add_row(**params):
    """
    Create a new city object
    in the db.
    """
    engine = setup_engine()
    with Session(bind=engine) as session:
        if 'No Data' not in params.values():
            city = City(
                        name=params['name'],
                        latitude=params['latitude'],
                        longitude=params['longitude']
                    )
            session.add(city)
            session.flush()
            session.commit()

            return city.id
        else:
            return None


async def get_row(**params) -> City:
    """
    Retrieve a db row via index.
    """
    engine = setup_engine()

    with Session(bind=engine) as session:
        result = session.execute(select(City).where(City.id == params['id'])).first()
        return result if result else None


async def update_row(**params):
    """
    Set new data to an existing row.
    """
    engine = setup_engine()
    with Session(bind=engine) as session:
        result = session.execute(update(City).where(City.id == params['id']).values(**params['body']))
        session.commit()
        return result if result else None


async def delete_row(**params):
    """
    Permanently delete a row
    from the database.
    """
    engine = setup_engine()
    with Session(bind=engine) as session:
        result = session.execute(delete(City).where(City.id == params['id']))
        session.commit()
        return result if result else None
    

async def get_nearby_rows(**params):
    """
    Retrive two nearest cities
    from the database.
    """
    engine = setup_engine()
    with Session(bind=engine) as session:
        ...
    