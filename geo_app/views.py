# requests handling is done here
from os import getenv
import math
from pathlib import Path
from json import JSONEncoder
from dotenv import load_dotenv
from aiohttp.web import json_response, Response
from geo_app import geo_client
from geo_app.db.transactions import (
                            add_row, update_row, delete_row,
                            get_nearest_rows, get_row
                        )


BASE_DIR = Path(__file__).resolve().parent
load_dotenv()
env_path = BASE_DIR/'.env'
load_dotenv(dotenv_path=env_path)


async def add_city(request) -> Response:
    """
    Fetch a city object from
    the external API and add
    it to the database.
    :args:
        request: Request
    :return:
        success_message: dict[str, int | str]
    """
    response = await geo_client.fetch_city(
                                city_name=request.match_info['city_name'],
                                api_key=getenv('API_KEY')
                            )
    # there may have been several results,
    # and the server choses the most important one

    # so here is the filtration of the cities
    types: list[str] = ['city', 'town', 'administrative']
    cities = [obj for obj in response if obj['type'] in types]
    city = cities[0] if len(cities) else None
    
    result = {
                'name': request.match_info['city_name'],
                'latitude': city['lat'] if city else 'No Data',
                'longitude': city['lon'] if city else 'No Data'
            }
    
    # adding the result as a new record to the
    # database if it does not exist there yet
    if result:
        # perform dumping to the db
        row_id = await add_row(**result)
        if row_id:
            return json_response(
                            data={
                                'message': 'Success',
                                'new_city_id': row_id
                            }, status=201)
        
    return json_response(
                        data={
                            'message': 'Could not add new city',
                            'results': response
                        }, status=404)

# Cruds
async def get_city(request) -> Response:
    """
    Return a city object from
    the database via its index.
    """
    result = await get_row(id=request.match_info['id'])
    if result:
        obj = result[0]
        return json_response(
            data={
                'name': obj.name,
                'latitude': obj.latitude,
                'longitude': obj.longitude
            }, status=200)
    return json_response(data={'message':'City was not found'}, status=404)


async def delete_city(request) -> Response:
    """
    Delete the city object from the
    database via its index.
    """
    result = await delete_row(id=request.match_info['id'])
    
    if result:
        return json_response(data={'message': 'City has been deleted'}, status=204)
    return json_response(body={'message': 'No such city found'}, status=404)


async def update_city(request) -> Response:
    """
    Modify fields of the
    city object.
    """
    obj_id = request.match_info['id']
    body = await request.json()
    fields: dict[str, str|float] = {k: v for k, v in body.items()}

    if body:
        obj = await update_row(id=obj_id, body=fields)
        if obj.rowcount > 0:
            return json_response(data={'message': 'City data was changed'}, status=201)
        return json_response(body={'message': 'No such city found'}, status=404)
    return json_response(body={'message': 'Incorrect fields were provided'}, status=400)
    

async def get_nearest_cities(request) -> Response:
    """
    Receive a name of city object
    and return the two nearest
    cities from the database.
    """
    
    result = await get_nearest_rows(name=request.match_info['city_name'])

    return json_response(data={
                                'result': [
                                        {
                                            'name': obj[0].name,
                                            'latitude': obj[0].latitude,
                                            'longitude': obj[0].longitude
                                        } for obj in result
                                    ]
                                }, status=200)