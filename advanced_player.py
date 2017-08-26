from player import BasePlayer
from neural_network import NeuralNetwork
import numpy as np


class AdvancedPlayer(BasePlayer):

    def __init__(self, id, nn_parameters):
        super().__init__(id)
        self.yaniv_nn = NeuralNetwork([6, 1])
        self.discard_nn = NeuralNetwork([7, 1])
        self.draw_nn = NeuralNetwork([5, 2])

        self.yaniv_nn.set_parameters(nn_parameters[:self.yaniv_nn.get_num_params()])
        self.discard_nn.set_parameters(nn_parameters[self.yaniv_nn.get_num_params():self.yaniv_nn.get_num_params()
                                                                                    +self.discard_nn.get_num_params()])
        self.draw_nn.set_parameters(nn_parameters[-self.draw_nn.get_num_params():])

    def decide_call_yaniv(self, game):
        if self.get_hand_value() > 7:
            return False
        if len(self.hand) == 0:
            return True
        opponent_num_cards = [len(p.hand) for p in game.player_list if p is not self]
        opponent_num_cards.sort()
        draw_card_value = min([c.value for c in game.deck.get_cards_available()])
        input_vec = np.array(opponent_num_cards + [self.get_hand_value(), game.round_counter, draw_card_value])
        if self.yaniv_nn.feed_forward(input_vec)[0] > 0.5:
            return True
        return False

    def decide_cards_to_discard(self, game):
        discardable_sets = self.get_discardable_sets()
        scored_sets = []
        for discardable_set in discardable_sets:
            input_vec = np.array([min(game.get_num_cards_players()), game.deck.get_top_card().value]
                                 + [c.value for c in discardable_set] + [0 for _ in range(5 - len(discardable_set))])
            scored_sets.append((self.discard_nn.feed_forward(input_vec), discardable_set))
        scored_sets.sort(key=lambda x: -x[0][0])
        return scored_sets[0][1]

    def decide_card_to_draw(self, game):
        input_vec = [game.round_counter, min(game.get_num_cards_players()), self.get_hand_value()]
        for card in game.deck.get_cards_available():
            input_vec.extend([card.value])
        if len(game.deck.get_cards_available()) == 1:
            input_vec.append(0)
        signal = self.draw_nn.feed_forward(np.array(input_vec))
        if signal[0] > 0.5 and game.deck.get_last_straight_bottom_card() is not None:
            return 'start of previous straight in discard pile', game.deck.get_last_straight_bottom_card()
        if signal[1] > 0.5:
            return 'discard pile', game.deck.get_top_discard()
        else:
            return 'unseen pile', game.get_top_card()
