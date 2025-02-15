from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from .forms import ReviewForm

# MOVIES
def movie_list(request):
    movies = Movie.objects.all()
    #print(movies)
    return render(request, "movies/movie_list.html", {"movies":movies})

def movie(request, movie_id):
    movie = Movie.objects.filter(id=movie_id).first()
    if not movie:
        print('movie does not exist') #404 page later?

    reviews = Review.objects.filter(movie_id=movie_id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    """movie_genres = []
    for genre in movie['genres']:
        movie_genres.append(genre['name'])"""


    return render(request, 'movies/movie.html', {
        'movie':movie,
        'reviews':reviews,
        'form':ReviewForm(),
        'average_rating':average_rating,
        'star_range':range(1,11),
    })

# REVIEWS
def submit_review(request, movie_id):
    form = ReviewForm(request.POST)
    if not request.user.is_authenticated:
        return redirect('users:login')
    form = ReviewForm(request.POST)
    if not form.is_valid():  # validate input
        print('invalid form:', form.errors)
        return
    review = form.save(commit=False)
    review.movie_id = movie_id
    review.user = request.user
    review.save()
    return redirect('movies:movie', movie_id=movie_id)

def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies:movie', movie_id=review.movie_id)

    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        form.save()
    return redirect('movies:movie', movie_id=review.movie_id)

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
    return redirect('movies:movie', movie_id=review.movie_id)

# SHOPPING CART
def cart(request):
    return render(request, 'movies/cart.html')
    



