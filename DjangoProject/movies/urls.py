from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    # MOVIES
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_id>/', views.movie, name='movie'),

    # REVIEWS
    path('<int:movie_id>/submit_review/', views.submit_review, name='submit_review'),
    path('<int:review_id>/delete_review/', views.delete_review, name='delete_review'),
    path('<int:review_id>/edit_review/', views.edit_review, name='edit_review'),

    # SHOPPING CART
    path('cart/', views.cart, name='cart'),

]