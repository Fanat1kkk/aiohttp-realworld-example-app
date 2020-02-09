from aiohttp import web


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
