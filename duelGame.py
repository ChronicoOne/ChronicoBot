import streamGame as sg
import userData as ud
import pygame
import gameUI as gui
from os.path import join 

class Player(ud.User):
    def __init__(self, name, posX, posY):
        
        super().__init__(name)
        self.posX = posX
        self.posY = posY
        self.color = (125, 125, 0)
        self.initial_size = (64, 64)
        self.size = (256, 256)
        self.replaced_color = pygame.Color(0, 0, 0)
        self.surface = self.load_model()

    def draw(self, display):
        display.blit(self.surface, (self.posX - (self.size[0] // 2), self.posY - (self.size[1] // 2)))
    
    def load_model(self):

        image_path = "images/duel_player_model.png" 
        surface = pygame.image.load(image_path)
        
        for j in range(self.initial_size[0]):
            for k in range(self.initial_size[1]):
                if surface.get_at((j,k)) == self.replaced_color:
                    surface.set_at((j,k), self.color)
               
        pants_name = self.get_pants()
        if pants_name != None:
            pants_path = join("images","pants", pants_name + ".png") 
            pants = pygame.image.load(pants_path)
            surface.blit(pants, (0,0))
        
        armor_name = self.get_armor()
        if armor_name != None:
            armor_path = join("images","armor", armor_name + ".png") 
            armor = pygame.image.load(armor_path)
            surface.blit(armor, (0,0))
        
        helmet_name = self.get_helmet()
        if helmet_name != None:
            helmet_path = join("images","helmets", helmet_name + ".png") 
            helmet = pygame.image.load(helmet_path)
            surface.blit(helmet, (0,0))
        
        surface = pygame.transform.scale(surface, self.size)
        surface = surface.convert_alpha()

        return surface
    
    def reflectX(self):
        self.surface = pygame.transform.flip(self.surface, True, False)

    def get_armor(self):
        if "dg_armor" in self:
            armor = self["dg_armor"]
        else:
            armor = None    
        return armor

    def get_helmet(self):
        if "dg_helmet" in self:
            helmet = self["dg_helmet"]
        else:
            helmet = None
        return helmet

    def get_pants(self):
        if "dg_pants" in self:
            pants = self["dg_pants"]
        else:
            pants = None
        return pants

ui_palette = {"black": (0, 0, 0),
                           "grey": (180, 180, 180),
                           "white": (255, 255, 255)}
       

class DuelGame(sg.Game):
    def __init__(self, console):
        super().__init__(console, 'Duel')

        player1, player2 = self.initPlayers()
        self.player1 = Player(player1, 100, 150)
        self.player2 = Player(player2, 400, 150)
        self.player2.reflectX()
        self.font = 'fonts/pixel.ttf'
        self.countDown = 10000
        self.topUI, self.botUI = self.initUI(self.console.display)        
    
    def initPlayers(self):
        user1 = self.getInput()
        user2 = self.getInput()
        
        return user1, user2

    def initUI(self, display):
        top_ui = gui.UIElement((490, 300),
                                margin_left="auto",
                                margin_top=5,
                                border_width=5,
                                border_radius=20,
                                border_color=ui_palette["white"],
                                color=ui_palette["black"],
                                parent=display) 

        bottom_ui = gui.UIElement((490, 200),
                                margin_left="auto",
                                margin_bottom=5,
                                border_width=5,
                                border_radius=20,
                                border_color=ui_palette["white"],
                                color=ui_palette["black"],
                                parent=display) 
        

        inner_bottom_ui = gui.UIElement((200, 100),
                                         margin_left="auto",
                                         margin_bottom="auto",
                                         border_width=5,
                                         border_radius=20,
                                         border_color=ui_palette["grey"],
                                         color = ui_palette["white"],
                                         parent=bottom_ui)
 
        attack_text = gui.UIText("Attack", inner_bottom_ui, ui_palette["black"],
                                 font_file=self.font,
                                 font_size=48, margin_top="auto", margin_right="auto") 
    
        return top_ui, bottom_ui

    def drawUI(self, display):

        self.topUI.draw(display)       
        self.botUI.draw(display)

    def draw(self):
        
        self.console.display.fill(self.console.background_color)
        self.drawUI(self.console.display)
        self.player1.draw(self.console.display)
        self.player2.draw(self.console.display)
        
        self.console.display.set_at((self.player1.posX, self.player1.posY), (0,0,0))
        pygame.display.flip()

    async def update(self):
        if self.countDown <= 0:
            self.running = False
        else:
            self.countDown -= 1

        return self.running
