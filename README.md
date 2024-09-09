Task:
Необходимо разработать HTTP API, с помощью которого можно:
1) добавлять/удалять в хранилище информацию о городах;

2) запрашивать информацию о городах из хранилища;

3) по заданным широте и долготе точки выдавать 2 ближайших к ней города из присутствующих в хранилище.

При запросе к API на добавление нового города клиент указывает только название города, а в хранилище добавляются также координаты города. Данные о координатах можно получать из любого внешнего API.
Реализация хранилища произвольная.
###

Для выполнения запрсов на сохранение
городов, необходимо получить API-ключ на https://geocode.maps.co

В файле .env указать ключ
'''API_KEY = 'your API here'''

Перед выполнением БД-транзакций, необходимо
создать схему таблицы:
'''python main.py makemigrations create-table'''

Убедитесь, Docker-машина запущена.

Затем, инициализировать образ:
'''docker-compose build -d'''

И запустить контейнер:
'''docker-compose up -d'''

Перед выполнением запрсов модифицации
и расчёта ближайших городов, необходимо
пополнить хранилище

Список эндпоинтов соответствующих методов
'''
http://localhost:8000/add-city/<name:str>  --> POST
http://localhost:8000/cities/<id:int>/  --> GET
http://localhost:8000/delete-city/<id:int>/  --> DELETE
http://localhost:8000/nearest-cities/<city_name:str>  --> GET
http://localhost:8000/update-city/<id:int>/  --> PATCH
http://localhost:8000/delete-city/<id:int>/  --> DELETE
'''

Примеры

1) Добавление, изменение и удаление города из базы данных;

Creation:
'''curl --request POST http://localhost:8000/add-city/Rome
{"message": "Success", "result": {"name": "Rome", "latitude": "41.8933203", "longitude": "12.4829321"}}'''

Deletion:
'''curl --request DELETE http://localhost:8000/delete-city/1/
{'message': 'City has been deleted'}'''

Update
'''curl --request PATCH  "http://localhost:8080/update-city/34/" -d "{\"name\": \"FOOOBAAAR\"}"
{"message": "City data was changed"}'''

2) Запрос сущности города из базы данных;
'''curl --request GET http://localhost:8000/cities/1/
{"name": "Rome", "latitude": "41.8933203", "longitude": "12.4829321"}'''


3) Получение списка двух ближайших городов к определённоиу городу.

Пример 1.
'''curl --request GET http://localhost:8000/nearest-cities/Пекин
{"result": [{"name": "Пекин", "latitude": 39.9057136, "longitude": 116.3912972}, {"name": "Vladivostok", "latitude": 43.1150678, "longitude": 131.8855768}]}'''

Пример 2.
'''curl --request GET http://localhost:8080/nearest-cities/Кемерово
{"result": [{"name": "MOSCOW", "latitude": 40.0, "longitude": 37.6174782}]}'''

