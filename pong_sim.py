import sys
import argparse
from time import sleep
import tkinter as tk

from pong_player import Human, AI
from pong_grid import Grid


class Game:
    def __init__(self, width, height, agent1, agent2):
        self.grid = Grid(width, height)
        self.players = [agent1, agent2]
        self.root = tk.Tk()
        self.c = tk.Canvas(self.root, width=width*100, height=height*100, borderwidth=5, background='black')
        self.c.pack()
        self.root.update()

    def playGame(self):
        game_over = False
        winner = -1
        if self.players[0].watch or self.players[1].watch:
            self.grid.print(self.c)
            self.root.update()
            self.grid.print()
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
        if self.players[0].watch or self.players[1].watch:
            print('-------------------------------{} won!-------------------'
                  '------------\n'.format(self.players[winner].name))
        self.players[winner].wins += 1

    def game_step(self):
        p1_action = self.players[0].get_action()
        p2_action = self.players[1].get_action()
                    sleep(1)  # Only need to sleep if both are AI
        if winner != -1:
            if self.players[0].watch or self.players[1].watch:
                print('-------------------------------{} won!-----------------'
                      '---------------\n'.format(self.players[winner].name))
            self.players[winner].wins += 1

    def game_step(self, state):
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
