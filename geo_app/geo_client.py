# http client sends requests to an external source
import asyncio
from typing import Coroutine, List
from aiohttp import ClientSession, ClientResponse


async def fetch_city(**query) -> Coroutine[ClientResponse]:
    """
    Get a list of geographical objects
    from the WEB.
    """
    async with ClientSession() as session:
        async with session.get(f'https://geocode.maps.co/search?q={query['city_name']}&api_key={query['api_key']}') as r:
            response = await r.json()

            return response