import sys
import asyncio
from aiohttp import web
from sqlalchemy import create_engine
from geo_app.db.models import CityBase
from geo_app.urls import routes


def make_app() -> None:
    # app realization
    app = web.Application()

    # combining the all the routes
    app.add_routes(routes)

    # launching the app
    web.run_app(app)


def make_migrations() -> None:
    """
    Perform database migrations.
    """
    if sys.argv[2] == 'create-table':
        """
        Create a table scheme for
        the first time.
        """
        engine = create_engine(f'sqlite+pysqlite:///{sys.argv[3]}.db')
        CityBase.metadata.create_all(engine)
        print(f'DB \'{sys.argv[3]}\' was initialized!')


def perform_commands() -> None:
    command = sys.argv[1]
    
    if command == 'run-app':
        return make_app()
    
    if command == 'makemigrations':
        return make_migrations()


if __name__ == '__main__':
    perform_commands()