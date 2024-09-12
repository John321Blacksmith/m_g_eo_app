# API routes realization here
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from aiohttp import web
from .views import RequestManager

BASE_DIR = Path(__file__).resolve().parent
load_dotenv()
env_path = BASE_DIR/'.env'
load_dotenv(dotenv_path=env_path)


configs = {
    'api': getenv('API_KEY'),
    'db_configs': {
        'url': getenv('SQLITE_PATH')
    }
}

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
