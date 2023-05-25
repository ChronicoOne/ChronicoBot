import streamGame as sg
import pygame

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

        top_ui_rect_outer = pygame.Rect((5,5), (490, 305))
        pygame.draw.rect(display, 
                         self.ui_palette["grey"], 
                         top_ui_rect_outer,
                         border_radius=20)
        

        top_ui_rect_inner = pygame.Rect((10,10), (480, 295))
        pygame.draw.rect(display, 
                         self.ui_palette["black"], 
                         top_ui_rect_inner,
                         border_radius=20)
        
         

        bottom_ui_rect_outer = pygame.Rect((5,305), (490, 190))
        pygame.draw.rect(display, 
                         self.ui_palette["grey"], 
                         bottom_ui_rect_outer,
                         border_radius=20)

        bottom_ui_rect_inner = pygame.Rect((10,310), (480, 180))
        pygame.draw.rect(display, 
                         self.ui_palette["black"], 
                         bottom_ui_rect_inner,
                         border_radius=20)

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
