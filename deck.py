import random
import card


class Deck:

    def __init__(self):
        self.cards = []
        self.discards = []
        self.last_straight_bottom_card = None
        for suit in ['H', 'S', 'C', 'D']:
            for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
                self.cards.append(card.Card(suit, rank))
        self.cards.append(card.Card('J', ''))
        self.cards.append(card.Card('J', ''))
        self.shuffle()
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def discard(self, cards):
        self.last_straight_bottom_card = None
        if isinstance(cards, list):
            if self.is_straight(cards):
                self.last_straight_bottom_card = cards[0]
            for card in cards:
                self.discards.append(card)
        else:
            self.discards.append(cards)

    def get_top_discard(self):
        return self.discards[-1]

    def get_last_straight_bottom_card(self):
        return self.last_straight_bottom_card

    def draw_last_straight_bottom_card(self):
        for i in range(len(self.discards) - 3, -1, -1):
            if self.discards[i] is self.last_straight_bottom_card:
                del self.discards[i]
        card = self.last_straight_bottom_card
        self.last_straight_bottom_card = None
        return card

    def get_top_card(self):
        return self.cards[-1]

    def draw_top_discard(self):
        return self.discards.pop()
        
    def draw_top_card(self):
        if len(self.cards) == 1:
            last_card = self.cards.pop()
            self.remake_deck()
            return last_card
        return self.cards.pop()
        
    def remake_deck(self):
        top_discard = self.draw_top_discard()
        self.cards = self.discards
        self.discards = []
        self.shuffle()
        self.discards.append(top_discard)

    def get_cards_available(self):
        available = [self.get_top_discard()]
        if self.last_straight_bottom_card is not None:
            available.append(self.last_straight_bottom_card)
        return available

    @staticmethod
    def is_straight(cards):
        if len(cards) >= 3:
            suit = None
            for card in cards:
                if card.suit != 'J':
                    if suit is None:
                        suit = card.suit
                        continue
                    if card.suit != suit:
                        return False
            return True
        return False

    def reset(self):
        self.__init__()


if __name__ == '__main__':
    d = Deck()
    print(d.draw_top_card())
