import requests
from django.conf import settings

BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies():
    url = f"{BASE_URL}/movie/popular"
    params = {"api_key": settings.TIMB_API_KEY, "language": "en-US","page":1}
    response = requests.get(url, params=params)
    print("API Status Code: ", response.status_code)
    if response.status_code == 200:
        data = response.json()
        print("API Response:", data)
        return data.get("results",[])
    print("error fetching:", response.text)
    return []