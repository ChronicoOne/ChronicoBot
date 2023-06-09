import pygame
from twitchio.ext import commands
from time import sleep
import asyncio

screen_size = (500, 500)
background_color = (0, 255, 0)
framewait = 0.0167

class ActionQ:
    def __init__(self):
        self.queue = []
    
    def push(self, action):
        self.queue.insert(0, action)

    def pop(self):
        return self.queue.pop()
    
    def clear(self):
        self.queue = []

    def isEmpty(self):
        return len(self.queue) == 0

class ChroniConsole:
    def __init__(self, ID, ctx=None, size=screen_size):
        self.ID = ID
        self.background_color = background_color
        self.display = self.init_game_surface(size)
        self.game = None
        self.ctx = ctx
        self.inputQ = ActionQ()
        self.outputQ = ActionQ()
        
    def init_game_surface(self, size):
        pygame.init()

        display = pygame.display.set_mode(size=size)
        
        display.fill(self.background_color)
        
        pygame.display.set_caption("ChroniConsole " + str(self.ID))
        pygame.display.flip()

        return display

    async def insert(self, GameClass, ctx):
        if self.game != None:
            print("ERROR: Cannot insert game into ChroniConsole! A game is already inserted...")
            return -1

        self.display.fill(self.background_color)
        pygame.display.flip()
        self.game = GameClass(self)
        self.ctx = ctx
        insert_response = f"Inserted \"{self.game.title}\" into the ChroniConsole"
        print(insert_response)
        await self.ctx.reply(insert_response)

    def eject(self):
        if self.game == None:
            print("ERROR: Cannot Eject game from ChroniConsole! No game inserted into the ChroniConsole")
            return -1

        if self.game.running:
            print("ERROR: Cannot Eject game from ChroniConsole! Game is still running...")
            return -1

        ejected_name = self.game.title
        self.game = None
        self.display.fill(self.background_color)
        pygame.display.flip()
        self.inputQ.clear()
        self.outputQ.clear()

        print(f"Ejected \"{ejected_name}\" from the ChroniConsole")    
    
    async def play(self):
        while(await self.update()):
            self.game.draw()
            await asyncio.sleep(framewait)
        return 1

    async def update(self):
        return await self.game.update()

    async def run(self):
        if self.game == None:
            print("ERROR: Cannot play game! No game inserted into ChroniConsole...")
            return -1
        if self.game.running:
            print("ERROR: Cannot play game! Game is already running...")
            return -1
        
        self.game.running = True

        return await self.play()    
    
    def getInput(self):
        if self.inputQ.isEmpty():
            return None
        return self.inputQ.pop()

    async def awaitInput(self, term1, term2=None, waitTime=1200):
        countDown = waitTime
        while True:
            currentInput = self.getInput()
            if currentInput != None and term1 in currentInput:
                if term2 != None:
                    if currentInput[term1].upper() == term2.upper():
                        return currentInput
                else:
                    return currentInput

            countDown -= 1
            if countDown < 0:
                return None

            await asyncio.sleep(framewait)
            
        return currentInput

    def pushInput(self, action):
        self.inputQ.push(action)

    def pushOutput(self, action):
        self.outputQ.push(action)
     
    def getOutput(self):
        if self.outputQ.isEmpty():
            return None
        return self.outputQ.pop()

class Game:
    def __init__(self, console, title):
        self.console = console
        self.title = title
        self.running = False

    def update(self):
        return self.running
    
    def getInput(self):
        return self.console.getInput()

    def pushOutput(self, action):
        self.console.pushOutput(action)
    
    async def awaitInput(self, term):
        return await self.console.awaitInput(term)
