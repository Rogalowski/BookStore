from rest_framework import routers, serializers
from .models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    # authors = AuthorSerializer(required=False, many=True)
    authors = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Book
        fields = ['id', 'external_id', 'title',
                  'published_year', 'acquired', 'thumbnail', 'authors']
        depth = 1

    @staticmethod
    def get_authors(obj):
        return AuthorSerializer(obj.authors.all(), many=True).data
