import pygame
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

class ChroniConsole:
    def __init__(self, size=screen_size):
        self.display = self.init_game_surface(size)
        self.game = None
        self.inputQ = ActionQ()
        self.outputQ = ActionQ()
        
    def init_game_surface(self, size):
        pygame.init()

        display = pygame.display.set_mode(size=size)

        display.fill(background_color)
        
        pygame.display.flip()

        return display

    def insert(self, GameClass):
        if self.game != None:
            print("ERROR: Cannot insert game into ChroniConsole! A game is already inserted...")
            return -1

        self.display.fill(background_color)
        pygame.display.flip()
        self.game = GameClass(self)
        print(f"Inserted {self.game.title} into the ChroniConsole")

    def eject(self):
        if self.game == None:
            print("ERROR: Cannot Eject game from ChroniConsole! No game inserted into the ChroniConsole")
            return -1

        if self.game.running:
            print("ERROR: Cannot Eject game from ChroniConsole! Game is still running...")
            return -1

        ejected_name = self.game.title
        self.game = None
        self.display.fill(background_color)
        pygame.display.flip()
        print(f"Ejected {ejected_name} from the ChroniConsole")    
    
    async def play(self):
        while(await self.update()):
            self.game.draw()
            await asyncio.sleep(framewait)
        return 1

    async def update(self):
        return self.game.update()

    async def run(self):
        if self.game == None:
            print("ERROR: Cannot play game! No game inserted into ChroniConsole...")
            return -1
        if self.game.running:
            print("ERROR: Cannot play game! Game is already running...")
            return -1
        
        self.game.running = True

        return await self.play()    

    def pushInput(self, action):
        self.inputQ.push(action)
        print(self.inputQ.queue)

    def getOutput(self, action):
        return self.outputQ.pop()

class Game:
    def __init__(self, console, title):
        self.console = console
        self.title = title
        self.running = False

    def update(self):
        return self.running
    
    def getInput(self):
        return self.console.inputQ.pop()

    def pushOutput(self, action):
        self.outputQ.push(action)
         
