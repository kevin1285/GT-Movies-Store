from django.urls import path
from . import views
from .views import movie_list
from .views import home, about

app_name = 'home'  # This enables namespacing in templates

urlpatterns = [
    path('home/', views.movie_list, name='movie_list'),

    path("", home, name='index'),
    path("about/", about, name='about'),
    # path('home/', views.home, name='home'),
    # path('about/', views.about, name='about'),
]