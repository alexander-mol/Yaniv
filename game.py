class Game:
    def __init__(self, deck, player_list):
        self.deck = deck
        self.player_list = player_list
        self.round_counter = 0
        self.assafed = False

    def get_top_discard(self):
        return self.deck.get_top_discard()

    def get_top_card(self):
        return self.deck.get_top_card()

    def get_num_cards_players(self):
        num_cards = []
        for player in self.player_list:
            num_cards.append(len(player.hand))
        return num_cards
