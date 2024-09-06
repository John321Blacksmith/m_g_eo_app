# API routes realization here
from aiohttp import web
import views


# the endpoints every client will use
routes = [
    # reading requests
    web.get('/cities', views.get_cities),
    web.get('/cities/{id}/', views.get_city),
    web.get('/nearest-cities/{name}'),

    # modification requests
    web.post('/cities', views.add_city),
    web.patch('/cities/{id}/'),
    web.delete('/cities/{id}/'),
]
