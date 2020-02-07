import json
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .hotel import Hotel
from .room import Room
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
        try:
            for hotel in search_hotels.data:
                offer = Hotel(hotel).construct_hotel()
                hotel_offers.append(offer)
                response = zip(hotel_offers, search_hotels.data)

            return render(request, 'demo/results.html', {'response': response,
                                                         'origin': origin,
                                                         'departureDate': checkinDate,
                                                         'returnDate': checkoutDate,
                                                         })
        except UnboundLocalError:
            messages.add_message(request, messages.ERROR, 'No results for your search.')
            return render(request, 'demo/demo_form.html', {})
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


def book_hotel(request, offer_id):
    try:
        guests = [{'id': 1, 'name': {'title': 'MR', 'firstName': 'BOB', 'lastName': 'SMITH'},
                   'contact': {'phone': '+33679278416', 'email': 'bob.smith@email.com'}}]

        payments = {'id': 1, 'method': 'creditCard',
                    'card': {'vendorCode': 'VI', 'cardNumber': '4151289722471370', 'expiryDate': '2021-08'}}
        r = amadeus.booking.hotel_bookings.post(offer_id, guests, payments).data
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error.response.body)
        return render(request, 'demo/book_hotel.html', {})
    return render(request, 'demo/book_hotel.html', {'response': r})


def rooms_per_hotel(request, hotel, departureDate, returnDate):
    try:
        rooms = amadeus.shopping.hotel_offers_by_hotel.get(hotelId=hotel,
                                                           checkInDate=departureDate,
                                                           checkOutDate=returnDate,
                                                           paymentPolicy='GUARANTEE').data

        hotel_rooms = Room(rooms).construct_room()
        return render(request, 'demo/rooms_per_hotel.html', {'response': hotel_rooms,
                                                         'amenities': rooms['hotel']['amenities'],
                                                         'name': rooms['hotel']['name'],
                                                         })
    except (TypeError, AttributeError, ResponseError, KeyError) as error:
        messages.add_message(request, messages.ERROR, error)
        return render(request, 'demo/rooms_per_hotel.html', {})

