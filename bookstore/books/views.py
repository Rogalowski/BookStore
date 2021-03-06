from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
import requests
from .models import Author, Book
from books.forms import AddBook_Form, SearchBook_Form, SearchBookGoogleApi_Form
from django.views.generic import UpdateView, DeleteView
from django.db.models import Q
from django.db.utils import IntegrityError
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import BookSerializer, AuthorSerializer
from django.contrib import messages


"""
Listing all books from database with GUI for client
"""


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

        """Search Form for Books"""

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

        """ Add Form of new Book"""


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

            add_book = Book.objects.create(
                title=title,
                description=description,
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

        """Edit Form for Book """


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

    """Get Books from Google API"""


class GoogleBooks_View(View):
    template_name = 'books/list_book_api_view.html'

    # def search(self, title_book_api, authors_book_api):
    def search(self, request, title_book_api):
        # googleapikey = ""
        # params = {'q': value, 'key': googleapikey}
        params = {'q': title_book_api}
        google_books = requests.get(
            url=f'https://www.googleapis.com/books/v1/volumes', params=params)
        # url=f'https://www.googleapis.com/books/v1/volumes?q={title_book_api}+inauthor:{authors_book_api}&maxResults=5')

        books_json = google_books.json()  # get books in JSON

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

            """ It will create authors in database that are not exists in database before importing new books"""
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
            """If book already exsist will it update, else create new entry"""
            if Book.objects.filter(external_id=external_id).exists():
                loop_number -= 1  # count of imported books
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

        messages.add_message(request, messages.INFO,
                             f'YOU HAVE  IMPORTED {loop_number} BOOKS.')
        print("COUNT: ", loop_number)

    def post(self,  request,  *args, **kwargs):
        form = SearchBookGoogleApi_Form(request.POST or None)
        if form.is_valid():

            title_book_api = form.cleaned_data['q']

            books = self.search(request, title_book_api)
            self.add_books_to_library(request, books)

            return HttpResponseRedirect(reverse_lazy('books'))

        return reverse_lazy('google_books')

    """Api Books with Searching, GET, POST, DELETE, PATCH methods"""


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):

        typed_title = self.request.query_params.get('title')
        typed_authors = self.request.query_params.get('author')
        typed_year_min = self.request.query_params.get('from')
        typed_year_max = self.request.query_params.get('to')

        if not self.request.query_params.get('title'):
            typed_title = " "
        if not self.request.query_params.get('from'):
            typed_year_min = 0
        if not self.request.query_params.get('to'):
            typed_year_max = 10000
        if not self.request.query_params.get('author'):
            typed_authors = ""

        filter_title = {'title__icontains': typed_title.replace('"', "")}
        filter_authors = {
            'authors__name__icontains': typed_authors.replace('"', "")}

        filter_year = {'published_year__gte': typed_year_min,
                       'published_year__lte': typed_year_max}

        if not self.request.query_params.get('acquired'):
            filtered_books = Book.objects.filter(
                Q(**filter_authors) &
                Q(**filter_title) & Q(**filter_year))
            return filtered_books

        if self.request.query_params.get('acquired') == 'false':
            typed_acquired = False
        elif self.request.query_params.get('acquired') == 'true':
            typed_acquired = True

        filter_acquired = {'acquired__exact': typed_acquired}

        filtered_books = Book.objects.filter(
            Q(**filter_authors) &
            Q(**filter_title) & Q(**filter_year) & Q(**filter_acquired))
        return filtered_books

    # def retrieve(self, request, *args, **kwargs):
    #     params = kwargs
    #     if kwargs['pk']:
    #         print("HAHAHH")
    #         print(args)
    #     a = self.request.GET.get('name')
    #     print("params:", request.GET.get('pk='))
    #     filter_title = {'title__icontains': params['pk']}

    #     books_retrieve = Book.objects.filter(acquired=False)

    #     serializer = BookSerializer(books_retrieve, many=True)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data

        new_book = Book.objects.create(
            title=data['title'],
            # description=data['description'],
            published_year=data['published_year'],
            acquired=data['acquired'],
            thumbnail=data['thumbnail'],

        )
        new_book.save()

        for author in data['authors']:
            author_obj = Author.objects.get(name=author['name'])
            new_book.authors.add(author_obj)

        serializer = BookSerializer(new_book)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        book.delete()

        return Response({"message": "Book has been deleted"})

    def put(self, request, *args, **kwargs):
        book_object = Book.objects.get()

        data = request.data
        book_object.title = data["title"]
        book_object.description = data["description"]
        book_object.acquired = data["acquired"]
        book_object.published_year = data["published_year"]
        book_object.thumbnail = data["thumbnail"]

        book_object.save()

        for author in data['authors']:
            author_obj = Author.objects.get(name=author['name'])
            book_object.authors.set(author_obj)

        serializer = BookSerializer(book_object)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        book_object = Book.objects.get()
        data = request.data

        book_object.title = data.get("title", book_object.title)
        book_object.title = data.get("description", book_object.description)
        book_object.title = data.get("acquired", book_object.acquired)
        book_object.title = data.get(
            "published_year", book_object.published_year)
        book_object.title = data.get("thumbnail", book_object.thumbnail)

        book_object.authors.set(**data['authors']['name'])
        book_object.save()
        serializer = BookSerializer(book_object)
        return Response(serializer.data)


"""API Authors model"""


class AuthorViewSet(viewsets.ModelViewSet):
    pass
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer


"""API Specyfication response"""


class APISpecViewSet(viewsets.ViewSet):
    queryset = Author.objects.all()

    def list(self, request, *args, **kwargs):
        return Response({"info": {"version": "2022.06.21"}})
