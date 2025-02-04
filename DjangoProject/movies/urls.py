from django.urls import path

from . import views
from .views import login_view, logout_view, signup_view

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='movies.index'),
    #path('', home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
]