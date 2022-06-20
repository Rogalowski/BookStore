"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from books.views import ListBook_View, AddBook_View, EditBook_View, DeleteBook_View, GoogleBooks_View

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books_list/', ListBook_View.as_view(), name="books"),
    path('add_book/', AddBook_View.as_view(), name="add_book"),
    path('books_list/<int:book_id>', EditBook_View.as_view(), name="edit_book"),
    path('delete_book/<int:book_id>',
         DeleteBook_View.as_view(), name="delete_book"),
    path('google/',
         GoogleBooks_View.as_view(), name="google_books"),


    path('', include('books.urls'))
]
