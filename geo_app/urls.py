# API routes realization here
from aiohttp import web
from .views import (
    get_cities, get_city,
    add_city, update_city,
    delete_city, get_nearest_cities
)


# the endpoints every client will use
routes = [
    # reading requests
    web.get('/cities', get_cities),
    web.get('/cities/{id}/', get_city),
    web.get('/nearest-cities/{name}', get_nearest_cities),

    # modification requests
    web.post('/cities', add_city),
    web.patch('/cities/{id}/', update_city),
    web.delete('/cities/{id}/', delete_city),
]
