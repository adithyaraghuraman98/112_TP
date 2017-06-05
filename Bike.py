import pygame
import math
from GameObject import GameObject
import Track

class Bike(GameObject):
    image = pygame.image.load('Bike.png')#http://goo.gl/fyGV1t
    
    def __init__(self, x, y,angle = 0):
        super(Bike, self).__init__(x, y, Bike.image, 15)
        self.airResistance = 0.94
        self.angleSpeed = 5
        self.baseAngle = 0
        self.angle = self.baseAngle 
        self.maxSpeed = 30
        self.gravity = 20
        self.freezeControls = None
        self.isFreeSlide = False
        
        
    def update(self, dt, keysDown, screenWidth, screenHeight):
        if keysDown(pygame.K_DOWN) and not self.freezeControls:
            self.angle -= self.angleSpeed
        
        elif keysDown(pygame.K_RIGHT) and self.freezeControls !=True:
            self.move()
            self.isFreeSlide = False
            if keysDown(pygame.K_UP):self.angle += self.angleSpeed
        elif(self.isFreeSlide):self.freeSlide()
        else:
            vx, vy = self.velocity
            self.velocity = self.airResistance * vx, self.airResistance * vy
            if(self.angle%360>90 and self.angle%360<180): self.angle+=self.angleSpeed
            elif(self.angle%360>0 and self.angle%360<90):self.angle-=self.angleSpeed
            elif(self.angle%360>270 and self.angle%360<360):self.angle+=self.angleSpeed
        
        super(Bike, self).update(screenWidth, screenHeight)
    
        
    def freeSlide(self):
        theta = self.baseAngle*math.pi/180
        self.velocity = (-3*math.sin(theta)*math.cos(theta),3*math.sin(theta)*math.sin(theta))

    def move(self):
        angle = math.radians(self.angle)
        vx, vy = self.velocity
        vx += math.cos(self.baseAngle*math.pi/180) 
        vy -= math.sin(self.baseAngle*math.pi/180) 
        speed = math.sqrt(vx ** 2 + vy ** 2) 
        if speed > self.maxSpeed:
            factor = self.maxSpeed / speed
            vx *= factor
            vy *= factor*0.5
        self.velocity = (vx, vy)