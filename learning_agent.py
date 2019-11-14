from pong_sim import main

import random
import numpy

'''
Sets up the pong state space to be used for Qlearning
Initializes start state
Moves states given an action
'''
class pongStates:

    # Constructor that initializes start state and all possible states
    def __init__(self):
        # Whatever we want the initial coordinates of the paddles and ball to be
        self.paddle1x = 0
        self.paddle1y = 0
        self.paddle2x = 0
        self.paddle2y = 0
        self.ballx = 0
        self.bally = 0
        # Cesur and Alex create state space here
        self.states = []


    # Moves paddle1x, paddle1y, paddle2x, paddle2y, ballx and bally
    # Actions in form of 0, 1 or 2 for up down and stay still
    def moveState(self, action):
        if (action == 0): # move paddle up
            pass
            # Adjust paddle coordinates here
            # And continue path of ball by one step?

        elif (action == 1): # move paddle down
            pass
            # Adjust paddle coordinates here
            # And continue path of ball by one step?

        else: # stay still
            pass
            # Adjust paddle coordinates here
            # And continue path of ball by one step?


    # Returns current state as list of paddle coordinates and ball coordinates
    def getCurrentState(self):
        currentState = []
        currentState.append((self.paddle1x, self.paddle1y))
        currentState.append((self.paddle2x, self.paddle2y))
        currentState.append((self.ballx, self.bally))

        return currentState

    # Accessor for the states
    def getStates(self):
        return self.states

    # Defines rewards for each state
    def getReward(self, state):
        pass
        # Implement -1 for losing state

'''
Used to implement the QLearning algorithm
Creates instance of pong states
Initializes qTable
'''
class QLearning:

    # Adjustable gamma, alpha and epsilon parameters
    def __init__(self, gamma, alpha, epsilon):
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon

        # This will need to be an x by 3 array
        # x being the number of states
        self.qTable = [[]]

    # Called to the the QLearning algorithm
    def runAlgorithm(self):

        # Large number of episodes
        for i in range(10000):

            # Initializing grid and getting current state
            pongGrid = pongStates()
            S = pongGrid.getCurrentState()
            states = pongGrid.getStates()

            # Will need to adjust this so (None, None) is whatever the losing/winning state is
            while pongGrid.getCurrentState() != (None, None):
                # Get the possible actions
                index1 = states.index(S)
                actionValues = self.qTable[index1]

                # Determines greedy or random
                num = random.random()

                if num <= self.epsilon:
                    # Random action
                    action = random.randint(0, 3)
                else:
                    # Greedy action
                    action = (numpy.ndarray.tolist(actionValues)).index(max(actionValues))

                # Observe S' and R
                pongGrid.moveState(action)
                S2 = pongGrid.getCurrentState()
                reward = pongGrid.getReward(S2)

                # Get possible A'
                index2 = states.index(S2)
                possibleActions = self.qTable[index2]

                maxA = (numpy.ndarray.tolist(possibleActions)).index(max(possibleActions))
                qSA = self.qTable[index1][action]
                # Update QTable
                self.qTable[index1][action] = qSA + self.alpha*(reward + self.gamma*self.qTable[index2][maxA] - qSA)
                S = S2  # S <- S'

        return

def main():

    agent = QLearning(0.5, 0.5, 0.1)
    agent.runAlgorithm()

main()

