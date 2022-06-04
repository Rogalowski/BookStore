from django.forms import ModelForm
from django import forms
from books.models import Author, Book
from django.forms import ModelForm


class AddBook_Form(ModelForm):

    class Meta:
        model = Book
        fields = (
            'title',
            'description',
            'authors',
            'published_year',
            'acquired',
            'thumbnail',

        )
        # widgets = {'status': forms.HiddenInput()}
        exclude = ('external_id',)


class SearchBook_Form(ModelForm):
    title = forms.CharField(label='Search by: title', required=False)
    authors = forms.ModelChoiceField(
        queryset=Author.objects.all(), required=False)
    # authors = forms.CharField(required=False)
    # publication_year =
    acquired = forms.BooleanField(label='acquired', required=False)

    class Meta:
        model = Book
        fields = (
            'title',
            'authors',
            'acquired',
        )
        labels = {
            "title": "Search by title/status",
        }
