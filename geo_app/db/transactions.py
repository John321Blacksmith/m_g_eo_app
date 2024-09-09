from pathlib import Path
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy import (select, insert, update, delete)
from sqlalchemy import Engine, create_engine
from .models import CityBase, City
from dotenv import load_dotenv
from ..utils import sort_dists, distance



BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv()
env_path = BASE_DIR/'.env'
load_dotenv(dotenv_path=env_path)


def setup_engine() -> Engine:
    """
    Create an engine object
    """
    return create_engine("sqlite+pysqlite:///cities1.db", echo=True)


def create_table() -> None:
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


async def get_row(**params):
    """
    Retrieve a db row via index or name.
    """
    engine = setup_engine()

    with Session(bind=engine) as session:
        if params['id']:
            result = session.execute(select(City).where(City.id == params['id'])).first()
        if params['name']:
            result = session.execute(select(City).where(City.name == params['name'])).first()
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
    

async def get_nearest_rows(**params):
    """
    Retrive a current obj and a list
    of ones to make calculations.
    """
    engine = setup_engine()
    with Session(bind=engine) as session:
        current_city = session.execute(select(City).where(City.name == params['name'])).first()
        cities = session.execute(select(City)).all()

        # make a list of distances
        distances: list[tuple[City, float]] = [(city, distance(current_city, city)) for city in cities]

        # sort a list of distances 
        sorted_dists: list[tuple[City, float]] = sort_dists(distances)

        # and get the two nearest values
        two_nearest: list[City] = [tup[0] for tup in sorted_dists[:2]]

        return two_nearest

    