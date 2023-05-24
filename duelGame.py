import streamGame as sg
import pygame

class Player:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.color = (125, 125, 0)
        self.radius = 40

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.posX, self.posY), self.radius)

class DuelGame(sg.Game):
    def __init__(self, console):
        super().__init__(console, 'Duel')
        self.player1 = Player(100, 250)
        self.player2 = Player(400, 250)
        self.countDown = 100

    def draw(self):
        self.console.display.fill(self.console.background_color)
        self.player1.draw(self.console.display)
        self.player2.draw(self.console.display)
        pygame.display.flip()

    async def update(self):
        if self.countDown <= 0:
            self.running = False
        else:
            self.countDown -= 1

        return self.running
