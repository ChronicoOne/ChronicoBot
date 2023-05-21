import streamGame as sg
import pygame 
from time import sleep
from random import randrange

framewait = 0.0167

class Ball:
    def __init__(self, pos, display):
        self.display = display
        self.pos = pos
        self.color = (255, 0, 255)
        self.radius = 20
        self.visible = True

    def draw(self):
        if self.visible:
            pygame.draw.circle(self.display, self.color, self.pos, self.radius) 
    
    def moveY(self, distance):
        self.pos = (self.pos[0], self.pos[1] + distance)

    def moveX(self, distance):
        self.pos = (self.pos[0] + distance, self.pos[1]) 
    



class Cup:
    def __init__(self, posX, posY, display, game):
        self.display = display
        self.game = game
        self.radius = 40
        self.color = (255, 0, 0)
        self.full = False
        self.speed = 5
        self.pos = (posX, posY)
        self.visible = True

    def draw(self):
        pygame.draw.circle(self.display, self.color, self.pos, self.radius) 

    def moveY(self, distance):
        self.pos = (self.pos[0], self.pos[1] + distance)

    def moveX(self, distance):
        self.pos = (self.pos[0] + distance, self.pos[1]) 
    
    def swap(self, cup):
        if self.pos[0] > cup.pos[0]:
            right_cup = self
            left_cup = cup
        else:
            left_cup = self
            right_cup = cup

        initialRightPos = right_cup.pos
        initialLeftPos = left_cup.pos

        isMovingX = left_cup.pos[0] < initialRightPos[0]
        
        halfway = initialLeftPos[0] + ((initialRightPos[0] - initialLeftPos[0]) / 2)

        while isMovingX:
            left_cup.moveX(self.speed)
            right_cup.moveX(-self.speed)
            if left_cup.pos[0] < halfway:
                left_cup.moveY(self.speed)
                right_cup.moveY(-self.speed)
            else:
                left_cup.moveY(-self.speed)
                right_cup.moveY(self.speed)

            isMovingX = left_cup.pos[0] < initialRightPos[0]
            self.game.draw()
            sleep(framewait)
        
        left_cup.pos = initialRightPos
        right_cup.pos = initialLeftPos

        self.game.draw()
        sleep(framewait)       

class CupGame:
    def __init__(self):
        self.display = sg.init_game_surface()
        self.raised_posY = 100
        self.start_posY = 250
        
        cup1 = Cup(125, self.raised_posY, self.display, self)
        cup2 = Cup(250, self.raised_posY, self.display, self)
        cup3 = Cup(375, self.raised_posY, self.display, self)

        self.cups = [cup1, cup2, cup3]
        self.speed = 5
        self.set_cup_speed()
        self.ball = Ball((250, 250), self.display)
        self.winner = None

    def draw(self):
        self.display.fill(sg.background_color)
        self.ball.draw()
        for cup in self.cups:
            cup.draw()
        pygame.display.flip()

    def random_swap(self):
        first_cup = randrange(3)
        second_cup = randrange(3)
        while second_cup == first_cup:
            second_cup = randrange(3)
        
        self.cups[first_cup].swap(self.cups[second_cup])
    
    def set_cup_speed(self):
        for cup in self.cups:
            cup.speed = self.speed

    def increase_speed(self, amount):
        self.speed += amount
        self.set_cup_speed()
    
    def reset(self):
        self.cups[0].pos = (125, self.raised_posY)
        self.cups[1].pos = (250, self.raised_posY)
        self.cups[2].pos = (375, self.raised_posY)

    def place_ball(self):
        self.reset()
        self.winner = randrange(3)
        ball_cup = self.cups[self.winner]
        initialPosList = [cup.pos for cup in self.cups]
        
        ball_cup.full = True
        self.ball.pos = (ball_cup.pos[0], self.start_posY)

        isAboveMin = ball_cup.pos[1] < self.start_posY

        while isAboveMin:
            
            for cup in self.cups:
                cup.moveY(2)
            
            self.draw()
            sleep(framewait)

            isAboveMin = ball_cup.pos[1] < self.start_posY
    
        for i in range(len(self.cups)):
            self.cups[i].pos = (initialPosList[i][0], self.start_posY)
     
        self.draw()
        self.ball.visible = False

    def end(self):
        ball_cup = self.cups[self.winner]
        self.ball.visible = True
        
        while ball_cup.pos[1] > self.raised_posY:
            for cup in self.cups:
                cup.moveY(-2)
            self.draw()
            sleep(framewait)

        self.reset()
        self.draw()

        return self.winner
    def play(self):
        self.place_ball()
        while self.speed < 17:
            self.draw()
            self.random_swap()
            self.increase_speed(0.25)
            sleep(framewait)

        for i in range(1000):
            self.draw()
            sleep(framewait)
