from django.db import models
from shortuuidfield import ShortUUIDField
import uuid
import shortuuid


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name},'


class Book(models.Model):
    external_id = ShortUUIDField(
        max_length=5,
        primary_key=False,
    )

    # external_id = models.UUIDField(
    #     default=uuid.uuid4,
    #     editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()
    authors = models.ManyToManyField(Author)
    published_year = models.SmallIntegerField(default=0)
    acquired = models.BooleanField()
    thumbnail = models.TextField(max_length=2048)
