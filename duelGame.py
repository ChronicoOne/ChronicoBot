import streamGame as sg
import pygame
import gameUI as gui

class Player:
    def __init__(self, posX, posY):
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
        surface = surface.convert_alpha()

        for j in range(self.initial_size[0]):
            for k in range(self.initial_size[1]):
                if surface.get_at((j,k)) == self.replaced_color:
                    surface.set_at((j,k), self.color)
        
        surface = pygame.transform.scale(surface, self.size)

        return surface
    
    def reflectX(self):
        self.surface = pygame.transform.flip(self.surface, True, False)

class DuelGame(sg.Game):
    def __init__(self, console):
        super().__init__(console, 'Duel')
        self.ui_palette = {"black": (0, 0, 0),
                           "grey": (180, 180, 180),
                           "white": (255, 255, 255)}
        self.player1 = Player(100, 150)
        self.player2 = Player(400, 150)
        self.player2.reflectX()
        self.font = pygame.font.Font('fonts/pixel.ttf', 48)
        self.countDown = 10000

    def drawUI(self, display):

        top_ui = gui.UIElement((0,0), 
                                (490, 300),
                                margin_left="auto",
                                margin_top=5,
                                border_width=5,
                                border_radius=20,
                                border_color=self.ui_palette["white"],
                                color=self.ui_palette["black"],
                                parent=display) 

        top_ui.draw(display)

        bottom_ui = gui.UIElement((0,0), 
                                (490, 200),
                                margin_left="auto",
                                margin_bottom=5,
                                border_width=5,
                                border_radius=20,
                                border_color=self.ui_palette["white"],
                                color=self.ui_palette["black"],
                                parent=display) 
        
        inner_bottom_ui = gui.UIElement((0,0),
                                         (200, 100),
                                         margin_left="auto",
                                         margin_bottom=10,
                                         border_width=5,
                                         border_color=self.ui_palette["grey"],
                                         color = self.ui_palette["white"],
                                         parent=bottom_ui)

        bottom_ui.draw(display)

        attack_text = self.font.render("Attack", True, self.ui_palette["white"], None)
        
        display.blit(attack_text, (15, 315))  
        

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
