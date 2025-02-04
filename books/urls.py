from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, SeriesViewSet
from .views import add_to_favorites, remove_from_favorites
from .views import login_page

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'series', SeriesViewSet)  

urlpatterns = [
    path('', include(router.urls)),
]


urlpatterns += [
    path('books/<int:book_id>/favorite/', add_to_favorites, name='add_to_favorites'),
    path('books/<int:book_id>/unfavorite/', remove_from_favorites, name='remove_from_favorites'),
    path('login/', login_page, name='login_page'),
]