import sys
import argparse
from time import sleep
import tkinter as tk

from pong_player import Human, AI
from pong_grid import Grid


class Game:
    """
    Game class that controls the main game loop of pong
    :attr width: the width of the game grid in discreet boxes
    :attr height: the height of the game grid in discreet boxes
    :attr agent1: the agent to use for player 1
    :attr agent2: the agent to use for player 2
    """
    def __init__(self, width, height, agent1, agent2):
        self.grid = Grid(width, height)
        self.players = [agent1, agent2]
        self.root = tk.Tk()
        self.c = tk.Canvas(self.root, width=width*100, height=height*100,
                           borderwidth=5, background='black')
        self.c.pack()
        self.root.update()

    def playGame(self):
        """
        Plays a single game. A game is over after either player scores.
        """
        game_over = False
        winner = -1
        if self.players[0].watch or self.players[1].watch:
            self.grid.print(self.c)
            self.root.update()
        # Initialize S
        s = self.grid.get_grid_state()
        # Loop for each step of an episode
        while not game_over:
            game_over, winner, s_prime = self.game_step(s)
            # S <- S'
            s = s_prime
            if self.players[0].watch or self.players[1].watch:
                self.grid.print(self.c)
                self.root.update()
                if not self.players[0].alive and not self.players[1].alive:
                    sleep(0.4)  # Only need to sleep if both are AI
        if winner != -1:
            if self.players[0].watch or self.players[1].watch:
                print('-------------------------------{} won!-----------------'
                      '---------------\n'.format(self.players[winner].name))
            self.players[winner].wins += 1

    def game_step(self, state):
        """
        Performs one step of the game. This will get the actions of both of
        the players, and then move the paddles and ball based on those actions.
        The given state will be used by AI players to determine their actions
        and will be used to update their Q tables.
        :param state: the current state of the game
        """
        # Choose A from S using policy derived from Q
        p1_action = self.players[0].get_action(state)
        p2_action = self.players[1].get_action(state)
        # Take action A and observe R, S'
        self.grid.move(p1_action, p2_action)
        rewards = self.grid.get_reward()
        p1_reward = rewards['P1 Reward']
        p2_reward = rewards['P2 Reward']
        s_prime = self.grid.get_grid_state()
        # Update Q Table
        if not self.players[0].alive:  # Only AI do this
            self.players[0].updateQ(state, p1_action, p1_reward, s_prime)
        if not self.players[1].alive:  # Only AI do this
            self.players[1].updateQ(state, p2_action, p2_reward, s_prime)
        step = (self.grid.result['Point Awarded'], self.grid.result['Scorer'],
                s_prime)
        return step


def parse_args():
    """
    Argument parser so that a user an change some params from the command line.
    """
    parser = argparse.ArgumentParser(usage='pong_sim.py --p1=[AI, Human] '
                                           '--p2=[AI, Human] [options]')
    parser.add_argument(
        '--p1',
        action='store',
        default='AI',
        help='Set if p1 should be an AI or a Human',
    )
    parser.add_argument(
        '--p2',
        action='store',
        default='AI',
        help='Set if p2 should be an AI or a Human',
    )
    parser.add_argument(
        '--watch', '-w',
        action='store_true',
        default=True,
        help='If both players are AI, set if you would like to watch them '
             'play.',
    )
    parser.add_argument(
        '--train',
        action='store',
        default=10000,
        help='Set the number of games to play to train the comupter.'
    )
    args = parser.parse_args()
    return args.p1, args.p2, args.watch, int(args.train)


def main():
    """
    Main program of the pong game. Alogrithm paramters are set here.
    After a full training session by the AI players there will be a final game
    played between the two of them that the users can watch and see the AI use
    the final derived policies.
    """
    p1_type, p2_type, watch, train = parse_args()
    # Algorithm Parameters alpha, epsilon, gamma
    alpha = 0.3
    epsilon = 0.005
    gamma = 0.8
    width = 15
    height = 10
    if p1_type == 'AI':
        p1 = AI('Player 1', alpha, epsilon, gamma, width, height, watch)
    elif p1_type == 'Human':
        p1 = Human('Player 1')
    else:
        print('Invalid selection for P1')
        return
    if p2_type == 'AI':
        p2 = AI('Player 2', alpha, epsilon, gamma, width, height, watch)
    elif p2_type == 'Human':
        p2 = Human('Player 2')
    else:
        print('Invalid selection for P2')
        return
    # Loop for each episode
    for i in range(train):
        game = Game(width, height, p1, p2)
        game.playGame()
    print('P1 Wins: {}\nP2 Wins: {}'.format(p1.wins, p2.wins))

    # Watch a game after they have been fully trained
    p1.watch = True
    p2.watch = True

    game = Game(width, height, p1, p2)
    game.playGame()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Aborting')
    sys.exit(0)
