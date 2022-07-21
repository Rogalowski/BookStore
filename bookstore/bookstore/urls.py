
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static  # static ROOT import
from django.conf import settings  # static ROOT import
from django.urls import re_path  # static ROOT import
from django.views.static import serve
from books.views import ListBook_View, AddBook_View, EditBook_View, DeleteBook_View, GoogleBooks_View

"""Client URLs and API URLs"""

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('books_list/', ListBook_View.as_view(), name="books"),
    path('add_book/', AddBook_View.as_view(), name="add_book"),
    path('books_list/<int:book_id>', EditBook_View.as_view(), name="edit_book"),
    path('delete_book/<int:book_id>',
         DeleteBook_View.as_view(), name="delete_book"),
    path('google/',
         GoogleBooks_View.as_view(), name="google_books"),


    path('', include('books.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
