from django.contrib import admin
from .models import Book
from .models import Author
# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
