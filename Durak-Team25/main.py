from Game import Game, RandomOpponentAgent
from GameState import GameState


class GameRunner(object):
    def __init__(self, display=None, agent=None, sleep_between_actions=False):
        super(GameRunner, self).__init__()
        # self.sleep_between_actions = sleep_between_actions
        # self.human_agent = agent is None
        # if display is None:
        #     display = GabrieleCirulli2048GraphicsDisplay(self.new_game, self.quit_game, self.human_agent)

        # if agent is None:
        #     agent = KeyboardAgent(display)

        self.display = display
        self._agent = agent
        self.current_game = None

    def new_game(self, initial_state=None, *args, **kw):
        self.quit_game()
        if initial_state is None:
            initial_state = GameState()
        opponent_agent = RandomOpponentAgent()
        game = Game(self._agent, opponent_agent, self.display, sleep_between_actions=self.sleep_between_actions)
        for i in range(self.num_of_initial_tiles):
            initial_state.apply_opponent_action(opponent_agent.get_action(initial_state))
        self.current_game = game
        return game.run(initial_state)

    def quit_game(self):
        if self.current_game is not None:
            self.current_game.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = Game()
    game.start()
