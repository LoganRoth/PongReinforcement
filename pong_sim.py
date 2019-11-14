import sys
import random
import argparse
from time import sleep


class Ball:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = -1 if random.randint(0, 1) == 0 else 1
        self.y_vel = random.randint(-1, 1)


class Paddle:
    def __init__(self, position: list):
        self.position = position
        self.top = min(position)
        self.bottom = max(position)
        self.length = len(position)

    def update_position(self, position: list):
        self.position = position
        self.top = min(position)
        self.bottom = max(position)


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
        paddle_len = int(height/5)
        for i in range(paddle_len):
            self.field[0][i + (2 * paddle_len)] = 1  # place p1 paddle
            self.field[width-1][i + (2 * paddle_len)] = 1  # place p2 paddle
            p1_paddle_pos.append(i + (2 * paddle_len))
            p2_paddle_pos.append(i + (2 * paddle_len))

        self.ball = Ball(ball_x, ball_y)
        self.p1_paddle = Paddle(p1_paddle_pos)
        self.p2_paddle = Paddle(p2_paddle_pos)

    def print(self):
        print('{}{:>37}'.format('Player 1', 'Player 2'))
        for row in range(self.height):
            x = []
            for item in range(self.width):
                x.append(self.field[item][row])
            print(x)
        print('\n')

    def is_paddle_move_valid(self, action, paddle):
        # NOTE: 0 is at the TOP of the printed grid
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
        for i in range(len(self.p1_paddle.position)):
            p1_pos.append(self.p1_paddle.position[i]
                          + (self.p1_paddle.length * p1_action))
            self.field[0][p1_pos[i]] = 1
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
        elif new_ball_x < 0:  # P2 Scored
            self.result['Point Awarded'] = True
            self.result['Scorer'] = 1
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


class Game:
    def __init__(self, width, height, agent1, agent2):
        self.grid = Grid(width, height)
        self.players = [agent1, agent2]

    def playGame(self):
        game_over = False
        winner = -1
        if self.players[0].watch or self.players[1].watch:
            self.grid.print()
        while not game_over:
            game_over, winner = self.game_step()
            if self.players[0].watch or self.players[1].watch:
                self.grid.print()
                if not self.players[0].alive and not self.players[1].alive:
                    sleep(1)  # Only need to sleep if both are AI
        if self.players[0].watch or self.players[1].watch:
            print('-------------------------------{} won!-------------------'
                  '------------\n'.format(self.players[winner].name))
        self.players[winner].wins += 1

    def game_step(self):
        p1_action = self.players[0].get_action()
        p2_action = self.players[1].get_action()
        self.grid.move(p1_action, p2_action)
        return self.grid.result['Point Awarded'], self.grid.result['Scorer']


class Player:
    def __init__(self, name, alive, watch):
        self.name = name
        self.alive = alive
        self.watch = watch
        self.wins = 0

    def get_action(self):
        """
        To be overloaded by the child class
        """
        pass


class Human(Player):
    def __init__(self, name):
        super().__init__(name, True, True)

    def get_action(self):
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
    def __init__(self, name, watch=False):
        super().__init__(name, False, watch)
        self.qtable = []

    def get_action(self):
        return random.randint(-1, 1)


def parse_args():
    parser = argparse.ArgumentParser(usage='pong_sim.py --p1=[AI, Human] '
                                           '--p2=[AI, Human] [options]')
    parser.add_argument(
        '--p1',
        action='store',
        default='Human',
        help='Set if p1 should be an AI or a Human',
    )
    parser.add_argument(
        '--p2',
        action='store',
        default='Human',
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
        default=1,
        help='Set the number of games to play to train the comupter.'
    )
    args = parser.parse_args()
    return args.p1, args.p2, args.watch, int(args.train)


def main():
    p1_type, p2_type, watch, train = parse_args()
    if p1_type == 'AI':
        p1 = AI('Player 1', watch)
    elif p1_type == 'Human':
        p1 = Human('Player 1')
    else:
        print('Invalid selection for P1')
        return
    if p2_type == 'AI':
        p2 = AI('Player 2', watch)
    elif p2_type == 'Human':
        p2 = Human('Player 2')
    else:
        print('Invalid selection for P2')
        return
    for i in range(train):
        game = Game(15, 10, p1, p2)
        game.playGame()
    print('P1 Wins: {}\nP2 Wins: {}'.format(p1.wins, p2.wins))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Aborting')
    sys.exit(0)
