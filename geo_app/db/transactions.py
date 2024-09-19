from functools import wraps
from typing import Callable, Any
from sqlalchemy import Connection, create_engine, Engine
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import (select, insert, update, delete)
from .models import City
from ..utils import sort_dists, distance



class DBManager:
    """
    This manager controls
    connection to the db
    and applied transactions.
    """
    def __init__(self, url: str) -> None:
        self.url = url
        self.engine = create_engine(self.url) # the engine remains up the server's life
    
    def transaction(funct):
        """
        Take a query transaction and
        return a corresponding queryset.
        """
        @wraps(funct)
        async def wrapper(self, *args, **kwargs):
            with self.engine.connect() as conn:
                query = await funct(self, *args, **kwargs)
                try:
                    queryset = conn.execute(query)
                except (NoResultFound, IntegrityError):
                    conn.rollback()
                    return None
                if query.__class__.__name__ in ['Insert', 'Update', 'Delete']:
                    conn.commit()
                return queryset
        return wrapper
    
    @transaction
    async def get_row(self, **params):
        """Selection query"""
        return select(City).where(City.id == params['id'])
    
    @transaction
    async def insert_row(self, **params):
        """Insertion query"""
        return insert(City).values(**params)

    @transaction
    async def update_row(self, **params):
        """Update query"""
        return update(City).where(City.id == params['id']).values(**params['body'])
    
    @transaction
    async def delete_row(self, **params):
        """Deletion query"""
        return delete(City).where(City.id == params['id'])

    async def get_nearest_rows(self, **params) -> list[City] | None:
        """
        Retrive a current obj and a list
        of ones to make calculations.
        """
        result: list[City] | None = None
        if self.engine:
            with self.engine.connect() as connection:
                cr_city = connection.execute(select(City).where(City.name == params['name'])).first() # prevent multpl dupls
                if cr_city:
                    cities = connection.execute(select(City)).all()

                    # make a list of distances, excluding current city
                    distances: list[tuple[City, float]] = [
                        (city, distance(cr_city, city)) for city in cities\
                            if city._mapping['name'] != cr_city._mapping['name']
                        ]

                    # sort a list of distances
                    sorted_dists: list[tuple[City, float]] = sort_dists(distances)

                    # and get the two nearest values
                    two_nearest: list[City] = [tup[0] for tup in sorted_dists[:2]]

                    result = two_nearest
        return result