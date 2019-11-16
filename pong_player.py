import random
import numpy as np


class Player:
    """
    Parent player class, intializes variables that both humans and AI will
    have.
    """
    def __init__(self, name, alive, watch):
        self.name = name
        self.alive = alive
        self.watch = watch
        self.wins = 0

    def get_action(self, state):
        """
        To be overloaded by the child class
        """
        pass


class Human(Player):
    """
    Human child class of Player. Both alive and watch are not settable by
    the Human class as they need to be set to true for a human to play.
    """
    def __init__(self, name):
        super().__init__(name, True, True)

    def get_action(self, state):
        """
        Prompts the user for input to determine what action the paddle should
        take.
        """
        valid_action = False
        action = 0
        while not valid_action:
            try:
                action = int(input('Choose action {}\n1 = up\n2 = don\'t move'
                                   '\n3 = down\nAction: '.format(self.name)))
                if action > 3 or action < 1:
                    raise ValueError
                else:
                    valid_action = True
            except ValueError:
                print('Invalid action, choose 1, 2 or 3.')
        # NOTE: Since 0 is a the "top", action to go up is -1
        if action == 1:  # up
            action = -1
        elif action == 2:  # don't move
            action = 0
        elif action == 3:  # down
            action = 1
        return action


class AI(Player):
    """
    AI child class of Player. Alive is set to false automatically since an AI
    is not alive. Other variables are given to AI to set the Q-learning
    algorithm parameters and to set up the Q table.
    """
    def __init__(self, name, alpha, epsilon, gamma, width, height,
                 watch=False):
        super().__init__(name, False, watch)
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        # TODO: Intialize Q
        self.qtable = []

    def get_action(self, state):
        """
        Chooses an action from the given state using the policy derived from Q
        with an epsilon-greedy choice.
        :param state: the current state of the game
        """
        # Determines greedy or random
        num = random.random()

        if num <= self.epsilon:
            # Random action
            action = random.randint(-1, 1)
        else:
            action_vals = self.qtable[state]
            action_vals = np.array(action_vals)
            # Choose greedy action, breaking ties randomly
            action = np.random.choice(np.flatnonzero(
                                             action_vals == action_vals.max()))
            if action == 0:  # up
                action = -1
            elif action == 1:  # don't move
                action = 0
            elif action == 2:  # down
                action = 1
        return action

    def updateQ(self, s1, a, r, s2):
        """
        Updates the players Q table given the current state, the chosen action,
        the reward of the action, and the next state.
        :param s1: the current state
        :param a: the chosen action
        :param r: the reward for action a
        :param s2: the next state
        """
        idx1 = self.get_state_idx(s1)
        idx2 = self.get_state_idx(s2)
        q_s1 = self.qtable[idx1]
        q_s2 = self.qtable[idx2]
        q_s1[a] += self.alpha * (r + self.gamma * np.max(q_s2) - q_s1[a])
        self.qtable[idx1][a] = q_s1[a]

    def get_state_idx(self, state):
        """
        Returns the state index in the state table based on the given state.
        :param state: the given state to determine the index of
        """
        # Using state information, determine the index in the Q table
        # NOTE: This could also be done in grids "get_current_state" function
        #       it would just need to take the information and convert that to
        #       an index
        pass
