from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    poster_path = models.CharField(max_length=255)
    release_date = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    genres = models.JSONField(default=list)
    runtime = models.IntegerField(null=True, blank=True) #runtime in minutes

    def __str__(self):
        return self.title

    def formatted_runtime(self):
        #Formats runtime as H:MM
        hours = self.runtime // 60
        minutes = self.runtime % 60
        if hours > 0 and minutes > 0:
            return f"{hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h"
        return f"{minutes}m"

    def formatted_release_date(self):
        # converts from YYYY-MM-DD to MM-DD-YYYY
        return datetime.strptime(self.release_date, "%Y-%m-%d").strftime("%m-%d-%Y")


class Review(models.Model):
    movie_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE) # if user is deleted, so are its reviews
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1,11)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}-star review by {self.user.username} for movie {self.movie_id}: {self.text}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    movies = models.ManyToManyField(Movie)

    def subtotal(self):
        return sum(movie.price for movie in self.movies.all())
    def tax(self):
        return (Decimal('0.04') * self.subtotal()).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    def total(self):
        return (self.subtotal() + self.tax()).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"Cart {self.id} - User: {self.user.username if self.user else 'Guest'}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    movies = models.ManyToManyField(Movie, through='OrderItem')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Canceled", "Canceled"),
        ],
        default="Pending",
    )

    def __str__(self):
        return f"Order {self.id} - User: {self.user.username if self.user else 'Guest'} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.id} - {self.movie.title} - ${self.price}"
