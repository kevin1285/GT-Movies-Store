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


