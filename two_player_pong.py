from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, color, size, paddle1, paddle2):
        self.canvas = canvas
        self.id = canvas.create_rectangle(10, 10, size, size, fill=color) #create 10x10 ball
        self.canvas.move(self.id, 360, w/2)
        #self.xspeed = random.randrange(-3,3)
        #self.yspeed = random.randrange(-2,2)
        self.xspeed = -(w/32)
        self.yspeed = -(h/24)
        self.paddle1 = paddle1
        self.paddle2 = paddle2
        # while (self.xspeed==0):
        #     self.xspeed = random.randrange(-1,1) #make sure ball never gets stuck
        self.hit_sides = False
        self.hit_leftside = False
        self.hit_rightside = False
        
    def draw(self):
        self.canvas.move(self.id, self.xspeed, self.yspeed)
        pos = self.canvas.coords(self.id)
        # Bounce off of ceiling
        if pos[1] <= 0:
            self.yspeed = (h/24)
        # Bounce off of bottom
        if pos[3] >= h:
            self.yspeed = -(h/24)
        # Past left paddle
        if pos[0] <= 0:
            self.hit_sides = True
            self.hit_leftside=True
        # Past right paddle
        if pos[2] >= w:
            self.hit_sides = True
            self.hit_rightside = True
        # Hit Paddle 1
        if pos[0]>w/2-250 and self.hit_paddle1(pos,paddle1) == True:
            self.xspeed = -(w/32)
            self.yspeed = random.randint(-1,2) * (h/24) #bounce off at random angle
        # Hit Paddle 2
        if pos[0]<w/2+250 and self.hit_paddle2(pos,paddle2) == True:
                self.xspeed = (w/32)
                self.yspeed = random.randint(-1,2) * (h/24) #bounce off at random angle

    def hit_paddle1(self, pos, paddle):
        paddle1_pos = self.canvas.coords(self.paddle1.id)
        if pos[2] >= paddle1_pos[0] and pos[0] <= paddle1_pos[2]:
            if pos[3] >= paddle1_pos[1] and pos[3] <= paddle1_pos[3]:
                return True
        return False
    
    def hit_paddle2(self, pos, paddle2):
        paddle2_pos = self.canvas.coords(self.paddle2.id)
        if pos[2] >= paddle2_pos[0] and pos[0] <= paddle2_pos[2]:
            if pos[1] >= paddle2_pos[1] and pos[1] <= paddle2_pos[3]:
                return True
        return False

class Paddle:
    def __init__(self, canvas, color, width, player):
        self.canvas = canvas
        self.height = h
        self.width = width
        self.id = canvas.create_rectangle(0, 0, 15, h/5, fill=color)
        self.canvas.move(self.id, width, 0)
        self.yspeed = 0
        self.player=player
        if player==1:
            self.canvas.bind_all('<KeyPress-Up>', self.move_up)
            self.canvas.bind_all('<KeyPress-Down>', self.move_down)
           
        elif player==2:
            self.canvas.bind_all('<KeyPress-w>', self.move_up)
            self.canvas.bind_all('<KeyPress-s>', self.move_down)         

    def draw(self):
        # self.canvas.move(self.id, self.xspeed, self.yspeed)
        self.canvas.move(self.id, 0, self.yspeed)
        pos = self.canvas.coords(self.id)
        print(pos[1], pos[3])

        # Paddle at top
        if pos[1] < 0:
            print("beyond north")
            self.yspeed = 0

        # Paddle at bottom
        if pos[3] > h:
            print("beyond south")
            self.yspeed = 0

    def move_up(self, evt):
        self.canvas.move(self.id, 0, self.yspeed)
        pos = self.canvas.coords(self.id)
        self.yspeed = -(h)/5
        if not (pos[1] <= 0): # Not past top
            self.canvas.move(self.id, 0, self.yspeed)
        self.yspeed = 0

    def move_down(self, evt):
        self.canvas.move(self.id, 0, self.yspeed)
        pos = self.canvas.coords(self.id)
        self.yspeed = (h)/5
        if not (pos[3] >= h): # Not past bottom
            self.canvas.move(self.id, 0, self.yspeed)
        self.yspeed = 0



score=0
score2=0
while(True):
    tk = Tk()
    tk.title("My pong game")
    h=480
    w=640

    canvas = Canvas(tk, width=w, height=h, bg='black')
    canvas.pack()
    tk.update()
    paddle1 = Paddle(canvas, 'White', w-15, 1)
    paddle2= Paddle(canvas, 'White', 5, 2)
    ball = Ball(canvas, 'white', 25, paddle1, paddle2)
    # canvas.create_line(w/2+2,0,w/2+2,h,fill="white",width=4, dash=(2, 4))

    # label = canvas.create_text(w/2-50, 5, anchor=NW, text=score,fill="white", font=("Ani",50))
    # label = canvas.create_text(w/2+15, 5, anchor=NW, text=score2,fill="white",font=("Ani",50))
    while ball.hit_sides == False:
        ball.draw()
        paddle1.draw()
        paddle2.draw()
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)
        if ball.hit_leftside==True:
            score=score+1
            ball.hit_sides == False
            ball.hit_leftside==False
        elif ball.hit_rightside==True:
            score2=score2+1
            ball.hit_sides == False
            ball.hit_rightside==False

            
# Game Over
    if score==1:
        go_labwel = canvas.create_text(w/2,h/2,text="P1 WON",font=("Cantarell Ultra-Bold",40), fill="White")
        ball.hit_sides == True
        tk.update()
        time.sleep(2)
        tk.destroy
        break
    elif score2==1:
        go_label = canvas.create_text(w/2,h/2,text="P2 WON",font=("Cantarell Ultra-Bold",40), fill="White")
        tk.update()
        time.sleep(2)
        tk.destroy
        break
    else:
        go_label = canvas.create_text(w/2,h/2,text="GAME OVER",font=("Cantarell Ultra-Bold",40), fill="White")
        tk.update()
        time.sleep(2)
        ball.hit_sides=False;
        tk.destroy()
