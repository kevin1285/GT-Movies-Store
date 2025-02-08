from django.urls import path

from . import views
from .views import login_view, logout_view, signup_view

app_name = 'movies'
urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    #path('', home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

]