import jwt
from datetime import datetime, timedelta
from aiohttp import web
from conduit import settings


def get_token(user_id):
    dt = datetime.now() + timedelta(days=60)

    token = jwt.encode({
        'id': user_id,
        'exp': int(dt.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')


def error_response(name, description):
    return web.json_response(
        {
            "errors": {
                name: [
                    description
                ]
            }
        },
        status=400
    )
