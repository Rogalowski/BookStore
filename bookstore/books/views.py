from pickle import APPEND
from django.http import HttpResponse, HttpResponseRedirect
# import requests
from django.views.generic.edit import FormView
from webbrowser import get
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
# from html5lib import serialize
import requests
# from requests import request
from .models import Author, Book
from books.forms import AddBook_Form, SearchBook_Form, SearchBookGoogleApi_Form
from django.views.generic import UpdateView, DeleteView
from django.db.models import Q
from django.db.utils import IntegrityError
from rest_framework import viewsets
from .serializers import BookSerializer, AuthorSerializer
from django.contrib import messages


class ListBook_View(View):
    def get(self, request,   *args, **kwargs):
        all_books = Book.objects.all()
        all_authors = Author.objects.all()

        form = SearchBook_Form(request.GET)
        context = {
            'form': form,
            'title': [],
            'author': [],
            'acquired': [],
            'published_year_min': [],
            'published_year_max': [],
        }
        if form.is_valid():
            typed_title = form.cleaned_data['title']
            typed_author = form.cleaned_data['authors']
            typed_year_min = form.cleaned_data['published_year_min']
            typed_year_max = form.cleaned_data['published_year_max']

            if not typed_author and not typed_year_min and not typed_year_max and not typed_title:
                context['all_books'] = all_books
                context['all_authors'] = all_authors
                return render(request, 'books/list_book_view.html', context)

            typed_acquired = form.cleaned_data['acquired']
            if not typed_year_min:
                typed_year_min = 0
            if not typed_year_max:
                typed_year_max = 3000

            filter_title = {'title__icontains': typed_title}
            filter_acquired = {'acquired__exact': typed_acquired}
            filter_year = {'published_year__gte': typed_year_min,
                           'published_year__lte': typed_year_max}

            if not typed_author:
                filtered_books = Book.objects.filter(
                    Q(**filter_title) & Q(**filter_year) & Q(**filter_acquired))
                print(f'filtered_books: {filtered_books}')
                context['filtered_books'] = filtered_books
                return render(request, 'books/list_book_view.html', context)
            else:
                filter_authors = {'authors': typed_author}
                print(f'typed_author IF: {typed_author}')
            filtered_books = Book.objects.filter(
                Q(**filter_title) & Q(**filter_year) & Q(**filter_acquired) & Q(**filter_authors))
            print(f'filtered_books: {filtered_books}')

            context['filtered_books'] = filtered_books
        return render(request, 'books/list_book_view.html', context)


class AddBook_View(View):
    def get(self, request):
        context = {
            'form': AddBook_Form(),
        }
        return render(request, 'books/add_book_view.html', context)

    def post(self, request):
        form = AddBook_Form(request.POST or None)
        context = {
            'form': form,
        }
        if form.is_valid():

            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            print(f"Choosen: {title}")  # Test get title from form, etc below
            print(f"description: {description}")

            authors = form.cleaned_data['authors']
            print(f"authors: {authors}")
            acquired = form.cleaned_data['acquired']
            print(f"acquired: {acquired}")
            published_year = form.cleaned_data['published_year']
            print(f" published_year: {published_year}")
            thumbnail = form.cleaned_data['thumbnail']
            print(f" thumbnail: {thumbnail}")

            # if Room.objects.filter(name=room_name).first():
            # error_name = f"That room exist: {room_name}"
            # return render(request, 'booking_rooms_templates/add_room_html.html', context={'error_name': error_name})

            add_book = Book.objects.create(
                title=title,
                description=description,
                # authors=authors,
                acquired=acquired,
                published_year=published_year,
                thumbnail=thumbnail,
            )
            add_book.authors.add(*authors)

            return redirect('books')

        context = {
            'form': form,
            'result': f"FORM CRASHED, TRY ONE MORE TIME"
        }
        return render(request, 'books/add_book_view.html', context)


class EditBook_View(UpdateView):
    template_name = 'books/add_book_view.html'
    fields = [
        'title',
        'description',
        'authors',
        'published_year',
        'acquired',
        'thumbnail',

    ]

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("book_id")
        return get_object_or_404(Book, id=id_)

    def get_success_url(self):
        return reverse('books')

    def patch(self, request, *args, **kwargs):
        form = AddBook_Form(request.PATCH or None)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            print(f"Choosen: {title}")  # Test get title from form, etc below
            print(f"description: {description}")

            authors = form.cleaned_data['authors']
            print(f"authors: {authors}")
            acquired = form.cleaned_data['acquired']
            print(f"acquired: {acquired}")
            published_year = form.cleaned_data['published_year']
            print(f" published_year: {published_year}")
            thumbnail = form.cleaned_data['thumbnail']
            print(f" thumbnail: {thumbnail}")

            # Book update fields
            book_update = Book.objects.get(id=kwargs['book_id'])
            book_update.title = title
            book_update.description = description
            book_update.acquired = acquired
            book_update.published_year = published_year
            book_update.thumbnail = thumbnail

            # Book save updated fields to database
            book_update.save()

            book_update.authors.set(authors)

            return redirect('books')

        context = {
            'form': form,
            'result': f"FORM CRASHED, TRY ONE MORE TIME"
        }
        return render(request, 'books/edit_book_view.html', context)


class DeleteBook_View(DeleteView):

    template_name = 'books/book_confirm_delete.html'
    model = Book

    def get_success_url(self):
        return reverse('books')

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('book_id')
        return get_object_or_404(Book, id=id_)


class GoogleBooks_View(View):

    # form_class = SearchBookGoogleApi_Form

    template_name = 'books/list_book_api_view.html'

    # def search(self, title_book_api, authors_book_api):
    def search(self, request, title_book_api):
        # googleapikey = ""
        # params = {'q': value, 'key': googleapikey}
        params = {'q': title_book_api}
        google_books = requests.get(
            url=f'https://www.googleapis.com/books/v1/volumes', params=params)
        # url=f'https://www.googleapis.com/books/v1/volumes?q={title_book_api}+inauthor:{authors_book_api}&maxResults=5')

        books_json = google_books.json()
        # print(f'books_json: ', books_json)
        print('BOOKS JSON: ', books_json)
        try:

            bookshelf = books_json['items']
        except KeyError:
            messages.add_message(request, messages.INFO,
                                 f'LOOKS LIKE, NOT FOUND BOOKS')
            return reverse_lazy('google_books')
        return bookshelf

    def get(self, request, *args, **kwargs):

        form = SearchBookGoogleApi_Form(request.GET or None)
        if form.is_valid():
            title_book_api = form.cleaned_data['q']
            # authors_book_api = form.cleaned_data['authors']
            # books = self.search(title_book_api, authors_book_api)
            books = self.search(request, title_book_api)
            # print(f'BOOKS: ', {books})
            context = {
                'books': books,
                'form': form,
            }
            return render(request, self.template_name, context)
        return render(request, self.template_name, {'form': form})

    def add_books_to_library(self, request, bookshelf):
        loop_number = 0
        for item in bookshelf:
            loop_number += 1
            try:
                external_id = item['id']
            except TypeError:
                messages.add_message(request, messages.INFO,
                                     f'NO IMPORTED BOOKS.')
                return reverse_lazy('google_books')

            title = item['volumeInfo']['title']
            try:
                authors_temp = item['volumeInfo']['authors']
            except KeyError:
                authors_temp = ['']
            try:
                published_year = item['volumeInfo']['publishedDate'][:4]
            except KeyError:
                published_year = 0
            acquired = False
            try:
                thumbnail = item['volumeInfo']['imageLinks']['thumbnail']
            except KeyError:
                thumbnail = f'https://www.buckinghambooks.com/static/basic_cms_store2/img/CoverNotFound2.jpg'

            print(" authors_temp ", authors_temp)

            try:
                description = item['volumeInfo']['subtitle']
            except KeyError:
                description = ""

            try:
                for author in authors_temp:
                    add_authors_to_model = Author.objects.get_or_create(
                        name=author
                    )
            except IntegrityError:
                pass
            # book_update = Book.objects.get(id=kwargs['book_id'])
            authors_filtered_book = Author.objects.filter(
                name__in=[*authors_temp])

            if Book.objects.filter(external_id=external_id).exists():
                loop_number -= 1
                import_book = Book.objects.get(external_id=external_id)
                import_book.title = title
                import_book.description = description
                import_book.published_year = published_year
                import_book.acquired = acquired
                import_book.thumbnail = thumbnail
                import_book.save()
                import_book.authors.set(authors_filtered_book)
            else:
                import_book = Book.objects.create(
                    external_id=external_id,
                    title=title,
                    description=description,
                    published_year=published_year,
                    acquired=acquired,
                    thumbnail=thumbnail,

                )
                import_book.authors.add(*authors_filtered_book)
            # import_book.title = title,
            # import_book.description = description,
            # import_book.published_year = published_year,
            # import_book.acquired = acquired,
            # import_book.thumbnail = thumbnail
            # import_book.save()
            # import_book = Book.objects.create(
            #     external_id=external_id,
            #     title=title,
            #     description=description,
            #     published_year=published_year,
            #     acquired=acquired,
            #     thumbnail=thumbnail
            # )

            # import_book.authors.add(*authors_filtered_book)

        messages.add_message(request, messages.INFO,
                             f'YOU HAVE  IMPORTED {loop_number} BOOKS.')
        print("COUNT: ", loop_number)

    def post(self,  request,  *args, **kwargs):
        form = SearchBookGoogleApi_Form(request.POST or None)
        if form.is_valid():
            #     title_book_api = form.cleaned_data['title']
            #     books = self.search(title_book_api)
            # for book in books:
            # print(f'BOOK: ', book.id)
            # print(f'books:  ', books)
            # for book in books:
            # print(f'BOOK: ', book['volumeInfo']['title'])
            title_book_api = form.cleaned_data['q']
            # authors_book_api = form.cleaned_data['authors']
            # books = self.search(title_book_api, authors_book_api)
            books = self.search(request, title_book_api)
            self.add_books_to_library(request, books)

            return HttpResponseRedirect(reverse_lazy('books'))
        # context = {
        # 'books': books,
        # }
        # return render(request, self.template_name, context)
        # return HttpResponseRedirect(reverse_lazy('google_books'))

        return reverse_lazy('google_books')


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
