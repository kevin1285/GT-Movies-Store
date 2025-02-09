from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    movie_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE) # if user is deleted, so are its reviews
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1,11)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}-star review by {self.user.username} for movie {self.movie_id}: {self.text}"


