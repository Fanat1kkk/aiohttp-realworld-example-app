from tortoise import fields, models
from core.models import TimestampedMixin


class Profile(TimestampedMixin, models.Model):
    user = fields.OneToOneField('models.User', on_delete=fields.CASCADE, db_index=True)
    bio = fields.TextField(null=True)
    image = fields.CharField(max_length=200, null=True)
