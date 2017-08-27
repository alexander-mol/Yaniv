class BasePlayer:

    def __init__(self, id):
        self.id = id
        self.hand = []

    def get_hand_value(self):
        value = 0
        for card in self.hand:
            value += card.value
        return value

    def decide_call_yaniv(self, game):
        if self.get_hand_value() <= 7:
            return True
        return False

    def decide_cards_to_discard(self, game):
        discardable_sets = self.get_discardable_sets()
        discardable_sets.sort(key=lambda x: -sum([y.value for y in x]))
        return discardable_sets[0]

    def decide_card_to_draw(self, game, cutoff=4):
        cards_available = [game.get_top_discard()]
        if game.deck.get_last_straight_bottom_card() is not None:
            cards_available.append(game.deck.get_last_straight_bottom_card())

        cards_available.sort(key=lambda x: x.value)
        if cards_available[0].value <= cutoff:
            card_to_draw = cards_available[0]
            if card_to_draw.value < sum([c.value for c in self.decide_cards_to_discard(game)]):
                if card_to_draw is game.get_top_discard():
                    return 'discard pile', card_to_draw
                else:
                    return 'start of previous straight in discard pile', card_to_draw
        return 'unseen pile', game.get_top_card()

    def get_high_card(self):
        self.hand.sort(key=lambda x: -x.value)
        return self.hand[0]

    def extract_cards(self, cards):
        if isinstance(cards, list):
            for card in cards:
                self.hand.remove(card)
        else:
            self.hand.remove(cards)

    def add_cards(self, cards):
        if isinstance(cards, list):
            for card in cards:
                self.hand.append(card)
        else:
            self.hand.append(cards)

    def get_discardable_sets(self):
        discarable_sets_list = []
        # trivial sets
        for card in self.hand:
            discarable_sets_list.append([card])

        # same rank
        self.hand.sort(key=lambda x: x.rank)
        running_discardable_set = [self.hand[0]]
        for card in self.hand[1:]:
            if running_discardable_set[-1].rank == card.rank:
                running_discardable_set.append(card)
            elif len(running_discardable_set) > 1:
                discarable_sets_list.append(running_discardable_set)
                running_discardable_set = [card]
            else:
                running_discardable_set = [card]
        if len(running_discardable_set) > 1:
            discarable_sets_list.append(running_discardable_set)

        # straights
        suit_count = self.get_suit_count()
        possible_straight_suits = []
        for suit in suit_count:
            if suit != 'J':
                if suit_count[suit] + suit_count['J'] >= 3:
                    possible_straight_suits.append(suit)
        for suit in possible_straight_suits:
            suit_set = self.get_set_from_hand(self.hand, suit=suit)
            suit_set.extend(self.get_set_from_hand(self.hand, suit='J'))
            suit_super_set = self.superset(suit_set)
            for item in suit_super_set:
                valid, ordered = self.valid_straight_numbers(item)
                if valid:
                    discarable_sets_list.append(ordered)

        return discarable_sets_list

    @staticmethod
    def valid_straight_numbers(cards):
        if len(cards) < 3:
            return False, []
        cards.sort(key=lambda x: x.order)
        valid_straight = []
        jokers = []
        joker_i = 0
        last_order = None
        for card in cards:
            if card.suit == 'J':
                jokers.append(card)
                continue
            if last_order is None or card.order - last_order == 1:
                valid_straight.append(card)
                last_order = card.order
            elif card.order - last_order  - 1 <= len(jokers) - joker_i and card.order != last_order:
                for i in range(joker_i, card.order - last_order - 1):
                    valid_straight.append(jokers[i])
                    joker_i += 1
                valid_straight.append(card)
                last_order = card.order
            else:
                return False, []
        for i in range(joker_i, len(jokers)):
            valid_straight = [jokers[i]] + valid_straight
        return True, valid_straight

    @staticmethod
    def superset(base_set):
        working_set = [[]]
        for item in base_set:
            working_set.extend([s + [item] for s in working_set])
        return working_set

    @staticmethod
    def summed_value_card_sets(card_sets):
        return_list = []
        for card_set in card_sets:
            sum_values = 0
            for card in card_set:
                sum_values += card.value
            return_list.append(sum_values)
        return return_list

    def get_suit_count(self):
        count = {'D': 0, 'S': 0, 'C': 0, 'H': 0, 'J': 0}
        for card in self.hand:
            count[card.suit] += 1
        return count

    @staticmethod
    def get_set_from_hand(hand, suit=None, rank=None):
        if rank is None and suit is not None:
            return [x for x in hand if x.suit == suit]
        if suit is None and rank is not None:
            return [x for x in hand if x.rank == rank]
        if suit is not None and rank is not None:
            return [x for x in hand if x.rank == rank and x.suit == suit]
        else:
            return hand

    def reset_hand(self):
        self.hand = []

    def __str__(self):
        return self.id


if __name__ == '__main__':
    s = {1, 2, 3}
    p = BasePlayer('A')
    print(p.superset(s))
