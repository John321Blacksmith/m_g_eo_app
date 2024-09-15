# Description
This microservise facilitates the client to interact with the city objects
so the client can fetch, add and update cities.
<div align="center">
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
<img src="https://img.shields.io/badge/aiohttp-9999FF.svg?style=for-the-badge&logo=aiohttp&logoColor=white" />
<img src="https://img.shields.io/badge/SQLAlchemy-9999FF.svg?style=for-the-badge&logo=SQLAlchemy&logoColor=white" />
<img src="https://img.shields.io/badge/Pydantic-9999FF.svg?style=for-the-badge&logo=Pydantic&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-9999FF.svg?style=for-the-badge&logo=Docker&logoColor=white" />
<img src="https://img.shields.io/badge/VS%20Code%20Insiders-35b393.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white" />
<img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white" />
</div>

# Реализация
Для выполнения запрoсов на сохранение
городов, необходимо получить API-ключ на https://geocode.maps.co

В созданном в основной директории
файле **.env** указать ключ и
конфигурации продакшена или локального
хранилища:
```
API_KEY = 'your API here'

PROD='dactive'

DB_NAME = '<db_name>'
USER = 'admin'
PASSWORD = '<password>'
PORT='<db_port>'

SQLITE_PATH = 'sqlite+pysqlite:///<db_name: str>.db'
```

Организуем виртуальную среду, подгружаем необходимые
зависимости и активируем:
```
python -m venv .venv

pip install -r requirements.txt

.venv\Scripts\activate
```

Перед выполнением БД-транзакций, необходимо
создать схему таблицы:

```
python main.py makemigrations create-table sqlite+pysqlite cities
```

Убедитесь, Docker-машина запущена.

Затем, инициализировать образ:

```
docker-compose build
```

И запустить контейнер:

```
# контейнер в фоновом режиме
docker-compose up -d

# запуск с логами
docker-compose up
```

Перед выполнением запрсов модифицации
и расчёта ближайших городов, необходимо
пополнить хранилище

Список эндпоинтов и соответствующих методов

```
http://localhost:8000/add-city/<name:str>  --> POST
http://localhost:8000/cities/<id:int>/  --> GET
http://localhost:8000/delete-city/<id:int>/  --> DELETE
http://localhost:8000/nearest-cities/<city_name:str>  --> GET
http://localhost:8000/update-city/<id:int>/  --> PATCH
http://localhost:8000/delete-city/<id:int>/  --> DELETE

```

# Примеры применения

1) Добавление, изменение и удаление города из базы данных;

Creation:
Для лучшего сравнения, необходимо добавить как можно
больше городов:
```
curl --request POST http://localhost:8000/add-city/Moscow
{"message": "City has been created"}

curl --request POST http://localhost:8000/add-city/Lyubertsy
{"message": "City has been created"}

curl --request POST http://localhost:8000/add-city/Balashikha
{"message": "City has been created"}

curl --request POST http://localhost:8000/add-city/Mytishchi
{"message": "City has been created"}

curl --request POST http://localhost:8000/add-city/Ryazan
{"message": "City has been created"}

curl --request POST http://localhost:8000/add-city/Kazan
{"message": "City has been created"}

curl --request POST http://localhost:8000/add-city/Vladimir
{"message": "City has been created"}

curl --request POST http://localhost:8000/add-city/Chelyabinsk
{"message": "City has been created"}

curl --request POST http://localhost:8000/add-city/New-York
{"message": "City has been created"}
```

Update:
```
curl --request PATCH  "http://localhost:8000/update-city/1/" -d "{\"name\": \"MOSCOW\"}"
{"message": "City data was changed"}
```

Deletion:
```
curl --request DELETE http://localhost:8000/delete-city/8/
{'message': 'City has been deleted'}
```

2) Запрос сущности города из базы данных;
```
curl --request GET http://localhost:8000/cities/1/
{"name": "MOSCOW", "latitude": 55.7505412, "longitude": 37.6174782}
```

3) Получение списка двух ближайших городов к определённоиу городу.

Пример 1.
```
curl --request GET http://localhost:8000/nearest-cities/MOSCOW
{"results": [{"name": "Mytishchi", "latitude": 55.9094928, "longitude": 37.7339358}, {"name": "Lyubertsy", "latitude": 55.6783142, "longitude": 37.89377}]}
```

Пример 2.
```
curl --request GET http://localhost:8000/nearest-cities/Vladimir
{"results": [{"name": "Ryazan", "latitude": 54.6295687, "longitude": 39.7425039}, {"name": "Balashikha", "latitude": 55.7997662, "longitude": 37.9373707}]}

Пример 3.
curl --request GET http://localhost:8080/nearest-cities/Kazan
{"results": [{"name": "Vladimir", "latitude": 56.1288899, "longitude": 40.4075203}, {"name": "Ryazan", "latitude": 54.6295687, "longitude": 39.7425039}]}
```

