class Room:
    def __init__(self, room):
        self.room = room

    def construct_room(self):
        offer = {}
        index = 0
        for r in self.room:
            offer['id'] = self.room['offers'][index]['id']
            offer['price'] = self.room['offers'][index]['price']['total']
            offer['description'] = self.room['offers'][index]['room']['description']['text']
            index += 1
        return offer
