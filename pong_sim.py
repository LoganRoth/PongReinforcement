import sys
import argparse
from time import sleep
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

from pong_player import Human, AI, Random
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
        # Only display if watch flag is one
        if self.players[0].watch or self.players[1].watch:
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
                    sleep(0.2)  # Only need to sleep if both are AI
        if winner != -1:
            if self.players[0].watch or self.players[1].watch:
                print('-------------------------------{} won!-----------------'
                      '---------------\n'.format(self.players[winner].name))
            self.players[winner].wins += 1
        return winner

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
        s_prime = self.grid.get_grid_state()
        rewards = self.grid.get_reward(state, s_prime)
        p1_reward = rewards['P1 Reward']
        p2_reward = rewards['P2 Reward']
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
        # default=True, # Show gameplay
        default=False,
        help='If both players are AI, set if you would like to watch them '
             'play.',
    )
    parser.add_argument(
        '--train',
        action='store',
        default=100000,
        # default=5,
        help='Set the number of games to play to train the comupter.'
    )
    parser.add_argument(
        '--tune',
        action='store_true',
        default=False,
        help='Set to put it into tuning mode for the algorithm parameters'
    )
    args = parser.parse_args()
    return args.p1, args.p2, args.watch, int(args.train), args.tune


def play_mode(p1_type, p2_type, watch, train):
    # Algorithm Parameters alpha, epsilon, gamma
    alpha1 = 0.5
    epsilon1 = 0.01
    gamma1 = 0.8
    alpha2 = 0.5
    epsilon2 = 0.1
    gamma2 = 0.8
    width = 15
    height = 10
    if p1_type == 'AI':
        p1 = AI('Player 1', alpha1, epsilon1, gamma1, width, height, watch)
    elif p1_type == 'Human':
        p1 = Human('Player 1')
    else:
        print('Invalid selection for P1')
        return
    if p2_type == 'AI':
        p2 = AI('Player 2', alpha2, epsilon2, gamma2, width, height, watch)
        # p2 = Random('Player 2', watch)
    elif p2_type == 'Human':
        p2 = Human('Player 2')
    else:
        print('Invalid selection for P2')
        return

    #Create an AI which will use a random strategy
    rando = Random('Player 2', watch)
    # Loop for each episode
    for i in range(train):
        game = Game(width, height, p1, rando)
        game.playGame()
    print('P1 Wins: {}\nRando Wins: {}'.format(p1.wins, rando.wins))
    rando.name = 'Player 1'
    rando.wins = 0

    player_wins = np.zeros(train//1000)
    player2counter = 0

    # Loop for each episode
    for i in range(train):
        game = Game(width, height, rando, p2) #Train player 2
        if i % 1000 == 0:
            player_wins[i // 1000] = player2counter + game.playGame()
        else:
            player2counter += game.playGame()
    print('P2 Wins: {}\nRando Wins: {}'.format(p2.wins, rando.wins))

    # Watch a game after they have been fully trained
    p1.epsilon = -1
    p2.epsilon = -1
    p1.watch = True
    p2.watch = True
    input("Are you ready, kids?")
    for _ in range(5):
        game = Game(width, height, p1, p2)
        game.playGame()

    plt.scatter(np.arange(train//1000), player_wins)
    plt.ylabel("# of Wins")
    plt.xlabel("Episode (1000s)")
    plt.show()

def tune_mode(watch, train):
    # Algorithm Parameters alpha, epsilon, gamma
    alphas = [0.2, 0.7, 0.725, 0.75, 0.775, 0.8]
    epsilons = [0.01]
    gammas = [0.2, 0.6, 0.7, 0.8]
    width = 15
    height = 10
    most_wins = 0
    best_alpha = None
    best_epsilon = None
    best_gamma = None
    rando = Random('Player 2', watch)
    for alpha in alphas:
        for epsilon in epsilons:
            for gamma in gammas:
                p1 = AI('Player 1', alpha, epsilon, gamma, width, height,
                        watch)
                # Loop for each episode
                for i in range(train):
                    game = Game(width, height, p1, rando)
                    game.playGame()
                if p1.wins > most_wins:
                    most_wins = p1.wins
                    best_alpha = alpha
                    best_epsilon = epsilon
                    best_gamma = gamma

    print('Most wins ({}) with params:\nα={}\nε={}\nγ={}'.format(most_wins,
                                                                 best_alpha,
                                                                 best_epsilon,
                                                                 best_gamma))


def main():
    """
    Main program of the pong game. Alogrithm paramters are set here.
    After a full training session by the AI players there will be a final game
    played between the two of them that the users can watch and see the AI use
    the final derived policies.
    """
    p1_type, p2_type, watch, train, tune = parse_args()
    if tune:
        tune_mode(watch, train)
    else:
        play_mode(p1_type, p2_type, watch, train)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Aborting')
    sys.exit(0)
