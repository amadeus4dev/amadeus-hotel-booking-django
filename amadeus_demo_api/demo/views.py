import json
import ast
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .hotel import Hotel
from .room import Room
from .booking import Booking
from django.http import HttpResponse

amadeus = Client()


def demo(request):
    origin = request.POST.get('Origin')
    checkinDate = request.POST.get('Checkindate')
    checkoutDate = request.POST.get('Checkoutdate')

    kwargs = {'cityCode': request.POST.get('Origin'),
              'checkInDate': request.POST.get('Checkindate'),
              'checkOutDate': request.POST.get('Checkoutdate')}

    if origin and checkinDate and checkoutDate:
        try:
            search_hotels = amadeus.shopping.hotel_offers.get(**kwargs)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error.response.body)
            return render(request, 'demo/demo_form.html', {})
        hotel_offers = []
        for hotel in search_hotels.data:
            offer = Hotel(hotel).construct_hotel()
            hotel_offers.append(offer)
            response = zip(hotel_offers, search_hotels.data)

        return render(request, 'demo/results.html', {'response': response,
                                                     'origin': origin,
                                                     'departureDate': checkinDate,
                                                     'returnDate': checkoutDate,
                                                     })
    return render(request, 'demo/demo_form.html', {})


def city_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None), subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_city_list(data), 'application/json')


def get_city_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode']+', '+data[i]['name'])
    result = list(dict.fromkeys(result))
    return json.dumps(result)


def book_hotel(request, hotel):
    try:
        r = amadeus.shopping.hotel_offers_by_hotel.get(hotelId=hotel).data
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error.response.body)
        return render(request, 'demo/book_hotel.html', {})
    return render(request, 'demo/book_hotel.html', {'response': r})


def rooms_per_hotel(request, hotel):
    try:
        rooms = amadeus.shopping.hotel_offers_by_hotel.get(hotelId=hotel).data
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error.response.body)
        return render(request, 'demo/rooms_per_hotel.html', {})
    hotel_rooms = []
    offer = Room(rooms).construct_room()
    hotel_rooms.append(offer)
    return render(request, 'demo/rooms_per_hotel.html', {'response': hotel_rooms,
                                                     'amenities': rooms['hotel']['amenities'],
                                                     'name': rooms['hotel']['name'],
                                                     })
