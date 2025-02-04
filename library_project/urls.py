from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from books.views import register_user, login_page, recommend_books_by_favorites
def logout_view(request):
    logout(request) 
    return redirect('/login/') 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('books.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_user, name='register_user'),
    path('login/', login_page, name='login_page'), 
    path('logout/', logout_view, name='logout'),
    path('recommendations/', recommend_books_by_favorites, name='recommend_books_by_favorites'),

]
