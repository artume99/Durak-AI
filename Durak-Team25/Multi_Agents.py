# from .Deck import hand_out_cards
from .Game import Agent


# class KeyboardAgent(Agent):
#     """
#     An agent controlled by the keyboard.
#     """
#     LEFT_KEY = 'a'
#     RIGHT_KEY = 'd'
#     UP_KEY = 'w'
#     DOWN_KEY = 's'
#
#     def __init__(self, tk_window):
#         super().__init__()
#         self.keys = []
#         tk_window.subscribe_to_keyboard_pressed(self.listener)
#         self.tk_window = tk_window
#         self._should_stop = False
#
#     def get_action(self, state):
#         self._should_stop = False
#         move = self._get_move(state)
#         while move is None and not self._should_stop:
#             self.tk_window.mainloop_iteration()
#             move = self._get_move(state)
#         if self._should_stop:
#             return Action.STOP
#         return move
#
#     def stop_running(self):
#         self._should_stop = True
#
#     def _get_move(self, state):
#         move = None
#         legal_actions = state.get_agent_legal_actions()
#         if Action.LEFT in legal_actions and (self.LEFT_KEY in self.keys or 'Left' in self.keys):  move = Action.LEFT
#         if Action.RIGHT in legal_actions and (self.RIGHT_KEY in self.keys or 'Right' in self.keys):  move = Action.RIGHT
#         if Action.UP in legal_actions and (self.UP_KEY in self.keys or 'Up' in self.keys):  move = Action.UP
#         if Action.DOWN in legal_actions and (self.DOWN_KEY in self.keys or 'Down' in self.keys):  move = Action.DOWN
#         self.keys = []
#         return move
#
#     def listener(self, tk_event=None, *args, **kw):
#         self.keys.append(tk_event.keysym)


class ExpectimaxAgent(Agent):
    def __init__(self, initial_cards=None):
        super().__init__(initial_cards)

    def get_action(self, game_state):
        """
        calculate the appropriate action
        :param game_state:
        :return:
        """
        pass
