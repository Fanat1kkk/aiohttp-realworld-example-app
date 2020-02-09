from aiohttp import web
from tortoise import exceptions
from authentication.models import User
from core.utils import error_response

routes = web.RouteTableDef()


@routes.post('/api/users')
async def create_user(request):
    try:
        loaded_json = await request.json()

        username = loaded_json['user']['username']
        if username == "":
            return error_response("username", "username is empty")

        email = loaded_json['user']['email']
        if email == "":
            return error_response("email", "email is empty")

        password = loaded_json['user']['password']
        if password == "":
            return error_response("password", "password is empty")

        user = await User.create(username=username, email=email, password=password)  # TODO: set_password
        return web.json_response(
            {
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "token": user.token
                }
            },
            status=201
        )
    except exceptions.IntegrityError as err:
        return error_response("database error", str(err))
    except Exception as err:
        return error_response("error", str(err))


@routes.post('/api/users/login')
async def login_user(request):
    try:
        loaded_json = await request.json()

        email = loaded_json['user']['email']
        password = loaded_json['user']['password']

        user = await User.filter(email=email).first()
        if user is not None:
            if user.password == password:  # TODO: check password
                return web.json_response(
                    {
                        "user": {
                            "email": user.email,
                            "username": user.username,
                            "token": user.token
                        }
                    },
                    status=200
                )
            else:
                return error_response("password", "password error")
        else:
            return error_response("user", "user not found")
    except exceptions.IntegrityError as err:
        return error_response("database error", str(err))
    except Exception as err:
        return error_response("error", str(err))


@routes.get('/api/user')
async def get_user(request):
    try:
        user_id = int(request['payload']['id'])
        user = await User.filter(id=user_id).first()
        if user is not None:
            return web.json_response(
                {
                    "user": {
                        "email": user.email,
                        "username": user.username,
                        "token": user.token
                    }
                },
                status=200
            )
        else:
            return error_response("user", "user not found")
    except exceptions.IntegrityError as err:
        return error_response("database error", str(err))
    except Exception as err:
        return error_response("error", str(err))
