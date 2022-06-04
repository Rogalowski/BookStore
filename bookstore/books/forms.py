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
