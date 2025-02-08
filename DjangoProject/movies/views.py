from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from movies.api_utils import get_popular_movies


def movie_list(request):
    movies = get_popular_movies()
    print(movies)
    return render(request, "movies/movie_list.html", {"movies":movies})


def home(request):
    return render(request, 'home/home.html')#change redirect



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:index')  # Redirect after successful login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'movies/login.html')


def logout_view(request):
    logout(request)
    return redirect('movies:login')  # Redirect to login page after logout

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('movies:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('movies:signup')

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)  # Automatically log in after signing up
        return redirect('home:movie_list')  # Redirect to home page

    return render(request, 'movies/signup.html')