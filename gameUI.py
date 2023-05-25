import pygame

class UIElement:
    def __init__(self, size,
                pos=(0,0),
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
        
        self.positioned_right = False
        self.positioned_bottom = False
        self.autoX = margin_left == "auto" or margin_right == "auto" 
        self.autoY = margin_top == "auto" or margin_bottom == "auto" 
        
        if self.autoX:
            if self.parent == None:
                print("Unable to detect size of parent for auto margin (parent == None)")
                self.margin_left = 0
            else:
                 self.margin_left = (self.parent.get_width() // 2) - (self.width // 2)
        else:
            self.margin_left = margin_left
        
        if self.autoY:
            if self.parent == None:
                print("Unable to detect size of parent for auto margin (parent == None)")
                self.margin_top = 0
            else:
                 self.margin_top = (self.parent.get_height() // 2) - (self.height // 2)
        else:
            self.margin_top = margin_top
        
        if not margin_bottom in [None, "auto"]:
            if self.parent == None:
                print("Unable to detect size of parent for bottom margin (parent == None)")
            else:
                self.positioned_bottom = True
                self.margin_top = self.parent.get_height() - self.height - margin_bottom

        if not margin_right in [None, "auto"]:
            if self.parent == None:
                print("Unable to detect size of parent for right margin (parent == None)")
            else:
                self.positioned_right = True
                self.margin_left = self.parent.get_width() - self.width - margin_right

 
        self.posX = posX + self.margin_left
        self.posY = posY + self.margin_top

        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color
        
        if isinstance(self.parent, UIElement):
            self.posX += self.parent.posX
            self.posY += self.parent.posY
            self.parent.append_children([self])
        
        self.outer_rect, self.inner_rect = self.init_rects()


    def init_rects(self):
        surface = pygame.Surface((self.width, self.height))
        
        outer_rect = None

        if self.border_width > 0:
            outer_rect = pygame.Rect(self.posX, self.posY, self.width, self.height)
            
        inner_rect = pygame.Rect(self.posX + self.border_width, self.posY + self.border_width,
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
        
class UIText(UIElement):
    def __init__(self, text, parent,
                 text_color=(255,255,255),
                 font_file="fonts/pixel.ttf",
                 font_size=48,
                 margin_left=0,
                 margin_top=0,
                 margin_right=None,
                 margin_bottom=None):

        self.font = self.font = pygame.font.Font(font_file, font_size)
        self.text_color = text_color
        self.text = text
        self.rendered_text = self.render_text()
        
        super().__init__(size=(self.rendered_text.get_width(),
                self.rendered_text.get_height()),
                margin_left=margin_left, margin_top=margin_top, 
                margin_right=margin_right, margin_bottom=margin_bottom,
                parent=parent)
        
        if self.positioned_right and not self.autoX:
            self.posX -= self.parent.border_width
        elif not self.autoX:
            self.posX += self.parent.border_width

        if self.positioned_bottom and not self.autoY:
            self.posY -= self.parent.border_width
        elif not self.autoY:
            self.posY += self.parent.border_width

    def render_text(self):
        return self.font.render(self.text, True, self.text_color, None) 
    
    def draw(self, display):           
        display.blit(self.rendered_text, 
                     (self.posX, self.posY))

