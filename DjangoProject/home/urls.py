from django.urls import path
from .views import home, about

app_name = 'home'  # This enables namespacing in templates

urlpatterns = [
    path('', home, name='index'),  # Now you can use {% url 'home:index' %}
    path('about/', about, name='about'),  # Now you can use {% url 'home:about' %}
]