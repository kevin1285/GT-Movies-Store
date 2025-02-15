from urllib.parse import urlencode

from django.contrib.auth import user_logged_in
from django.db.models import Avg
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Movie, Review, Cart, Order, OrderItem
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
        login_url = reverse("users:login")
        return HttpResponseRedirect(f"{login_url}?{urlencode({'next': 'movies:movie/movie_id'})}")
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
def get_or_create_cart(request):
    #Retrieve the user's cart or create one if it doesn't exist.
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
        else:
            cart = Cart.objects.create()
            request.session["cart_id"] = cart.id  # Save guest cart ID
    return cart

def cart(request):
    cart = get_or_create_cart(request)
    return render(request, "movies/cart.html", {"cart": cart, "movies": cart.movies.all()})

def add_to_cart(request, movie_id):
    cart = get_or_create_cart(request)
    movie = get_object_or_404(Movie, id=movie_id)
    cart.movies.add(movie)
    return redirect('movies:cart')

def remove_from_cart(request, movie_id):
    cart = get_or_create_cart(request)
    if cart:
        cart.movies.remove(movie_id)
    return redirect('movies:cart')

@receiver(user_logged_in)
def merge_guest_cart(request, user, **kwargs):
    session_cart_id = request.session.get("cart_id")
    if session_cart_id:
        try:
            guest_cart = Cart.objects.get(id=session_cart_id)
            user_cart, _ = Cart.objects.get_or_create(user=user)

            # Merge guest cart into user cart
            for movie in guest_cart.movies.all():
                user_cart.movies.add(movie)

            # Delete guest cart and remove session key
            guest_cart.delete()
            del request.session["cart_id"]

        except Cart.DoesNotExist:
            print("CART DOES NOT EXIST")

# CHECKOUT:
def checkout(request):
    if not request.user.is_authenticated:
        login_url = reverse("users:login")
        return HttpResponseRedirect(f"{login_url}?{urlencode({'next': request.path})}")
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.movies.exists():
        return redirect('movies:cart')  # no checkout if empty cart

    return render(request, "movies/checkout.html", {
        "cart": cart,
        "subtotal": cart.subtotal(),
        "tax": cart.tax(),
        "total": cart.total(),
    })


def place_order(request):
    if not request.user.is_authenticated:
        login_url = reverse("users:login")
        return HttpResponseRedirect(f"{login_url}?{urlencode({'next': request.path})}")
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(
        user=request.user,
        subtotal=cart.subtotal(),
        tax=cart.tax(),
        total=cart.total()
    )
    for movie in cart.movies.all():
        OrderItem.objects.create(order=order, movie=movie, price=movie.price)
    cart.movies.clear()
    return redirect("movies:order_confirmation")

def order_confirmation(request):
    return render(request, "movies/order_confirmation.html")

def orders(request):
    if not request.user.is_authenticated:
        login_url = reverse("users:login")
        return HttpResponseRedirect(f"{login_url}?{urlencode({'next': request.path})}")
    user_orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "movies/orders.html", {"orders": user_orders})

def order_detail(request, order_id):
    if not request.user.is_authenticated:
        login_url = reverse("users:login")
        return HttpResponseRedirect(f"{login_url}?{urlencode({'next': request.path})}")

    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    return render(request, "movies/order_detail.html", {
        "order": order,
        "order_items": order_items,
    })