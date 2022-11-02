class Hotel:
    def __init__(self, hotel):
        self.hotel = hotel

    def construct_hotel(self):
        try:
            offer = {}
            offer['price'] = self.hotel['offers'][0]['price']['total']
            offer['name'] = self.hotel['hotel']['name']
            offer['hotelID'] = self.hotel['hotel']['hotelId']
            offer['description'] = self.hotel['hotel']['description']['text']
        except (TypeError, AttributeError, KeyError):
            pass
        return offer
