import streamGame as sg
import pygame 
from time import sleep
from random import randrange

class Cup:
    def __init__(self, ID):
        self.color = (255, 0, 0)
        self.radius = 40
        self.ID = ID
        self.lastID = ID
        self.posX = ID * 125 
        self.posY = 250

    def place(self, x, y):
        self.posX = x
        self.posY = y
    
    def moveX(self, distance):
        self.posX += distance

    def moveY(self, distance):
        self.posY += distance

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.posX, self.posY), self.radius)

class CupGame(sg.Game):
    def __init__(self, console):
        super().__init__(console, 'Cups')
        self.votes = {}
        self.cups = [Cup(1), Cup(2), Cup(3)]
        self.speed = 5
        self.swapping = False

    def draw(self):
        self.console.display.fill(self.console.background_color)
        print("Cups:", [cup.ID for cup in self.cups])
        for cup in self.cups:
            cup.draw(self.console.display)
        pygame.display.flip()
    
    def update(self):
        if not self.swapping:
            self.swap()
        self.processInput()
        self.moveCups()
        return self.running
    
    def processInput(self):
        currentInput = self.getInput()
        while(currentInput != None):
            for user in currentInput:
                self.votes[user] = currentInput[user]
            currentInput = self.getInput()

    def increaseSpeed(self, amount):
        self.speed += amount

    def swap(self):
        self.swapping = True
        firstCupID = randrange(3) + 1
        secondCupID = randrange(3) + 1
        
        while(firstCupID == secondCupID):
            secondCupID = randrange(3) + 1
        
        for cup in self.cups:
            if cup.ID == firstCupID:
                cup.lastID = cup.ID
                cup.ID = secondCupID
            elif cup.ID == secondCupID:
                cup.lastID = cup.ID
                cup.ID = firstCupID
    
    def moveCups(self):
        for cup in self.cups:
            if cup.lastID != cup.ID:
                movingLeft = cup.ID < cup.lastID
                targetX = cup.ID * 125
                previousX = cup.lastID * 125
                halfwayX = (targetX - previousX) / 2
                movingUp = cup.posX < halfwayX + previousX
                
                if movingLeft:
                    cup.posX -= self.speed
                else:
                    cup.posX += self.speed

                if movingUp:
                    cup.posY += self.speed
                else:
                    cup.posY -= self.speed
                
                if abs(cup.posX - targetX) <= self.speed:
                    cup.posX = targetX
                    cup.posY = 250
                    cup.lastID = cup.ID
                    self.swapping = False
                
