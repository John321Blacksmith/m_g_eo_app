import sys
import asyncio
from aiohttp import web
from geo_app.db.transactions import create_table
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
        create_table()


def perform_commands() -> None:
    command = sys.argv[1]
    
    if command == 'run-app':
        return make_app()
    
    if command == 'makemigrations':
        return make_migrations()


if __name__ == '__main__':
    perform_commands()