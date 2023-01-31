import geocoder

class Hotel:
    def __init__(self, hotel):
        self.hotel = hotel

    def construct_hotel(self):
        try:
            offer = {}
            offer['price'] = self.hotel['offers'][0]['price']['total']
            offer['name'] = self.hotel['hotel']['name']
            offer['hotelID'] = self.hotel['hotel']['hotelId']
            address = geocoder.osm(
                [self.hotel['hotel']['latitude'], self.hotel['hotel']['longitude']], 
                method='reverse'
            )
            if address.json.get('houseNumber') is not None:
                offer['address'] = address.json['street'] + ' ' +  address.json['houseNumber']
            elif address.json.get('housenumber') is not None:
                offer['address'] = address.json['street'] + ' ' +  address.json['housenumber']
            else:
                offer['address'] = address.json['street']
        except (TypeError, AttributeError, KeyError):
            pass
        return offer
