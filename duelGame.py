import streamGame as sg
import userData as ud
import pygame
import gameUI as gui
from os.path import join 
from colors import stringToColor, colorSurface

ui_palette = {"black": (0, 0, 0),
                           "grey": (180, 180, 180),
                           "white": (255, 255, 255)}
 
class Spell:
    def __init__(self, player, name, description, baseDamage, parent=None):
        self.damage = baseDamage + player.get_magic_damage()
        self.name = name
        self.description = description
        self.UIElement = None
        self.initUI(parent)
    
    def initUI(self, parent):
        if parent == None:
            self.UIElement = None
            return -1

        outer_box = gui.UIElement((230, 50),
                                  margin_top=20,
                                  color=ui_palette["black"],
                                  parent=parent) 
        
        bullet_point = gui.UIElement((15, 15),
                                     margin_left=5, margin_top=15,
                                     color=ui_palette["white"],
                                     parent=outer_box)

        title_text = gui.UIText(self.name, outer_box, font_size=24, margin_left=30)
        desc_text = gui.UIText(self.description, outer_box, font_size=18, 
                               margin_left=30, margin_top=30)
        self.UIElement = outer_box

    def draw(self, display):
        self.UIElement.draw(display)

class FireBall(Spell):
    def __init__(self, player, parent=None):
        super().__init__(player, 
                         "FireBall",
                         "Shoot a FireBall at enemy",
                         10,
                         parent=parent)

class Player(ud.User):
    def __init__(self, name, posX, posY):
        super().__init__(name)
        self.posX = posX
        self.posY = posY
        self.initial_size = (64, 64)
        self.size = (256, 256)
        self.default_color = pygame.Color(50,50,50)
        self.surface = self.load_model()
        self.spells = self.get_spells()
        self.health = self.get_max_health()
    def draw(self, display):
        display.blit(self.surface, (self.posX - (self.size[0] // 2), self.posY - (self.size[1] // 2)))
    
    def load_model(self):

        image_path = "images/duel_player_model.png" 
        surface = pygame.image.load(image_path)
        surface = surface.convert_alpha()

        colorSurface(surface, self.get_player_color())

        pants_name = self.get_pants()
        if pants_name != None:
            pants_path = join("images","pants", pants_name + ".png") 
            pants = pygame.image.load(pants_path)
            pants = pants.convert_alpha()
            colorSurface(pants, self.get_pants_color())
            surface.blit(pants, (0,0))
        
        armor_name = self.get_armor()
        if armor_name != None:
            armor_path = join("images","armor", armor_name + ".png") 
            armor = pygame.image.load(armor_path)
            colorSurface(armor, self.get_armor_color())
            surface.blit(armor, (0,0))
        
        helmet_name = self.get_helmet()
        if helmet_name != None:
            helmet_path = join("images","helmets", helmet_name + ".png") 
            helmet = pygame.image.load(helmet_path)
            colorSurface(helmet, self.get_helmet_color())
            surface.blit(helmet, (0,0))
        
        surface = pygame.transform.scale(surface, self.size)
        surface = surface.convert_alpha()

        return surface
    
    def reflectX(self):
        self.surface = pygame.transform.flip(self.surface, True, False)

    def get_player_color(self):
        if "dg_player_color" in self:
            return stringToColor(self["dg_player_color"])
        else:
            return self.default_color

    def get_armor(self):
        if "dg_armor" in self:
            armor = self["dg_armor"]
        else:
            armor = None    
        return armor
    
    def get_armor_color(self):
        if "dg_armor_color" in self:
            return stringToColor(self["dg_armor_color"])
        else:
            return self.default_color

    def get_helmet(self):
        if "dg_helmet" in self:
            helmet = self["dg_helmet"]
        else:
            helmet = None
        return helmet

    def get_helmet_color(self):
        if "dg_helmet_color" in self:
            return stringToColor(self["dg_helmet_color"])
        else:
            return self.default_color

    def get_pants(self):
        if "dg_pants" in self:
            pants = self["dg_pants"]
        else:
            pants = None
        return pants
    
    def get_pants_color(self):
        if "dg_pants_color" in self:
            return stringToColor(self["dg_pants_color"])
        else:
            return self.default_color

    def get_spells(self):
        if "dg_spells" in self:
            spells = self["dg_spells"]
            spell_list = []
            
            if "fireball" in spells.split(','):
                 spell_list.append(FireBall(self))
            
            return spell_list 
        else:
            return []

    def get_magic_damage(self):
        if "dg_magic_damage" in self:
            return int(self["dg_magic_damage"])
        else:
            return 0

    def get_max_health(self):
        if "dg_max_health" in self:
            return int(self["dg_max_health"])
        else:
            return 50
    
class DuelGame(sg.Game):
    def __init__(self, console):
        super().__init__(console, 'Duel')

        player1, player2 = self.initPlayers()
        self.player1 = Player(player1, 100, 150)
        self.player2 = Player(player2, 400, 150)
        self.player2.reflectX()
        self.countDown = 10000
        self.UI = UI(self.console.display)
        self.UI.initPlayer(self.player1)
        self.UI.initPlayer(self.player2)

    def initPlayers(self):
        user1 = self.getInput()
        user2 = self.getInput()
        
        return user1, user2

    def draw(self):
        
        self.console.display.fill(self.console.background_color)
        self.UI.draw(self.console.display)
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
    
class UI:
    def __init__(self, display):
        self.topUI = self.initTop(display)
        self.bottomUI = self.initBottom(display)
        self.font = 'fonts/pixel.ttf'
    
    def initTop(self, display):
        topUI = gui.UIElement((490, 300),
                                margin_left="auto",
                                margin_top=5,
                                border_width=5,
                                border_radius=20,
                                border_color=ui_palette["white"],
                                color=ui_palette["black"],
                                parent=display) 

        return topUI

    def initBottom(self, display):
        bottomUI = gui.UIElement((490, 200),
                                margin_left="auto",
                                margin_bottom=5,
                                border_width=5,
                                border_radius=20,
                                border_color=ui_palette["white"],
                                color=ui_palette["black"],
                                parent=display) 
        return bottomUI
    
    def initPlayer(self, player):
        for spell in player.spells:
            spell.initUI(self.bottomUI)
        

    def draw(self, display):
        self.topUI.draw(display)
        self.bottomUI.draw(display)
