from django.urls import path
from . import views
from .views import home, about

app_name = 'home'  # This enables namespacing in templates

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
]