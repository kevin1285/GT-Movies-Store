from django.shortcuts import render
from movies.api_utils import get_popular_movies


def movie_list(request):
    movies = get_popular_movies()
    print(movies)
    return render(request, "movies/movie_list.html", {"movies":movies})


