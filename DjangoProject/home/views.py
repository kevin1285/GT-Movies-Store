from django.shortcuts import render
from .api_utils import get_popular_movies

def home(request):
    return render(request, 'home/home.html')

def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})

def movie_list(request):
    movies = get_popular_movies()
    print(movies)
    return render(request,"home/movie_list.html",{"movies":movies})

