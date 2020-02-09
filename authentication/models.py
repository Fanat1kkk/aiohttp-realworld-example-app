import jwt
from datetime import datetime, timedelta
from tortoise import fields
from conduit import settings
from core.models import TimestampedMixin, AbstractBaseModel


class User(TimestampedMixin, AbstractBaseModel):
    username = fields.CharField(db_index=True, max_length=255, unique=True)
    email = fields.CharField(db_index=True, max_length=255, unique=True)
    password = fields.CharField(max_length=128)

    class Meta:
        table = "user"

    def __str__(self):
        return self.username

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
