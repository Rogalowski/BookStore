from rest_framework import routers
from .views import BookViewSet, AuthorViewSet, APISpecViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'api_spec', APISpecViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),


]
