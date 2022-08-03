from collections import namedtuple
from typing import List

from Deck import Deck
from Game import RandomOpponentAgent, Action
from Game import Agent

CardTup = namedtuple("CardTup", ["attack", "defend"])


class GameState:
    def __init__(self, deck: Deck = None, done=False):
        super(GameState, self).__init__()
        self.attacker = Agent()  # can remove the defender state as it will always be the opposition of the attacker
        self.defender = Agent()
        self.deck = deck
        self.looser = None
        self._done = done
        self.card_in_play = None
        self.cards_on_board: List[CardTup] = []

    @property
    def done(self):
        return self._done

    def reshuffle(self):
        self.deck.build()

    def get_legal_actions(self, agent_index):
        if agent_index == 0:
            return self.get_agent_legal_actions()
        elif agent_index == 1:
            return self.get_opponent_legal_actions()
        else:
            raise Exception("illegal agent index.")

    def get_opponent_legal_actions(self):
        """
        Checks the type of the opponent (attack, defend) and returns it's actions
        :return:
        """
        if type(self.attacker) is RandomOpponentAgent:
            return self.attacking_actions()
        else:
            return self.defending_actions()

    def attacking_actions(self):
        if len(self.cards_on_board) == 6 or len(self.attacker.hand) == 0:
            return [Action.BETA]  # Return beta, max 6 cards on board
        actions = self.attacker.hand
        if len(self.cards_on_board) > 0:  # Add beta action if there is a card in play
            actions.append(Action.BETA)
        return actions

    def defending_actions(self):
        if len(self.defender.hand) == 0:
            return [Action.BETA]  # Hands is empty
        actions = [Action.TAKE]
        for card in self.defender.hand:
            if self._can_attack_card_in_play(card):
                actions.append(card)
        return actions

    def _can_attack_card_in_play(self, card):
        """
        checks if "card" can attack the card in play
        :param card:
        :return:
        """
        return (card.suit == self.card_in_play.suit and card.rank > self.card_in_play.rank) \
               or (card.is_kozer() and not self.card_in_play.is_kozer())

    def get_agent_legal_actions(self):
        """
        Checks the type of the player (attack, defend) and returns it's actions
        :return:
        """
        if type(self.attacker) is RandomOpponentAgent:
            return self.defending_actions()
        else:
            return self.attacking_actions()

    def apply_attack_action(self, action):
        if Action.BETA:
            self._replenish_cards_for_players()
            self._clear_board()
            self._switch_roles()
        else:  # Place card
            self.card_in_play = action
            self.attacker.hand.remove(action)
            self.cards_on_board.append(CardTup(attack=action, defend=None))
        self._check_looser()

    def apply_defend_action(self, action):
        if Action.BETA:
            self._replenish_cards_for_players()
            self._clear_board()
            self._switch_roles()
        elif Action.TAKE:
            self.defender.hand.extend(self.cards_on_board)
            self._replenish_cards(self.attacker)
            self._clear_board()
        else:  # Place card
            self.defender.hand.remove(action)
            self.cards_on_board[-1].defend = action
        self._check_looser()

    def _switch_roles(self):
        self.attacker, self.defender = self.defender, self.attacker

    def _clear_board(self):
        self.cards_on_board.clear()

    def _check_looser(self):
        """
        Checks if there is a looser, null if there is no looser
        :return:
        """
        if len(self.attacker.hand) == 0:
            self.looser = self.defender
            self._done = True
        elif len(self.defender.hand) == 0:
            self.looser = self.attacker
            self._done = True

    def _replenish_cards_for_players(self):
        """
        check if either player needs more cards and give them if necessary
        the attacker gets cards first
        :return:
        """
        if len(self.deck.cards_list) <= 0:
            return
        self._replenish_cards(self.attacker)
        self._replenish_cards(self.defender)

    def _replenish_cards(self, player: Agent):
        cards_needed = max(0, 6 - len(player.hand))
        player.hand.extend(self.deck.hand_out_cards(cards_needed))

    def generate_successor(self, agent_index=0, action=Action.STOP):
        """
        generates teh successor state by apllying action
        :param agent_index:
        :param action:
        :return:
        """
        # successor = GameState(rows=self._num_of_rows, columns=self._num_of_columns, board=self._board.copy(),
        #                       score=self.score, done=self._done)
        # if agent_index == 0:
        #     successor.apply_action(action)
        # elif agent_index == 1:
        #     successor.apply_opponent_action(action)
        # else:
        #     raise Exception("illegal agent index.")
        # return successor
        pass
