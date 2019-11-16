import random


class Ball:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = -1 if random.randint(0, 1) == 0 else 1
        self.y_vel = random.randint(-1, 1)


class Paddle:
    def __init__(self, position: list, idx):
        self.position = position
        self.pos_idx = idx
        self.top = min(position)
        self.bottom = max(position)
        self.length = len(position)

    def update_position(self, position: list):
        self.position = position
        self.top = min(position)
        self.bottom = max(position)
