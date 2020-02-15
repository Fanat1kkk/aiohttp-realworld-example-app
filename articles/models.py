from core.models import TimestampedMixin, AbstractBaseModel


class Article(TimestampedMixin, AbstractBaseModel):
    pass
