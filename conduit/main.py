import logging
import sys
import asyncio
import uvloop
import aiohttp_cors
from aiohttp import web
from aiohttp_jwt import JWTMiddleware
from tortoise import Tortoise
from conduit.authentication.views import routes as authentication_routes
from conduit import settings

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def on_shutdown(app):
    await Tortoise.close_connections()


def init(argv=None):
    app = web.Application(
        middlewares=[
            JWTMiddleware(
                settings.SECRET_KEY,
                whitelist=[
                    r'/api/users',
                ]
            )
        ]
    )

    app.router.add_routes(authentication_routes)

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

    app.on_shutdown.append(on_shutdown)

    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tortoise.init(db_url=settings.DB_URL,
                                          modules={'models': ['conduit.authentication.models']}))

    web.run_app(init(argv))


if __name__ == '__main__':
    main(sys.argv[1:])
