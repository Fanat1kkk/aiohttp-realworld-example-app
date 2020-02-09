from tortoise import fields
from core.models import TimestampedMixin, AbstractBaseModel


class User(TimestampedMixin, AbstractBaseModel):
    username = fields.CharField(db_index=True, max_length=255, unique=True)
    email = fields.CharField(db_index=True, max_length=255, unique=True)
    password = fields.CharField(max_length=128)

    class Meta:
        table = "user"

    def __str__(self):
        return self.username
