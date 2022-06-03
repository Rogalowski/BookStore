from django.shortcuts import render
from django.views import View
from .models import Author, Book

# Create your views here.


class List_Book(View):
    def get(self, request):
        all_books = Book.objects.all()
        all_authors = Author.objects.all()

        context = {
            'all_books': all_books,
            'all_authors': all_authors,
        }
        return render(request, 'books/list_book_view.html', context)


class Add_Book(View):
    pass
