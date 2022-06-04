from webbrowser import get
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from .models import Author, Book
from books.forms import AddBook_Form
from django.views.generic import UpdateView, DeleteView
# Create your views here.


class ListBook_View(View):
    def get(self, request,   *args, **kwargs):
        # book = Book.objects.get(id=kwargs['book_id'])
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
        return reverse('')

    def post(self, request, *args, **kwargs):
        form = AddBook_Form(request.POST or None)

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

            return redirect('')

        context = {
            'form': form,
            'result': f"FORM CRASHED, TRY ONE MORE TIME"
        }
        return render(request, 'books/add_book_view.html', context)


class DeleteBook_View(DeleteView):

    template_name = 'books/book_confirm_delete.html'
    model = Book

    def get_success_url(self):
        return reverse('')

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('book_id')
        return get_object_or_404(Book, id=id_)
