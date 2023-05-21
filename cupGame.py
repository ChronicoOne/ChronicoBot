import streamGame as sg
import pygame 
from time import sleep
from random import randrange

class CupGame(sg.Game):
    def __init__(self, console):
        super().__init__(console, 'Cups')
        self.votes = {}

    def draw(self):
        print("Votes:", self.votes)

    def update(self):
        currentInput = self.getInput()
        while(currentInput != None):
            for user in currentInput:
                self.votes[user] = currentInput[user]
            currentInput = self.getInput()
        return self.running

    
