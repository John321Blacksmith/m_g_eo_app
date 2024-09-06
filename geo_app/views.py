# requests handling is done here

import asyncio
import serializers
import models
from aiohttp.web import Response


async def get_cities(request) -> Response[dict]:
    """
    Return a list of sities
    from the database with
    their information.
    """
    return Response()


async def get_nearest_cities(request) -> Response[dict]:
    """
    Receive a name of the
    city as a query parameter
    and return the two nearest
    cities from the database
    """
    return Response()


# Cruds
async def get_city(request) -> Response:
    """
    Return a city object.
    """
    return Response()


async def add_city(request) -> Response:
    """
    Add a new city object to the
    database.
    """
    return Response()


async def delete_city(request) -> Response:
    """
    Delete the city object from the
    database.
    """
    return Response()


async def update_city(request) -> Response:
    """
    Modify fields of the
    city object.
    """
    return Response()