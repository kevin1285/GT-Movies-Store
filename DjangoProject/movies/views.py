from django.shortcuts import render
from movies.api_utils import get_popular_movies, get_movie

def movie_list(request):
    movies = get_popular_movies()
    print(movies)
    return render(request, "movies/movie_list.html", {"movies":movies})

def movie(request, movie_id):
    movie = get_movie(movie_id)
    return render(request, "movies/movie.html", {"movie":movie})


