class Room:
    def __init__(self, rooms):
        self.rooms = rooms

    def construct_room(self):
        hotel_rooms = []
        for room in self.rooms['offers']:
            offer = {}
            offer['price'] = room['price']['total']
            offer['description'] = room['room']['description']['text']
            offer['offerID'] = room['id']
            hotel_rooms.append(offer)
        return hotel_rooms
