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
            # Hotel List
            hotel_list = amadeus.reference_data.locations.hotels.by_city.get(cityCode=origin)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error.response.body)
            return render(request, 'demo/demo_form.html', {})
        hotel_offers = []
        hotel_ids = []
        for i in hotel_list.data:
            hotel_ids.append(i['hotelId'])
        num_hotels = 40
        kwargs = {'hotelIds': hotel_ids[0:num_hotels],
            'checkInDate': request.POST.get('Checkindate'),
            'checkOutDate': request.POST.get('Checkoutdate')}
        try:
            # Hotel Search
            search_hotels = amadeus.shopping.hotel_offers_search.get(**kwargs)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error.response.body)
            return render(request, 'demo/demo_form.html', {})
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
            messages.add_message(request, messages.ERROR, 'No hotels found.')
            return render(request, 'demo/demo_form.html', {})
    return render(request, 'demo/demo_form.html', {})


def rooms_per_hotel(request, hotel, departureDate, returnDate):
    try:
        # Search for rooms in a given hotel
        rooms = amadeus.shopping.hotel_offers_search.get(hotelIds=hotel,
                                                           checkInDate=departureDate,
                                                           checkOutDate=returnDate).data
        hotel_rooms = Room(rooms).construct_room()
        return render(request, 'demo/rooms_per_hotel.html', {'response': hotel_rooms,
                                                             'name': rooms[0]['hotel']['name'],
                                                             })
    except (TypeError, AttributeError, ResponseError, KeyError) as error:
        messages.add_message(request, messages.ERROR, error)
        return render(request, 'demo/rooms_per_hotel.html', {})


def book_hotel(request, offer_id):
    try:
        offer_availability = amadeus.shopping.hotel_offer_search(offer_id).get()
        if offer_availability.status_code == 200:
            guests = [{'id': 1, 'name': {'title': 'MR', 'firstName': 'BOB', 'lastName': 'SMITH'},
                       'contact': {'phone': '+33679278416', 'email': 'bob.smith@email.com'}}]

            payments = {'id': 1, 'method': 'creditCard',
                        'card': {'vendorCode': 'VI', 'cardNumber': '4151289722471370', 'expiryDate': '2021-08'}}
            booking = amadeus.booking.hotel_bookings.post(offer_id, guests, payments).data
        else:
            return render(request, 'demo/booking.html', {'response': 'The room is not available'})
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error.response.body)
        return render(request, 'demo/booking.html', {})
    return render(request, 'demo/booking.html', {'id': booking[0]['id'],
                                                 'providerConfirmationId': booking[0]['providerConfirmationId']
                                                 })


def city_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None),
                                                        subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error.response.body)
    return HttpResponse(get_city_list(data), 'application/json')


def get_city_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode'] + ', ' + data[i]['name'])
    result = list(dict.fromkeys(result))
    return json.dumps(result)
