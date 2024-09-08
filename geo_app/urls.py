# API routes realization here
from aiohttp import web
from .views import (
    add_city, 
    update_city, get_city,
    delete_city, get_nearest_cities
)


# the endpoints every client will use
routes = [
    # reading requests
    web.get('/cities/{id}/', get_city),
    web.get('/nearest-cities/{name}', get_nearest_cities), # postGis

    # modification requests
    web.post('/add-city/{city_name}', add_city),
    web.patch('/update-city/{id}/', update_city),
    web.delete('/delete-city/{id}/', delete_city),
    
]
