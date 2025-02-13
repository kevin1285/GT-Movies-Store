from django.contrib import admin
from movies.models import Movie, Review

# Register your models here.

admin.site.register(Movie)
admin.site.register(Review)