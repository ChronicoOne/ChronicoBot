import streamGame as sg
import pygame 
from time import sleep
from random import randrange

class CupGame(sg.Game):
    def __init__(self, console):
        super().__init__(console, 'Cups')

    def draw(self):
        print("Drawing")

    def update(self):
        currentOutput = self.getInput()
        while(currentOutput != None):
            if list(currentOutput.values())[0] == "end":
                self.running = False
            currentOutput = self.console.getOutput()
        return self.running

    
