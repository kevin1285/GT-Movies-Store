from django.contrib import admin
from movies.models import Movie, Review, Cart, Order

# Register your models here.

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Order)