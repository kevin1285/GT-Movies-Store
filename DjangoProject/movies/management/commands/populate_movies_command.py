from django.core.management.base import BaseCommand
from movies.populate_movies import store_popular_movies, get_popular_movies
class Command(BaseCommand):
    help = "Fetch and store popular movies in the database."

    def handle(self, *args, **kwargs):
        movies = get_popular_movies()
        store_popular_movies(movies)
        self.stdout.write(self.style.SUCCESS("Successfully stored popular movies!"))