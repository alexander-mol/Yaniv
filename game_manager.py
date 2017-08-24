from player import BasePlayer
from advanced_player import AdvancedPlayer
from deck import Deck
from game import Game
import logging
import pickle


class GameManager:

    def __init__(self, player_list=None):
        self.deck = Deck()
        if player_list is None:
            self.player_list = [BasePlayer('A'), BasePlayer('B'), BasePlayer('C'), BasePlayer('D')]
        else:
            self.player_list = player_list
        self.game = Game(self.deck, self.player_list)
        logging.basicConfig(filename='log.txt',
                            filemode='w',
                            # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            format='%(message)s',
                            # datefmt='%H:%M:%S',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def play_games(self, num_games):
        scores_dict = dict([(p.id, 0) for p in self.player_list])
        draw_count = 0
        starting_player = self.player_list[0]
        for i in range(num_games):
            self.logger.debug(f'-------------- Started game {i} --------------')
            self.deck.reset()
            self.deal_cards()
            self.flip_first_card()
            self.game.round_counter = 0
            starting_player, result = self.game_round_loop(starting_player)
            if result is 'draw':
                draw_count += 1
                continue
            for p in result.keys():
                scores_dict[p] += result[p]
        self.logger.info(f'Final scores after {num_games} games: {scores_dict}.')
        self.logger.info(f'Number of draws: {draw_count}.')
        # print(f'Final scores after {num_games} games: {scores_dict}.')
        # print(f'Number of draws: {draw_count}.')
        return scores_dict, draw_count

    def deal_cards(self):
        for player in self.player_list:
            player.reset_hand()
            for _ in range(5):
                player.add_cards(self.deck.draw_top_card())

    def flip_first_card(self):
        self.deck.discard(self.deck.draw_top_card())

    def game_round_loop(self, starting_player):
        self.logger.info(f'Started game with {len(self.player_list)} players, {[p.id for p in self.player_list]}.')
        yaniv = False
        turn_zero = True
        while not yaniv:
            if self.game.round_counter >= 40:
                self.logger.info(f'Game ends in draw.')
                # print('Game ends in draw.')
                return None, 'draw'
            for player in self.player_list:
                if turn_zero and player is not starting_player:
                    continue
                turn_zero = False
                self.logger.debug(f'Player {player.id} starting turn. Round: {self.game.round_counter}')
                self.logger.debug(f"Player's hand: {[str(c) for c in player.hand]}, value: {player.get_hand_value()}.")
                self.logger.debug(f'Top of discard pile: {self.deck.get_top_discard()}')
                if player.decide_call_yaniv(self.game):
                    self.logger.info(f'Player {player} calls yaniv!')
                    # print(f'Player {player} calls yaniv!')
                    scores_dict = self.yaniv_handler(player)
                    return player, scores_dict
                player_discards = player.decide_cards_to_discard(self.game)
                self.logger.debug(f'Player discards: {[str(c) for c in player_discards]}')
                draw_pile, draw_card = player.decide_card_to_draw(self.game)
                self.logger.debug(f'Player draws from {draw_pile}, {str(draw_card)}.')
                self.execute_player_deck_interactions(player, player_discards, draw_pile, draw_card)
            self.game.round_counter += 1

    def execute_player_deck_interactions(self, player, discards, draw_pile, draw_card):
        if draw_pile == 'discard pile':
            self.deck.draw_top_discard()
        elif draw_pile == 'start of previous straight in discard pile':
            self.deck.draw_last_straight_bottom_card()
        elif draw_pile == 'unseen pile':
            self.deck.draw_top_card()
        else:
            self.logger.warning('WARNING: Unknown draw pile string.')
            print('WARNING: Unknown draw pile string.')
        player.extract_cards(discards)
        self.deck.discard(discards)
        if draw_card.rank == self.deck.get_top_discard().rank and draw_card.suit != 'J':
            self.logger.debug(f'Card drawn has same rank as top discard: immediate discard.')
            self.deck.discard(draw_card)
        else:
            player.add_cards(draw_card)

    def yaniv_handler(self, yaniv_caller):
        yaniv_caller_hand_value = yaniv_caller.get_hand_value()
        for player in self.player_list:
            if player.get_hand_value() <= yaniv_caller_hand_value and player is not yaniv_caller:
                self.game.assafed = True
                self.logger.debug(f'{yaniv_caller} was assafed by {player}!')
                # print(f'{yaniv_caller} was assafed by {player}!')
                break
        self.logger.debug(f'Final hand values: {[(p.id, p.get_hand_value()) for p in self.player_list]}')
        scores_dict = self.create_score_dict(yaniv_caller)
        return scores_dict

    def create_score_dict(self, yaniv_caller):
        scores_dict = {}
        for player in self.player_list:
            if player is yaniv_caller:
                if not self.game.assafed:
                    scores_dict[player.id] = 0
                else:
                    scores_dict[player.id] = player.get_hand_value() + 30
            else:
                scores_dict[player.id] = player.get_hand_value()
        return scores_dict


if __name__ == '__main__':
    # wins = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'Draw': 0}
    # for _ in range(10000):
    #     gm = GameManager()
    #     gm.deal_cards()
    #     gm.flip_first_card()
    #     wins[gm.game_round_loop().id] += 1
    # print(wins)
    with open('08241201.p', 'rb') as f:
        params = pickle.load(f)
    player_list = [AdvancedPlayer('A', params), BasePlayer('B'), BasePlayer('C'), BasePlayer('D')]
    gm = GameManager(player_list)
    gm.play_games(100)
