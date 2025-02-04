from django.shortcuts import render
from .api_utils import get_popular_movies
def home(request):
    return render(request, 'home.html')

def movie_list(request):
    movies = get_popular_movies()
    print(movies)
    return render(request,"moviesStore/movie_list.html",{"movies":movies})