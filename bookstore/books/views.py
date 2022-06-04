from webbrowser import get
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Author, Book
from books.forms import AddBook_Form

# Create your views here.


class ListBook_View(View):
    def get(self, request,   *args, **kwargs):
        all_books = Book.objects.all()
        all_authors = Author.objects.all()

        context = {
            'all_books': all_books,
            'all_authors': all_authors,
        }
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

            return redirect('')

        context = {
            'form': form,
            'result': f"FORM CRASHED, TRY ONE MORE TIME"
        }
        return render(request, 'books/add_book_view.html', context)


class EditBook_View(View):
    def get(self, request):
        pass
