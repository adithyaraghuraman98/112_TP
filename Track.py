import pygame
import math
from pygamegame import PygameGame
from GameObject import GameObject

class Track(pygame.sprite.Sprite):
    def __init__(self,x,y,angle = 0,length = 0):
        super(Track, self).__init__()
        
        self.angle = angle*math.pi/180
        self.length = length
        self.image = pygame.Surface((length*math.cos(self.angle),
            length*math.sin(self.angle)+5),pygame.SRCALPHA) 
        self.FlagImage = pygame.image.load('Flag.png')
        self.originalx = x-50
        self.x = x-50
        self.y = y+40
        self.isLastTrack = False
        self.flagPoint = None
        self.bestTime = None
        if(self.angle == 0):self.height = 5
        else: self.height = length*math.sin(self.angle)
        if(self.angle<0):    
            pygame.draw.line(self.image,(0,0,0),(0,0),
                (length*math.cos(self.angle),+length*math.sin(self.angle)),4)
        else: 
            pygame.draw.line(self.image,(0,0,0),(0,length*math.sin(self.angle)),
                (length*math.cos(self.angle),0),4)
        
        self.rect = pygame.Rect(self.x+40, self.y-self.height,
                 self.length*math.cos(self.angle),self.height+20)  
        self.tempRect = pygame.Rect(self.x+40, self.y-self.height,
                 self.length*math.cos(self.angle),self.height+20) 
    def __str__(self):
        return "%d,%d,%d,%d" %(self.x,self.y,self.angle,self.length)

    def presentY(self,x):
        return self.y - (x - self.x)*math.tan(self.angle) 

    def drawFlag(self):
        self.isLastTrack = True
        self.flagPoint = self.x+self.length
        self.image.blit(self.FlagImage,(10,0))

    def xRange(self):
        return range(int(self.x),int(self.x+self.length*math.cos(self.angle))+30)
    
    def updateRect(self):
        self.rect = pygame.Rect(self.x+40, self.y-self.height,
                 self.length*math.cos(self.angle),self.height+20)

    def update(self,vel):
        #self.y -= vel[1]
        self.x -= vel[0]
        if(self.flagPoint!= None):self.flagPoint-=vel[0]
        self.updateRect()
        