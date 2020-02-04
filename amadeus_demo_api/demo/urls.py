from django.urls import path

from . import views

urlpatterns = [
    path('', views.demo, name='demo_form'),
    path('city_search/', views.city_search, name='city_search'),
    path('book_hotel/<str:offer_id>', views.book_hotel, name='book_hotel'),
    path('rooms_per_hotel/<str:hotel>/<str:departureDate>/<str:returnDate>', views.rooms_per_hotel, name='rooms_per_hotel')
]
