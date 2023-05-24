import streamGame as sg
import pygame 
from time import sleep
from random import randrange

class Ball:
    def __init__(self, posX):
        self.posX = posX
        self.color = (200, 0, 200)
        self.radius = 20
        self.visible = True

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.posX, 250), self.radius)

class Cup:
    def __init__(self, ID):
        self.color = (255, 0, 0)
        self.radius = 40
        self.ID = ID
        self.lastID = ID
        self.posX = ID * 125 
        self.posY = 100
        self.ball = None

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
        self.winnerCup = None
        self.ball = Ball(250)
        self.speed = 5
        self.maxSpeed = 16
        self.countDown = 700
        self.swapping = False
        self.revealing = False
        self.ending = False
        self.reset()

    def draw(self):
        self.console.display.fill(self.console.background_color)
        
        if self.ball.visible:
            self.ball.draw(self.console.display)

        for cup in self.cups:
            cup.draw(self.console.display)

        pygame.display.flip()
    
    async def update(self):
        self.processInput()

        if self.revealing and not self.swapping:
            self.moveCups(100)
        elif not self.ending:
            if not (self.swapping or self.ball.visible):
                self.swap()
            self.increaseSpeed(0.025)
            self.moveCups(250)
        
        if self.speed >= self.maxSpeed and not(self.swapping or self.ending):
            self.ending = True
            await self.console.ctx.send("Vote for which cup contains the ball! | ?vote (1, 2, or 3)")

        if self.ending:
            if self.countDown == 0:
                await self.announceWinners()
                self.ball.visible = True
                self.ball.posX = self.winnerCup.posX
                self.revealing = True
                self.countDown -= 1
            else:
                self.countDown -= 1

        return self.running
    
    def processInput(self):
        currentInput = self.getInput()
        while(currentInput != None):
            for user in currentInput:
                self.votes[user] = currentInput[user]
            currentInput = self.getInput()

    def increaseSpeed(self, amount):
        self.speed += amount
    
    def reset(self):
        self.speed = 5
        self.cups = [Cup(1), Cup(2), Cup(3)]
        self.winnerCup = self.cups[randrange(3)]
        self.ball.posX = self.winnerCup.posX
        self.votes = {}
        self.countDown = 700
        self.revealing = False
        self.swapping = False
        self.ending = False

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
    
    def getWinners(self):
        
        self.swapping = False
        winners = []

        for user in self.votes:
            if self.votes[user] == str(self.winnerCup.ID):
                winners.append("@" + user) 
        
        return winners

    async def announceWinners(self):
        winners = self.getWinners()
        winnerString = ", ".join(winners)
        if len(winners) > 0:
            await self.console.ctx.send(f"Congrats to {winnerString} for winning Cups!")
        else:
            await self.console.ctx.send("Cups game ended with no winners!")
        return 1 


    def moveCups(self, returnY):
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
                    cup.posY = returnY
                    cup.lastID = cup.ID
                    self.swapping = False
            
            elif abs(cup.posY - returnY) <= 3:
                cup.posY = returnY
                if self.revealing:
                    self.running = False
                else:
                    self.ball.visible = False

            elif cup.posY > returnY and not self.swapping:
                cup.posY -= 1
            elif cup.posY < returnY and not self.swapping:
                cup.posY += 1 

