from time import sleep
import tkinter as tk

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
        self.timeSteps = 0
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
            self.timeSteps += 1
            game_over, winner, s_prime = self.game_step(s)
            # S <- S'
            s = s_prime
            if self.players[0].watch or self.players[1].watch:
                self.grid.print(self.c)
                self.root.update()
                if not self.players[0].alive and not self.players[1].alive:
                    sleep(0.05)  # Only need to sleep if both are AI
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
        s_prime = self.grid.get_grid_state()
        if ((state["Ball Pos"][0] == 1) and (s_prime["Ball Pos"][0] == 2)):
            self.players[0].hits += 1
        if ((state["Ball Pos"][0] == 13) and (s_prime["Ball Pos"][0] == 12)):
            self.players[1].hits += 1
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
