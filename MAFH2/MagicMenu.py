import pygame
from fortuneengine.GameEngineElement import GameEngineElement

from constants import MENU_PATH, PUZZLE_PATH
from gettext import gettext as _

NORMAL_MENU = 1
GRID_MENU = 2

class MagicMenuHolder( GameEngineElement ):
    def __init__(self, callback):
        GameEngineElement.__init__(self, has_draw=True, has_event=False)
        self.menu = None
        self.callback = callback
        self.background = pygame.image.load(MENU_PATH + "battleMenubackground.gif")

    def remove_from_engine(self):
        super( MagicMenuHolder, self ).remove_from_engine()
        self.clear_menu()
        
    def draw(self, screen):
        screen.blit(self.background,(0,286,452,414))
        #draw the boxes with the specific magic icons randomly
        
    def menu_called(self, id):
        self.callback(id, self)

    def clear_menu(self):
        if self.menu:
            self.menu.remove_from_engine()
            self.menu = None
            
    def show_menu(self,id):
        if self.is_in_engine():
            self.clear_menu()
        else:
            self.add_to_engine()
        
        
        #example of what will come  
        if id == "fire":
            menu_type = GRID_MENU
            spell_type = 0
            menu_options = [
                        [_('1'), lambda: self.menu_called("fire1"), 140,1],
                        [_('2'), lambda: self.menu_called("fire2"), 140,1],
                        [_('3'), lambda: self.menu_called("fire3"), 140,1],
                        [_('4'), lambda: self.menu_called("fire4"), 140,1],
                        [_('5'), lambda: self.menu_called("fire5"), 140,1],
                        [_('6'), lambda: self.menu_called("fire6"), 140,1],
                        [_('7'), lambda: self.menu_called("fire7"), 140,1],
                        [_('8'), lambda: self.menu_called("fire8"), 140,1]
            ]
        self.menu = MagicMenu(menu_options, 237, 375, menu_type)

class MagicMenu(GameEngineElement):
    def __init__(self, magic_menu, x, y, type):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)

        self.menu = Menu(magic_menu, type )

        self.menu.set_pos(x, y)
        self.add_to_engine()

    def event_handler(self, event):
        return self.menu.update(event)

    def draw(self, screen):
        self.menu.draw( screen )

#not finished
class Menu(object):
    def __init__(self, options, cols, spelltype):
        """Initialize the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""

        self.options = options
        self.x = 0
        self.y = 0
        self.cols = cols
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        
        
        #btn1-4 will be correct buttons and btn5-8 will be incorrect
        
        if(spelltype == 0):
            self.btn1 = pygame.image.load(PUZZLE_PATH + "FireGlyph1btn.gif")
            self.btn2 = pygame.image.load(PUZZLE_PATH + "FireGlyph2btn.gif")
            self.btn3 = pygame.image.load(PUZZLE_PATH + "FireGlyph3btn.gif")
            self.btn4 = pygame.image.load(PUZZLE_PATH + "FireGlyph4btn.gif")
            
            #filler buttons
            self.btn5 = pygame.image.load(PUZZLE_PATH + "LigGlyph1btn.gif")
            self.btn6 = pygame.image.load(PUZZLE_PATH + "HealGlyph1btn.gif")
            self.btn7 = pygame.image.load(PUZZLE_PATH + "MissileGlyph1btn.gif")
            self.btn8 = pygame.image.load(PUZZLE_PATH + "LigGlyph2btn.gif")
            
        elif(spelltype == 1):
            #lightning attack
            self.btn1 = pygame.image.load(PUZZLE_PATH + "LigGlyph1btn.gif")
            self.btn2 = pygame.image.load(PUZZLE_PATH + "LigGlyph2btn.gif")
            self.btn3 = pygame.image.load(PUZZLE_PATH + "LigGlyph3btn.gif")
            self.btn4 = pygame.image.load(PUZZLE_PATH + "LigGlyph4btn.gif")
            
            self.btn5 = pygame.image.load(PUZZLE_PATH + "HealGlyph1btn.gif")
            self.btn6 = pygame.image.load(PUZZLE_PATH + "MissileGlyph1btn.gif")
            self.btn7 = pygame.image.load(PUZZLE_PATH + "FireGlyph1btn.gif")
            self.btn8 = pygame.image.load(PUZZLE_PATH + "FireGlyph2btn.gif")
            
        elif(spelltype == 2):
            #missile attack
            self.btn1 = pygame.image.load(PUZZLE_PATH + "MissileGlyph1btn.gif")
            self.btn2 = pygame.image.load(PUZZLE_PATH + "MissileGlyph2btn.gif")
            self.btn3 = pygame.image.load(PUZZLE_PATH + "MissileGlyph3btn.gif")
            self.btn4 = pygame.image.load(PUZZLE_PATH + "MissileGlyph4btn.gif")
    
            self.btn5 = pygame.image.load(PUZZLE_PATH + "HealGlyph1btn.gif")
            self.btn6 = pygame.image.load(PUZZLE_PATH + "LigGlyph1btn.gif")
            self.btn7 = pygame.image.load(PUZZLE_PATH + "FireGlyph1btn.gif")
            self.btn8 = pygame.image.load(PUZZLE_PATH + "FireGlyph2btn.gif")
        elif(spelltype == 3):
            #heal
            self.btn1 = pygame.image.load(PUZZLE_PATH + "HealGlyph1btn.gif")
            self.btn2 = pygame.image.load(PUZZLE_PATH + "HealGlyph2btn.gif")
            self.btn3 = pygame.image.load(PUZZLE_PATH + "HealGlyph3btn.gif")
            self.btn4 = pygame.image.load(PUZZLE_PATH + "HealGlyph4btn.gif")
            
            self.btn5 = pygame.image.load(PUZZLE_PATH + "LigGlyph1btn.gif")
            self.btn6 = pygame.image.load(PUZZLE_PATH + "MissileGlyph1btn.gif")
            self.btn7 = pygame.image.load(PUZZLE_PATH + "FireGlyph1btn.gif")
            self.btn8 = pygame.image.load(PUZZLE_PATH + "FireGlyph2btn.gif")
                            
        self.height = (len(self.options)*self.btn1.get_height()) / cols

    def draw(self, surface):
        """Draw the menu to the surface."""
        i=0 # Row Spacing
        h=0 # Selection Spacing
        j=0 # Col Spacing
        height = self.btn1.get_height()
        width = self.btn1.get_width()
        
        for o in self.options:
            if h==self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]

            newX = self.x + width * j
            newY = self.y + i * height
            surface.blit(self.btn1, (newX, newY) )
            
            #pygame.draw.rect(surface, (0, 74, 94), ( newX, newY, o[2], 44))
            #pygame.draw.rect(surface, (4, 119, 152), ( newX + 2, newY + 2, o[2]-4, 40))
            #surface.blit(ren, (newX + 15, newY + 12))

            j+=o[3]
            h+=1
            if j >= self.cols:
                i+=1
                j=0


    def update(self, event):
        """Update the menu and get input for the menu."""
        return_val = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.cols != 1:
                    self.option += self.cols
                else:
                    self.option += 1
                return_val = True
            elif event.key == pygame.K_UP:
                if self.cols != 1:
                    self.option -= self.cols
                else:
                    self.option -= 1
                return_val = True
            elif event.key == pygame.K_RIGHT:
                if self.cols != 1:
                    self.option += 1
                    return_val = True
            elif event.key == pygame.K_LEFT:
                if self.cols != 1:
                    self.option -= 1
                    return_val = True
            elif event.key == pygame.K_RETURN:
                self.options[self.option][1]()
                return_val = True

            self.option = self.option % len(self.options)

        return return_val

    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.x = x
        self.y = y
