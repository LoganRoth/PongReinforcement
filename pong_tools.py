import random


class Ball:
    """
    Class for the pong ball.
    :attr x_pos: x position of the ball
    :attr y_pos: y position of the ball
    :attr x_vel: x velocity of the ball (-1 or 1)
    :attr y_vel: y velocity of the ball (-1, 0, or 1)
    """
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = -1 if random.randint(0, 1) == 0 else 1
        self.y_vel = random.randint(-1, 1)


class Paddle:
    """
    Class for the pong paddle.
    :attr position: a list of row indices that the paddle is on
                    ie, [1, 2, 3] means the paddle covers rows 1, 2, and 3 in
                    whichever column the player is on (player 1 in column 0,
                    player 2 in column height-1)
    :attr idx: the position index to indicate which of the 5 possible
               positions the paddle is in
    :attr top: the index of the top of the paddle
    :attr bottom: the index of the bottom of the paddle
    """
    def __init__(self, position: list, idx):
        self.position = position
        self.pos_idx = idx
        self.top = min(position)
        self.bottom = max(position)
        self.length = len(position)

    def update_position(self, position: list):
        """
        Updates the position of the paddle given a new position list.
        """
        self.position = position
        self.top = min(position)
        self.bottom = max(position)
