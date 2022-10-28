class Room:
    def __init__(self, rooms):
        self.rooms = rooms

    def construct_room(self):
        hotel_rooms = []
        try:
            for room in self.rooms[0]['offers']:
                offer = {}
                offer['price'] = room['price']['total']
                offer['description'] = room['room']['description']['text']
                offer['offerID'] = room['id']
                hotel_rooms.append(offer)
        except (TypeError, AttributeError, KeyError):
            pass
        return hotel_rooms