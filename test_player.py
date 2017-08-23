import unittest
import player
from card import Card


class test_BasePlayer(unittest.TestCase):

    def test_valid_straight_numbers(self):
        sut = player.BasePlayer('A')
        cards = [Card('D', '4'), Card('D', '5'), Card('D', '6')]
        assert(sut.valid_straight_numbers(cards) == (True, cards))

        cards = [Card('D', '2'), Card('D', '5'), Card('D', '6'), Card('J', '')]
        assert (sut.valid_straight_numbers(cards) == (False, []))

        cards = [Card('D', '5'), Card('D', '6'), Card('J', '')]
        assert (sut.valid_straight_numbers(cards) == (True, [cards[0], cards[1], cards[2]]))

        cards = [Card('D', '5'), Card('D', '5'), Card('D', '6'), Card('D', '7')]
        assert (sut.valid_straight_numbers(cards) == (False, []))

        cards = [Card('D', '5'), Card('D', '5'), Card('D', '6'), Card('D', '7'), Card('J', '')]
        assert (sut.valid_straight_numbers(cards) == (False, []))

        cards = [Card('D', '5'), Card('J', ''), Card('D', '8'), Card('J', '')]
        expected = [Card('D', '5'), Card('J', ''), Card('J', ''), Card('D', '8')]
        assert (sut.valid_straight_numbers(cards) == (True, expected))

        cards = [Card('D', '5'), Card('J', ''), Card('D', '6'), Card('J', '')]
        expected = [Card('J', ''), Card('D', '5'), Card('J', ''), Card('J', '')]
        assert (sut.valid_straight_numbers(cards) == (True, cards))

