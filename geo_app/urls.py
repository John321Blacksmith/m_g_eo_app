# API routes realization here
from os import getenv
from aiohttp import web
from .views import RequestManager
from .utils import get_env_vars

# exract neccessary configs
configs = get_env_vars()

# realize an http-manager
r_manager = RequestManager(**configs)

# the endpoints every client will use
routes = [
    # reading requests
    web.get('/cities/{id}/',r_manager.get_city),
    web.get('/nearest-cities/{city_name}', r_manager.get_nearest_cities), # postGis

    # modification requests
    web.post('/add-city/{city_name}', r_manager.add_city),
    web.patch('/update-city/{id}/', r_manager.update_city),
    web.delete('/delete-city/{id}/', r_manager.delete_city),
    
]
