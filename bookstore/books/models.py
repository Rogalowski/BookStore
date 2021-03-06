from django.db import models
from shortuuidfield import ShortUUIDField
import uuid
import shortuuid


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name},'


class Book(models.Model):
    external_id = ShortUUIDField(
        max_length=10, default=None, blank=True, null=True
        # primary_key=True,
    )
    # external_id = models.UUIDField(
    #     default=uuid.uuid4,
    #     editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    authors = models.ManyToManyField(Author)
    published_year = models.SmallIntegerField(default=0)
    acquired = models.BooleanField(default=False)
    thumbnail = models.TextField(
        max_length=2048, default=None, blank=True, null=True)
