# requests handling is done here
from aiohttp.web import json_response, Response
from sqlalchemy.exc import NoResultFound
from geo_app import geo_client
from geo_app.db.transactions import DBManager


class RequestManager:
    """
    This manager implements a
    DB Manager and has a control
    over user's requests.
    """
    def __init__(self, **kwargs) -> None:
        self.api = kwargs['api']
        self.db_configs = kwargs['db_configs']
        self.db_manager = DBManager(
                                    self.db_configs['url']
                                ) if self.db_configs else None
        
    async def get_city(self, request, *args, **kwargs) -> Response:
        """
        Return a city object from
        the database via its index.
        """
        queryset = await self.db_manager.get_row(id=request.match_info['id'], *args, **kwargs)
        if queryset:
            try:
                obj = queryset.one()._mapping
            except NoResultFound:
                return json_response(data={'message':'City was not found'}, status=404)
            
            return json_response(
                data={
                    'name': obj['name'],
                    'latitude': obj['latitude'],
                    'longitude': obj['longitude']
                }, status=200)
        

    async def add_city(self, request) -> Response:
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
                                    api_key=self.api
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
            flag = await self.db_manager.insert_row(**result)
            if flag.rowcount:
                return json_response(
                                data={
                                    'message': 'City has been created',
                                }, status=201)

        return json_response(
                            data={
                                'message': 'Could not add new city',
                                'results': response
                            }, status=404)

    async def delete_city(self, request) -> Response:
        """
        Delete the city object from the
        database via its index.
        """
        flag = await self.db_manager.delete_row(id=request.match_info['id'])
    
        if flag.rowcount == 1:
            return json_response(data={'message': 'City has been deleted'}, status=204)
        return json_response(data={'message': 'No such city found'}, status=404)


    async def update_city(self, request) -> Response:
        """
        Modify fields of the
        city object.
        """
        obj_id = request.match_info['id']
        body = await request.json()
        fields: dict[str, str|float] = {k: v for k, v in body.items()}
   
        if body:
            flag = await self.db_manager.update_row(id=obj_id, body=fields)
            if flag.rowcount == 1:
                return json_response(data={'message': 'City data was changed'}, status=201)
            return json_response(data={'message': 'No such city found'}, status=404)
        return json_response(data={'message': 'Incorrect fields were provided'}, status=400)
    

    async def get_nearest_cities(self, request) -> Response:
        """
        Receive a name of city object
        and return the two nearest
        cities from the database.
        """
       
        results = await self.db_manager.get_nearest_rows(name=request.match_info['city_name'])
        if results:
            return json_response(data={
                                        'results': [
                                                {
                                                    'name': obj.name,
                                                    'latitude': obj.latitude,
                                                    'longitude': obj.longitude
                                                } for obj in results
                                            ]
                                        }, status=200)
        return json_response(data={'message': 'City was wan\'t found'}, status=404)