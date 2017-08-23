class Card:

    def __init__(self, suit, rank):
        if not self.validate(suit, rank):
            print('Card instantiation failed validation.')
            return
        self.suit = suit
        self.rank = rank
        self.value = self.get_value(rank)
        self.order = self.get_order(rank)

    @staticmethod
    def validate(suit, rank):
        if suit in ['H', 'S', 'C', 'D']:
            if rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
                return True
        if suit in ['J'] and rank in ['']:
            return True
        return False

    @staticmethod
    def get_value(rank):
        value_table = {'': 0, 'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                       '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10,
                       'Q': 10, 'K': 10}
        return value_table[rank]

    @staticmethod
    def get_order(rank):
        order_table = {'': 0, 'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                       '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11,
                       'Q': 12, 'K': 13}
        return order_table[rank]

    def __str__(self):
        return self.suit + self.rank

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __ne__(self, other):
        return self.suit != other.suit or self.rank != other.rank