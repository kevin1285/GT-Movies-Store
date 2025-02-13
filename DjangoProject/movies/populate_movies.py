import requests
from django.conf import settings
from movies.models import Movie
import random

BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies():
    url = f"{BASE_URL}/movie/popular"
    params = {"api_key": settings.TIMB_API_KEY, "language": "en-US","page":1}
    response = requests.get(url, params=params)
    #print("API Status Code: ", response.status_code)
    if response.status_code == 200:
        data = response.json()
        #print("API Response:", data.get("results", []))
        return data.get("results",[])
    #print("error fetching:", response.text)
    return []

def get_movie(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": settings.TIMB_API_KEY, "language": "en-US","page":1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def generate_movie_price():
    #Generate random movie price ending in .99, .49, or .00 with base [5, 30].
    base_price = random.randint(5, 30)
    decimal_prices = [0.99, 0.49, 0.00]
    return round(base_price + random.choice(decimal_prices), 2)

def store_popular_movies(movies):
    printed = False
    for movie_data in movies:
        movie = get_movie(movie_data["id"])
        if not printed:
            print(movie)
            printed = True
        if not movie:
            print(f"Skipping movie - details not found")
            continue

        genre_names = [genre["name"] for genre in movie["genres"]]

        Movie.objects.update_or_create(
            id=movie["id"],
            defaults={
                "title": movie["title"],
                "overview": movie["overview"],
                "release_date": movie["release_date"],
                "poster_path": movie["poster_path"],
                "price": generate_movie_price(),
                "runtime": movie["runtime"],
                "genres": genre_names,
            },
        )







