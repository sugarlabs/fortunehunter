import pygame
from fortuneengine.GameEngineElement import GameEngineElement
from fortuneengine.DrawableObject import DrawableObject
from fortuneengine.DrawableFontObject import DrawableFontObject

from constants import MENU_PATH
from gettext import gettext as _

NORMAL_MENU = 1
GRID_MENU = 3

class BattleMenuHolder( GameEngineElement ):
    def __init__(self, callback):
        GameEngineElement.__init__(self, has_draw=True, has_event=False)
        self.menu = None
        self.callback = callback
        self.background = DrawableObject([pygame.image.load( MENU_PATH + "battleMenubackground.gif")], '')
        self.font = pygame.font.SysFont("cmr10",18,False,False)
        self.disp = DrawableFontObject("", self.font)
        self.sec_disp = DrawableFontObject("", self.font)
        self.add_to_scene([self.background])
        self.add_to_scene([self.disp])
        self.add_to_scene([self.sec_disp])

    def set_disp(self, msg):
        self.disp.changeText(msg, (0,0,0))

    def set_sec_disp(self, msg):
        self.sec_disp.changeText(msg, (0,0,0))

    def remove_from_engine(self):
        super( BattleMenuHolder, self ).remove_from_engine()
        self.clear_menu()

    def draw(self):
        self.background.setPosition(0,286)
        self.disp.setPosition(250,340)
        self.sec_disp.setPosition(237, 375)

    def menu_called(self, id):
        self.callback(id, self)

    def clear_menu(self):
        if self.menu:
            self.menu.clear()
            self.menu.remove_from_engine()
            self.menu = None

    def show_menu(self,id):
        if self.is_in_engine():
            self.clear_menu()
        else:
            self.add_to_engine()

        y_offset = 0
        if id == "selection":
            menu_type = NORMAL_MENU
            menu_options = [
                        [_("Attack"), lambda: self.menu_called("attack_show"), 140,1],
                        [_('Special'), lambda: self.show_menu("special"), 140,1],
                        [_('Magic'), lambda: self.show_menu("magic"), 140,1],
                        [_('Scan'), lambda: self.menu_called("scan"), 140,1],
            ]

        elif id == "attack":
            y_offset = 50
            menu_type = GRID_MENU
            menu_options = [
                        ['1', lambda: self.menu_called('1'),44,1],
                        ['2', lambda: self.menu_called('2'),44,1],
                        ['3', lambda: self.menu_called('3'),44,1],
                        ['4', lambda: self.menu_called('4'),44,1],
                        ['5', lambda: self.menu_called('5'),44,1],
                        ['6', lambda: self.menu_called('6'),44,1],
                        ['7', lambda: self.menu_called('7'),44,1],
                        ['8', lambda: self.menu_called('8'),44,1],
                        ['9', lambda: self.menu_called('9'),44,1],
                        [_("C"), lambda: self.menu_called('clear'),44,1],
                        ['0', lambda: self.menu_called('0'),44,1],
                        [_("E"), lambda: self.menu_called('enter'),44,1],
            ]

        elif id == "special":
            menu_type = NORMAL_MENU
            menu_options = [
                        [_("Back"), lambda: self.show_menu("selection"),140,1]
            ]

        elif id == "magic":
            menu_type = NORMAL_MENU
            menu_options = [
                        [_("Fire"),  lambda: self.menu_called("fire"), 140, 1],
                        [_("Lightning"),  lambda: self.menu_called("lightning"), 140, 1],
                        [_("Missile"), lambda: self.menu_called("missile"), 140, 1],
                        [_("Heal"),  lambda: self.menu_called("heal"), 140, 1],
                        [_("Back"), lambda: self.show_menu("selection"), 140, 1]
            ]

        else:
            print "Invalid Menu", id
            return

        self.menu = BattleMenu(menu_options, 237, 375+y_offset, menu_type)


class BattleMenu(GameEngineElement):
    def __init__(self, game_menu, x, y, type=NORMAL_MENU):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)

        self.menu = Menu(game_menu, type, self.game_engine.get_scene(), x, y )

        self.add_to_engine()

    def event_handler(self, event):
        return self.menu.update(event)

    def draw(self):
        self.menu.draw()
    
    def clear(self):
        self.menu.clear()

class Menu(object):
    def __init__(self, options, cols, scene, x=237, y=375):
        """Initialize the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""

        self.options = options
        self.scene = scene
        self.x = x
        self.y = y
        self.cols = cols
        self.font = pygame.font.SysFont("cmr10",18,False,False)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.options)*self.font.get_height()
        self.font_list = []
        self.rect_list = []
        
        for o in self.options:
            self.font_list.append(DrawableFontObject(o[0], self.font))
            ren = self.font.render(o[0], 1, [0,0,0])
            if ren.get_width() > self.width:
                self.width = ren.get_width()

        i=0 # Row Spacing
        h=0 # Selection Spacing
        j=0 # Col Spacing
        for o in self.options:
            newX = self.x + 45 * j
            newY = self.y + i * 45
            
            surf = pygame.Surface((o[2],44))
            surf.fill((0, 74, 94))
            tempDO = DrawableObject([surf], "")
            tempDO.setPosition(newX,newY)
            self.rect_list.append(tempDO)
            
            surf = pygame.Surface((o[2]-4, 40))
            surf.fill((4, 119, 152))
            tempDO = DrawableObject([surf], "")
            tempDO.setPosition(newX+2, newY+2)
            self.rect_list.append(tempDO)

            j+=o[3]
            h+=1
            if j >= self.cols:
                i+=1
                j=0
            
        self.scene.addObjects(self.rect_list)
        self.scene.addObjects(self.font_list)

    def draw(self):
        #self.scene.drawEntireScene(surface)
        """Draw the menu to the surface."""
        i=0 # Row Spacing
        h=0 # Selection Spacing
        j=0 # Col Spacing
        k=1 # Rect Counter
        for o in self.options:
            if h==self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            self.font_list[h].changeText(text, clr)

            newX = self.x + 45 * j
            newY = self.y + i * 45
            
            self.font_list[h].setPosition(newX + 15, newY + 12)

            j+=o[3]
            h+=1
            k+=2
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

            # This jumps for uniform size buttons
            # TODO FIX ME: weird behavior when jumping over weird sized buttons.
            self.option = self.option % len(self.options)

        return return_val

    def clear(self):
        for text in self.font_list:
            self.scene.removeObject(text)
        for rect in self.rect_list:
            self.scene.removeObject(rect)

    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.x = x
        self.y = y
