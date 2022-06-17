from rest_framework import routers, serializers
from .models import Book, Author


class BookSerializer(serializers.HyperlinkedRelatedField):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description']


class AuthorSerializer(serializers.ModelSerializer):
    authors = serializers.HyperlinkedModelSerializer(

    )
