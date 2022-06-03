from webbrowser import get
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Author, Book
from books.forms import AddBookForm

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
    def get(self, request):
        context = {
            'form': AddBookForm(),
        }
        return render(request, 'books/add_book_view.html', context)

    def post(self, request):
        form = AddBookForm(request.POST or None)
        context = {
            'form': form,
        }
        if form.is_valid():
            # get provided title by user from
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
                # authors=authors,
                acquired=acquired,
                published_year=published_year,
                thumbnail=thumbnail,
            )
            add_book.authors.add(
                # *Author.objects.
                *Author.objects.filter(id=authors.id)
            )

            return redirect('')

        context = {
            'form': form,
            'result': f"FORM CRUSHED, TRY ONE MORE TIME"
        }
        return render(request, 'books/add_book_view.html', context)
