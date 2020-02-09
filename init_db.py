from tortoise import Tortoise, run_async
from conduit import settings


async def init():
    await Tortoise.init(
        db_url=settings.DB_URL,
        modules={'models': ['authentication.models']}
    )
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(init())
