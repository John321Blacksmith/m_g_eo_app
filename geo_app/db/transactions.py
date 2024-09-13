from sqlalchemy import create_engine
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
    
    async def get_row(self, **params) -> dict[str, int|float] | None:
        """
        Retrieve a db row via index or name.
        """
        result: dict[str, int|float] | None = None
        if self.engine:
            with self.engine.connect() as connection:
                try:
                    queryset = connection.execute(select(City).where(City.id == params['id']))
                    result = queryset.one()._mapping
                except NoResultFound:
                    return None
        return result
    
    async def insert_row(self, **params) -> int | None:
        """
        Create a new city object
        in the db.
        """
        result: int | None = None
        if self.engine:
            with self.engine.connect() as connection:
                if 'No Data' not in params.values():
                    try:
                        result = connection.execute(insert(City).values(**params))
                    except IntegrityError as exc:
                        print(exc.args)
                        connection.rollback()
                
                    connection.commit()
                    return result.rowcount
        return result
    
    async def update_row(self, **params) -> int | None:
        """
        Set new data to an existing row.
        """
        result: int | None = None
        if self.engine:
            with self.engine.connect() as connection:
                try:
                    result = connection.execute(update(City)
                                                .where(City.id == params['id'])
                                                .values(**params['body']))
                except IntegrityError as exc:
                    print(exc.args)
                    connection.rollback()
                
                connection.commit()
                return result.rowcount
        return result
                
    async def delete_row(self, **params) -> int | None:
        """
        Permanently delete a row
        from the database.
        """
        result: int | None = None
        if self.engine:
            with self.engine.connect() as connection:
                try:
                    result = connection.execute(delete(City).where(City.id == params['id']))
                except IntegrityError as exc:
                    print(exc.args)
                    connection.rollback()
                connection.commit()
                return result.rowcount
        return result
    
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