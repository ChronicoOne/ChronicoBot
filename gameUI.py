import pygame

class UIElement:
    def __init__(self, pos, size, 
                color=(255,255,255), 
                margin_left=0, margin_top=0, margin_right=None, margin_bottom=None,
                border_width=0, border_radius=0, border_color=(0,0,0),
                parent=None):
        
        (posX, posY) = pos
        (width, height) = size
        self.parent = parent
        self.children = []
        self.width = width
        self.height = height
        self.color = color
        
        if margin_left == "auto":
            if self.parent == None:
                print("Unable to detect size of parent for auto margin (parent == None)")
                self.margin_left = 0
            else:
                 self.margin_left = (self.parent.get_width() // 2) - (self.width // 2)
        else:
            self.margin_left = margin_left
        
        if margin_top == "auto":
            if self.parent == None:
                print("Unable to detect size of parent for auto margin (parent == None)")
                self.margin_top = 0
            else:
                 self.margin_top = (self.parent.get_height() // 2) - (self.height // 2)
        else:
            self.margin_top = margin_top
        
        if margin_bottom != None:
            if self.parent == None:
                print("Unable to detect size of parent for bottom margin (parent == None)")
            else:
                self.margin_top = self.parent.get_height() - self.height - margin_bottom

        if margin_right != None:
            if self.parent == None:
                print("Unable to detect size of parent for right margin (parent == None)")
            else:
                self.margin_top = self.parent.get_width() - self.width - margin_right

 
        self.posX = posX + self.margin_left
        self.posY = posY + self.margin_top

        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color
        self.outer_rect, self.inner_rect = self.init_rects()

        if isinstance(self.parent, UIElement):
            self.parent.append_children([self])

    def init_rects(self):
        surface = pygame.Surface((self.width, self.height))
        
        outer_rect = None

        posX = self.posX
        posY = self.posY

        if isinstance(self.parent, UIElement):
            posX += self.parent.posX
            posY += self.parent.posY

        if self.border_width > 0:
            outer_rect = pygame.Rect(posX, posY, self.width, self.height)
            
        inner_rect = pygame.Rect(posX + self.border_width, posY + self.border_width,
                                 self.width - (self.border_width * 2),
                                 self.height - (self.border_width * 2))
        
        return outer_rect, inner_rect
    
    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def append_children(self, children):
        for child in children:
            child.parent = self
            self.children.append(child)
    
    def draw(self, display):
        
        if self.outer_rect != None:
            pygame.draw.rect(display, self.border_color, self.outer_rect, 
                             border_radius=self.border_radius)
        
        pygame.draw.rect(display, self.color, self.inner_rect,
                         border_radius=self.border_radius)
        
        for child in self.children:
            child.draw(display)
        

