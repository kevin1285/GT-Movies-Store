from django.urls import path
from . import views

app_name = 'home'  # This enables namespacing in templates

urlpatterns = [
    path("", views.home, name='index'),
    path("about/", views.about, name='about'),
    # path('home/', views.home, name='home'),
    # path('about/', views.about, name='about'),
]