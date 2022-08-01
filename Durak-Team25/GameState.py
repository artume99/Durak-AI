class GameState:
    def __init__(self, rows=DEFAULT_BOARD_SIZE, columns=DEFAULT_BOARD_SIZE, board=None, score=0, done=False):
        super(GameState, self).__init__()
        self.attacker = None  # can remove the defender state as it will always be the opposition of the attacker
        self.defender = None
        pass
        # self._done = done
        # self._score = score
        # if board is None:
        #     board = np.zeros((rows, columns), dtype=np.int32)
        # self._board = board
        # self._num_of_rows, self._num_of_columns = rows, columns

    # @property
    # def done(self):
    #     return self._done
    #
    # @property
    # def score(self):
    #     return self._score
    #
    # @property
    # def max_tile(self):
    #     return np.max(self._board)
    #
    # @property
    # def board(self):
    #     return self._board

    def get_legal_actions(self, agent_index):
        if agent_index == 0:
            return self.get_agent_legal_actions()
        elif agent_index == 1:
            return self.get_opponent_legal_actions()
        else:
            raise Exception("illegal agent index.")

    def get_opponent_legal_actions(self):
        pass

    def get_agent_legal_actions(self):
        pass

    def apply_opponent_action(self, action):
        pass

    def apply_action(self, action):
        pass

    def update_state(self):
        """
        updates the state of the game
        :return:
        """
        pass

    def generate_successor(self, agent_index=0, action=Action.STOP):
        successor = GameState(rows=self._num_of_rows, columns=self._num_of_columns, board=self._board.copy(),
                              score=self.score, done=self._done)
        if agent_index == 0:
            successor.apply_action(action)
        elif agent_index == 1:
            successor.apply_opponent_action(action)
        else:
            raise Exception("illegal agent index.")
        return successor
