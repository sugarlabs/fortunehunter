import pippy, pygame, sys, math
from hero import *
from battleEngine import *
from menu import *
from map import *
from tutorial import *
from item import *
from pygame.locals import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

################################################################################
# Player Class: stores info about the player ie. current position in dungeon etc
################################################################################
class Player:
  ####LOADS EVERYTHING FOR THE GAME####
  def __init__(self,x=0,y=0):
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
    
    self.initializeMenu()
    self.loadTutorial()
    self.loadImages()
    self.currentX=x
    self.currentY=y
    self.dgnIndex=-1
    self.dungeons=[("dungeon.txt",3,5),("dungeon2.txt",5,5)]
    self.nextDungeon()
    self.battlePlayer=Hero(self)
    self.curBattle=BattleEngine(self.battlePlayer,[Enemy(self,'0')])
    self.movTutorial=False
    self.hpTutorial=False
    self.battleTutorial=False
    self.puzzleTutorial=False
    self.lockTutorial=False
    self.invTutorial=False

    #state variables
    self.inTutorial=False
    self.mainMenu=True
    self.traversal=False
    self.waiting=False
    self.battle=False
    self.inGameTutorial=False
    #self.statMenu=False

    self.msg1=""
    self.msg2=""
    self.msg3=""
    self.msg4=""
    self.msg5=""

    self.playerFacing=NORTH

    #sound
    self.doorEffect=pygame.mixer.Sound(IMG_PATH+"door.wav")

  def initializeMenu(self):
    mainMenuImages=[IMG_PATH+"TutorialButton.gif",IMG_PATH+"NewGameButton.gif",IMG_PATH+"CloseButton.gif"]
    self.MainMenu=Menu(["Tutorial","New Game","Close"],self,IMG_PATH+"mafh_splash.gif",mainMenuImages,"Main Menu")
    
    statMenuOptions=["Weapon","Armor","Accessory","ItemSlot1","ItemSlot2","ItemSlot3","ItemSlot4"]
    statMenuImages=[IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif"]
    self.statsMenu=Menu(statMenuOptions,self,IMG_PATH+"battleMenubackground.gif",statMenuImages,"Stats")

    self.currentMenu=self.MainMenu
    self.previousMenu=self.MainMenu

 # def createInventoryMenu(self):
  #  inventoryMenuOptions=[]
  #  for item in self.battlePlayer.int_Ar:
    
  def loadTutorial(self):
    tutorialImages=[IMG_PATH+"t1.gif",IMG_PATH+"t2.gif",IMG_PATH+"t3.gif"]
    self.tutorial=Tutorial(tutorialImages,0,0)

  def loadImages(self):
    self.currentRoomSprite=pygame.sprite.Sprite()
    self.currentRoomSprite.image=pygame.image.load(IMG_PATH+"Black.gif")
    self.currentRoomSprite.rect=pygame.Rect(0,0,1200,700)

    self.Black=pygame.sprite.Sprite()
    self.Black.image=pygame.image.load(IMG_PATH+"Black.gif")
    self.Black.rect=pygame.Rect(0,0,1200,700)

    self.FLRSprite=pygame.sprite.Sprite()
    self.FLRSprite.image=pygame.image.load(IMG_PATH+"flr.gif")
    self.FLRSprite.rect=self.currentRoomSprite.rect

    self.FRSprite=pygame.sprite.Sprite()
    self.FRSprite.image=pygame.image.load(IMG_PATH+"fr.gif")
    self.FRSprite.rect=self.currentRoomSprite.rect

    self.FSprite=pygame.sprite.Sprite()
    self.FSprite.image=pygame.image.load(IMG_PATH+"f.gif")
    self.FSprite.rect=self.currentRoomSprite.rect

    self.FLSprite=pygame.sprite.Sprite()
    self.FLSprite.image=pygame.image.load(IMG_PATH+"fl.gif")
    self.FLSprite.rect=self.currentRoomSprite.rect

    self.LRSprite=pygame.sprite.Sprite()
    self.LRSprite.image=pygame.image.load(IMG_PATH+"lr.gif")
    self.LRSprite.rect=self.currentRoomSprite.rect

    self.LSprite=pygame.sprite.Sprite()
    self.LSprite.image=pygame.image.load(IMG_PATH+"l.gif")
    self.LSprite.rect=self.currentRoomSprite.rect

    self.NoSprite=pygame.sprite.Sprite()
    self.NoSprite.image=pygame.image.load(IMG_PATH+"_.gif")
    self.NoSprite.rect=self.currentRoomSprite.rect

    self.RSprite=pygame.sprite.Sprite()
    self.RSprite.image=pygame.image.load(IMG_PATH+"r.gif")
    self.RSprite.rect=self.currentRoomSprite.rect

    self.currentRoomGroup=pygame.sprite.Group(self.currentRoomSprite)

  def migrateMessages(self,msg):
    self.msg1=self.msg2
    self.msg2=self.msg3
    self.msg3=self.msg4
    self.msg4=self.msg5
    self.msg5=msg
    
  def nextDungeon(self):
    self.dgnIndex+=1
    dgnWidth=self.dungeons[self.dgnIndex][1]
    dgnHeight=self.dungeons[self.dgnIndex][2]
    self.dgn=Dungeon(dgnWidth,dgnHeight,IMG_PATH+self.dungeons[self.dgnIndex][0])
    self.dgn.fill()
    self.currentX=self.dgn.start[0]
    self.currentY=self.dgn.start[1]
    self.currentRoom=self.dgn.rooms.get((self.currentX,self.currentY))
    self.dgnMap=Map(self.dgn)
    self.currentRoom=self.dgn.rooms.get((self.currentX,self.currentY))
    
  def initInGameBattleTutorial(self,screen):
    batImages=[IMG_PATH+"attackButton.gif",IMG_PATH+"DivPH.gif",IMG_PATH+"GeomPH.gif",IMG_PATH+"ItemPH.gif"]
    batBg=IMG_PATH+"battleMenubackground.gif"
    numPadImages=[IMG_PATH+"1.gif",IMG_PATH+"2.gif",IMG_PATH+"3.gif",IMG_PATH+"4.gif",IMG_PATH+"5.gif",IMG_PATH+"6.gif",IMG_PATH+"7.gif",IMG_PATH+"8.gif",IMG_PATH+"9.gif",IMG_PATH+"0.gif",IMG_PATH+"Clear.gif",IMG_PATH+"Enter.gif"]
    geomImages=[IMG_PATH+"1.gif",IMG_PATH+"2.gif",IMG_PATH+"3.gif",IMG_PATH+"4.gif"]
    itemMenuOption=["Wrong","Wrong","Wrong",self.curBattle.battleMenu]
    itemMenu=Menu(itemMenuOption,self,batBg,batImages,"ItemTut")
    geomMenu3Option=[itemMenu,itemMenu,itemMenu,itemMenu,itemMenu,itemMenu,itemMenu,itemMenu,itemMenu]
    geomMenu3=Menu(geomMenu3Option,self,batBg,[IMG_PATH+"FireGlyph1btn.gif",IMG_PATH+"FireGlyph1btn.gif",IMG_PATH+"FireGlyph1btn.gif",IMG_PATH+"FireGlyph1btn.gif",IMG_PATH+"FireGlyph1btn.gif",IMG_PATH+"FireGlyph1btn.gif",IMG_PATH+"FireGlyph1btn.gif",IMG_PATH+"FireGlyph1btn.gif",IMG_PATH+"FireGlyph1btn.gif"],"GeomTut3")
    geomMenu3.numPad=True
    geomMenu2Option=[geomMenu3,"Wrong","Wrong","Wrong"]
    geomMenu2=Menu(geomMenu2Option,self,batBg,geomImages,"GeomTut2")
    geomMenuOption=["Wrong","Wrong",geomMenu2,"Wrong"]
    geomMenu=Menu(geomMenuOption,self,batBg,batImages,"GeomTut")
    divMenu2Option=[geomMenu]
    divMenu2=Menu(divMenu2Option,self,batBg,[IMG_PATH+"DivPH.gif"],"DivTut2")
    divMenuOption=["Wrong",divMenu2,"Wrong","Wrong"]
    divMenu=Menu(divMenuOption,self,batBg,batImages,"DivTut")
    critMenuOption=[divMenu,divMenu,divMenu,divMenu,divMenu,divMenu,divMenu,divMenu,divMenu,divMenu,divMenu,divMenu]
    critMenu=Menu(critMenuOption,self,batBg,numPadImages,"CritTut")
    critMenu.numPad=True
    atkMenuOption=[critMenu,"Wrong","Wrong","Wrong"]
    atkMenu=Menu(atkMenuOption,self,batBg,batImages,"AtkTut")
    self.currentMenu=atkMenu
    self.battleTutorial=True

  def initMovTutorial(self,screen):
    font=pygame.font.SysFont("cmr10",42,False,False)
    y=0
    lines=["Welcome to the first Dungeon!","To look around, press left or right.","To move forward, press up","To check inventory or equipment,","Press space or x"]
    for message in lines:
      screen.blit(font.render(message,True,(0,200,0)),(400,200+y,200,300))
      y+=40

  def checkRoom(self):
    message="Your search reveals "
    found=False
    if type(self.currentRoom.it1)==type(Item("","")) and self.currentRoom.it1.hidden:
      self.battlePlayer.inv_Ar.append(self.currentRoom.it1)
      message+=" "+self.currentRoom.it1.name
      found=True
    if type(self.currentRoom.it2)==type(Item("","")) and self.currentRoom.it2.hidden:
      self.battlePlayer.inv_Ar.append(self.currentRoom.it2)
      message+=" "+self.currentRoom.it2.name
      found=True
    if type(self.currentRoom.it3)==type(Item("","")) and self.currentRoom.it3.hidden:
      self.battlePlayer.inv_Ar.append(self.currentRoom.it3)
      message+=" "+self.currentRoom.it3.name
      found=True
    if type(self.currentRoom.it4)==type(Item("","")) and self.currentRoom.it4.hidden:
      self.battlePlayer.inv_Ar.append(self.currentRoom.it4)
      message+=" "+self.currentRoom.it4.name
      found=True
    if found==False:
      message+="nothing"
    return(message)