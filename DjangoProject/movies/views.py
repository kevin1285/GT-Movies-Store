from django.db.models import Avg
from django.shortcuts import render, redirect
from movies.api_utils import get_popular_movies, get_movie
from .models import Review
from .forms import ReviewForm

def movie_list(request):
    movies = get_popular_movies()
    #print(movies)
    return render(request, "movies/movie_list.html", {"movies":movies})

def movie(request, movie_id):
    movie = get_movie(movie_id)
    if not movie:
        print('movie does not exist') #404 page later?

    reviews = Review.objects.filter(movie_id=movie_id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    form = ReviewForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('users:login')
        form = ReviewForm(request.POST)
        if not form.is_valid(): #validate input
            print('invalid form:', form.errors)
            return
        review = form.save(commit=False)
        review.movie_id = movie_id
        review.user = request.user
        review.save()
        return redirect('movies:movie', movie_id=movie_id) #reload page to show new review
    return render(request, 'movies/movie.html', {
        'movie':movie,
        'reviews':reviews,
        'form':form,
        'average_rating':average_rating,
    })


