import sys
import argparse
import numpy as np
import matplotlib.pyplot as plot

from pong_player import Human, AI, Random
from pong_game import Game


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
        default=False,
        help='If both players are AI, set if you would like to watch them '
             'play.',
    )
    parser.add_argument(
        '--train',
        action='store',
        default=50000,
        help='Set the number of games to play to train the comupter.'
    )
    parser.add_argument(
        '--mode',
        action='store',
        default=0,
        help='Mode 0: Train two agents and have them play each other. '
             'Mode 1: Tune the algorithm parameters to find the best set. '
             'Mode 2: Train one agent and then save the Q-table to a file. '
             'Mode 3: Two agents use saved Q-tables and play each other. '
             'Mode 4: Train two agents and graphs results.'
    )
    args = parser.parse_args()
    return args.p1, args.p2, args.watch, int(args.train), int(args.mode)


def write_qtable(player, width, height):
    """
    Writes a Q-Table text file that can be loaded in by the get_qtable function
    and used by two agents.
    """
    with open('qtable.txt', 'w+') as f:
        f.write(str(player.alpha) + '\n')
        f.write(str(player.gamma) + '\n')
        for x in range(width):
            for y in range(height):
                for idx in range(13):  # Number of paddle positions
                    for a in range(3):  # Number of possible actions
                        f.write(str(player.qtable[x, y, idx, a]) + '\n')


def get_qtable(player, name, width, height):
    """
    Reads a Q-Table text file create by the write_qtable function
    and sets it as the AI agent's Q-Table to be used.
    """
    qtable = None
    with open('qtable.txt', 'r') as f:
        qtable = f.readlines()
    qtableIter = iter(qtable)
    player.alpha = float(next(qtableIter))
    player.gamma = float(next(qtableIter))
    for x in range(width):
        for y in range(height):
            for idx in range(13):  # Number of paddle positions
                for a in range(3):  # Number of possible actions
                    if name == 'Player 1':
                        player.qtable[x, y, idx, a] = float(next(qtableIter))
                    else:
                        x_flip = 18 - x  # Flip the table for Player 2
                        player.qtable[x_flip, y, idx, a] =\
                            float(next(qtableIter))


def train_and_play_mode(p1_type, p2_type, watch, train, width, height):
    """
    Mode 0
    Train two agents and have them play each other.
    """
    # Algorithm Parameters alpha, epsilon, gamma
    alpha1 = 0.8
    epsilon1 = 0.005
    gamma1 = 0.8
    alpha2 = 0.8
    epsilon2 = 0.005
    gamma2 = 0.8
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
    rando = Random('Player 2', watch)
    # Loop for each episode
    for _ in range(train):
        game = Game(width, height, p1, rando)
        game.playGame()
    print('P1 Wins: {}\nRando Wins: {}'.format(p1.wins, rando.wins))
    rando.name = 'Player 1'
    rando.wins = 0
    # Loop for each episode
    for _ in range(train):
        game = Game(width, height, rando, p2)
        game.playGame()
    print('P2 Wins: {}\nRando Wins: {}'.format(p2.wins, rando.wins))

    # Watch a game after they have been fully trained
    p1.epsilon = -1
    p2.epsilon = -1
    p1.watch = True
    p2.watch = True
    input("Press [Enter] when ready to begin game")
    for _ in range(5):
        game = Game(width, height, p1, p2)
        game.playGame()


def tune_mode(train, width, height):
    """
    Mode 1
    Tune the algorithm parameters to find the best set.
    """
    # Algorithm Parameters alpha, epsilon, gamma
    alphas = np.linspace(0.1, 1, 36, endpoint=False)
    epsilons = np.linspace(0.005, 0.05, 10)
    gammas = np.linspace(0.1, 1, 36, endpoint=False)
    most_wins = 0
    best_alpha = None
    best_epsilon = None
    best_gamma = None
    rando = Random('Player 2', False)
    for alpha in alphas:
        for epsilon in epsilons:
            for gamma in gammas:
                p1 = AI('Player 1', alpha, epsilon, gamma, width, height,
                        False)
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


def train_and_save_mode(train, width, height):
    """
    Mode 2
    Train one agent and then save the Q-table to a file.
    """
    alpha = 0.8
    epsilon = 0.005
    gamma = 0.8
    p1 = AI('Player 1', alpha, epsilon, gamma, width, height, False)
    rando = Random('Player 2', False)
    # Loop for each episode
    for _ in range(train):
        game = Game(width, height, p1, rando)
        game.playGame()
    write_qtable(p1, width, height)


def play_mode(p1_type, p2_type, width, height):
    """
    Mode 3
    Two agents use saved Q-tables and play each other.
    """
    if p1_type == 'AI':
        p1 = AI('Player 1', 0, -1, 0, width, height, True)
    elif p1_type == 'Human':
        p1 = Human('Player 1')
    else:
        print('Invalid selection for P1')
        return
    if p2_type == 'AI':
        p2 = AI('Player 2', 0, -1, 0, width, height, True)
    elif p2_type == 'Human':
        p2 = Human('Player 2')
    else:
        print('Invalid selection for P2')
        return
    get_qtable(p1, 'Player 1', width, height)
    get_qtable(p2, 'Player 2', width, height)
    input("Press [Enter] when ready to begin game")
    for _ in range(1):
        game = Game(width, height, p1, p2)
        game.playGame()


def generate_timesteps_plot(train, width, height):
    """
    Mode 4
    Used to generate time step and hit plots.
    """
    alpha1 = 0.8
    epsilon1 = 0.005
    gamma1 = 0.8
    alpha2 = 0.8
    epsilon2 = 0.005
    gamma2 = 0.8
    p1 = AI('Player 1', alpha1, epsilon1, gamma1, width, height)
    p2 = AI('Player 2', alpha2, epsilon2, gamma2, width, height)
    rando = Random('Test')
    gameNum = 0
    plot.plot(gameNum, 0, 'b.')
    plot.xlabel("Game number")
    plot.ylabel("Time steps")
    # Loop for each episode
    for _ in range(train):
        gameNum += 1
        print(gameNum)
        game = Game(width, height, p1, rando)
        game2 = Game(width, height, rando, p2)
        game.playGame()
        game2.playGame()
        # Play a game together and count time steps
        testGame = Game(width, height, p1, p2)
        testGame.playGame()
        # Can adjust this to be p1.hits, p2.hits
        plot.plot(gameNum, testGame.timeSteps, 'b.')

    plot.show()

    print('Done making the plot!')


def main():
    """
    Main program of the pong game. Alogrithm paramters are set here.
    After a full training session by the AI players there will be a final game
    played between the two of them that the users can watch and see the AI use
    the final derived policies.
    """
    width = 19
    height = 15
    p1_type, p2_type, watch, train, mode = parse_args()
    if mode == 0:
        train_and_play_mode(p1_type, p2_type, watch, train, width, height)
    elif mode == 1:
        tune_mode(train, width, height)
    elif mode == 2:
        train_and_save_mode(train, width, height)
    elif mode == 3:
        play_mode(p1_type, p2_type, width, height)
    elif mode == 4:
        generate_timesteps_plot(train, width, height)
    else:
        print('Invalid mode selected')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Aborting')
    sys.exit(0)
