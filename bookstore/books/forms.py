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
    acquired = forms.BooleanField(label='acquired', required=False)
    published_year_min = forms.IntegerField(
        label='Year, min', required=False)
    published_year_max = forms.IntegerField(label='max', required=False)

    class Meta:
        model = Book
        fields = (
            'title',
            'authors',
            'acquired',
            # 'published_year',
            'published_year_min',
            'published_year_max',
        )
        labels = {
            "title": "Search by title/status",
        }
