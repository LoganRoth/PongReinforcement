import random

from pong_tools import Ball, Paddle


class Grid:
    def __init__(self, width, height):
        self.result = {'Point Awarded': False, 'Scorer': None}
        self.width = width
        self.height = height
        self.field = []
        for i in range(width):
            one_row = []
            for j in range(height):
                one_row.append(0)
            self.field.append(one_row)
        ball_x = int(width/2)
        ball_y = int(height/2)
        self.field[ball_x][ball_y] = 2  # place the ball
        p1_paddle_pos = []
        p2_paddle_pos = []
        paddle_len = int(height/5)  # 5 discreet paddle positions
        for i in range(paddle_len):
            self.field[0][i + (2 * paddle_len)] = 1  # place p1 paddle
            self.field[width-1][i + (2 * paddle_len)] = 1  # place p2 paddle
            p1_paddle_pos.append(i + (2 * paddle_len))
            p2_paddle_pos.append(i + (2 * paddle_len))

        self.ball = Ball(ball_x, ball_y)
        self.p1_paddle = Paddle(p1_paddle_pos, 2)  # start in the middle
        self.p2_paddle = Paddle(p2_paddle_pos, 2)  # start in the middle

    def print(self):
        """
        TODO: LOGAN
        Change to be a prettier GUI.
        """
        print('{}{:>37}'.format('Player 1', 'Player 2'))
        for row in range(self.height):
            x = []
            for item in range(self.width):
                x.append(self.field[item][row])
            print(x)
        print('\n')

    def is_paddle_move_valid(self, action, paddle):
        # NOTE: 0 is at the TOP of the grid
        valid = True
        if paddle.bottom + (action * paddle.length) >= self.height:
            valid = False
        if paddle.top + (action * paddle.length) < 0:
            valid = False
        return valid

    def move(self, p1_action, p2_action):
        if not self.is_paddle_move_valid(p1_action, self.p1_paddle):
            p1_action = 0
        if not self.is_paddle_move_valid(p2_action, self.p2_paddle):
            p2_action = 0
        self.move_paddles(p1_action, p2_action)
        self.move_ball()

    def move_paddles(self, p1_action, p2_action):
        for i in range(self.height):
            self.field[0][i] = 0
            self.field[self.width-1][i] = 0
        p1_pos = []
        p2_pos = []
        self.p1_paddle.pos_idx += p1_action
        for i in range(len(self.p1_paddle.position)):
            p1_pos.append(self.p1_paddle.position[i]
                          + (self.p1_paddle.length * p1_action))
            self.field[0][p1_pos[i]] = 1
        self.p2_paddle.pos_idx += p2_action
        for i in range(len(self.p2_paddle.position)):
            p2_pos.append(self.p2_paddle.position[i]
                          + (self.p2_paddle.length * p2_action))
            self.field[self.width-1][p2_pos[i]] = 1

        self.p1_paddle.update_position(p1_pos)
        self.p2_paddle.update_position(p2_pos)

    def move_ball(self):
        new_ball_y = self.ball.y_vel + self.ball.y_pos
        new_ball_x = self.ball.x_vel + self.ball.x_pos
        if new_ball_y < 0 or new_ball_y >= self.height:  # Hit a wall
            self.ball.y_vel = -self.ball.y_vel
            new_ball_y = self.ball.y_vel + self.ball.y_pos
        if new_ball_x >= self.width:  # P1 Scored
            self.result['Point Awarded'] = True
            self.result['Scorer'] = 0
            return
        elif new_ball_x < 0:  # P2 Scored
            self.result['Point Awarded'] = True
            self.result['Scorer'] = 1
            return
        elif self.field[new_ball_x][new_ball_y] == 1:  # Hit a paddle
            self.ball.x_vel = -self.ball.x_vel
            new_ball_x = self.ball.x_vel + self.ball.x_pos
            self.ball.y_vel = random.randint(-1, 1)
            new_ball_y = self.ball.y_vel + self.ball.y_pos
        if new_ball_y < 0 or new_ball_y >= self.height:  # Hit a wall
            self.ball.y_vel = -self.ball.y_vel
            new_ball_y = self.ball.y_vel + self.ball.y_pos
        self.field[self.ball.x_pos][self.ball.y_pos] = 0
        if not self.result['Point Awarded']:
            self.field[new_ball_x][new_ball_y] = 2
        self.ball.x_pos = new_ball_x
        self.ball.y_pos = new_ball_y

    def get_grid_state(self):
        return {
            'Player 1': self.p1_paddle.pos_idx,
            'Player 2': self.p2_paddle.pos_idx,
            'Ball Pos': [self.ball.x_pos, self.ball.y_pos]
            }

    def get_reward(self):
        if self.result['Point Awarded']:
            p1_reward = -1 if self.result['Scorer'] == 1 else 0
            p2_reward = -1 if self.result['Scorer'] == 0 else 0
            return {'P1 Reward': p1_reward, 'P2 Reward': p2_reward}
        else:
            return {'P1 Reward': 0, 'P2 Reward': 0}
