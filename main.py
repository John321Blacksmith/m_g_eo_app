import asyncio
from aiohttp import web
from geo_app.urls import routes

# app realization
app = web.Application()

# combining the all the routes
app.add_routes(*routes)

if __name__ == '__main__':

    # launching the app
    web.run_app(app)