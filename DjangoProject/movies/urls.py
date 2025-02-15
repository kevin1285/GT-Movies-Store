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
    path('cart/add/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:movie_id>/', views.remove_from_cart, name='remove_from_cart'),

    # CHECKOUT
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),

    # ORDERS
    path("orders/", views.orders, name="orders"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),

]