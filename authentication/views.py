from aiohttp import web
from tortoise import exceptions
from core.utils import error_response
from authentication.models import User
from profiles.models import Profile

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
        bio = ""
        image = ""
        if user is not None:
            profile = await Profile.get_or_none(user=user)
            if profile is not None:
                bio = profile.bio
                image = profile.image

        return web.json_response(
            {
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "token": user.token,
                    "bio": bio,
                    "image": image
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
                bio = ""
                image = ""
                profile = await Profile.get_or_none(user=user)
                if profile is not None:
                    bio = profile.bio
                    image = profile.image

                return web.json_response(
                    {
                        "user": {
                            "email": user.email,
                            "username": user.username,
                            "token": user.token,
                            "bio": bio,
                            "image": image
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
            bio = ""
            image = ""
            profile = await Profile.get_or_none(user=user)
            if profile is not None:
                bio = profile.bio
                image = profile.image

            return web.json_response(
                {
                    "user": {
                        "email": user.email,
                        "username": user.username,
                        "token": user.token,
                        "bio": bio,
                        "image": image
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


@routes.put('/api/user')
async def put_user(request):
    try:
        print('payload:', request['payload'])
        loaded_json = await request.json()
        data = loaded_json['user']
        print('data:', data)

        user_id = int(request['payload']['id'])
        user = await User.get_or_none(id=user_id)
        if user is not None:
            if data.get('username') is not None:
                user.username = data['username']
                if user.username == "":
                    return error_response("username", "username is empty")
            if data.get('email') is not None:
                user.email = data['email']
                if user.email == "":
                    return error_response("email", "email is empty")
            if data.get('password') is not None:
                user.password = data['password']
                if user.password == "":
                    return error_response("password", "password is empty")

            await user.save()

            profile = await Profile.get_or_none(user=user)
            if profile is None:
                profile = await Profile(user=user)

            if data.get('bio') is not None:
                profile.bio = data['bio']
            if data.get('image') is not None:
                profile.image = data['image']

            await profile.save()

            return web.json_response(
                {
                    "user": {
                        "email": user.email,
                        "username": user.username,
                        "token": user.token,
                        "bio": profile.bio,
                        "image": profile.image
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
