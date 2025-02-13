from django.db import models
from django.contrib.auth.models import User

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

class Review(models.Model):
    movie_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE) # if user is deleted, so are its reviews
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1,11)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}-star review by {self.user.username} for movie {self.movie_id}: {self.text}"


