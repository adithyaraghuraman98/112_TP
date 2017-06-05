#Adithya Raghuraman + araghura + section O 
#A few adaptations from Lukas Peraza's Asteroids Game
import pygame
from Bike import Bike
from pygamegame import PygameGame
import random
from Track import Track
import math
import time

def generateRandomTrack():
    listLength = random.randint(3,4)
    result = [None]*listLength
    x = 800/3 - 40
    y = 600*2/3 
    for i in range(listLength):
        if(i == 0 or i ==listLength-1):angle = 0
        else: angle = random.randint(20,45)
        length = random.randint(200,400)
        result[i] = Track(x,y,angle,length)  
        space = random.randint(40,70)
        x = x + length*math.cos(angle*math.pi/180)+space
        y = y - length*math.sin(angle*math.pi/180)
        if(y<90):y = 600*2/3 
    return result

def generateRandomHardTrack():
    listLength = random.randint(8,15)
    result = [None]*listLength
    x = 800/3 - 40
    y = 600*2/3 
    for i in range(listLength):
        if(i == 0 or i ==listLength-1):angle = 0
        else: angle = random.randint(30,60)
        length = random.randint(200,400)
        result[i] = Track(x,y,angle,length)  
        space = random.randint(40,70)
        x = x + length*math.cos(angle*math.pi/180)+space
        y = y - length*math.sin(angle*math.pi/180)
        if(y<90):y = 600*2/3
    return result

def generateTrack1():
    width,height = 800,600
    track1 = Track(width/3-40,height*2/3,0,300)
    track2 = Track(width/3-40+300,height*2/3,25,250)
    track3 = Track(width/3-40+600,height*2/3,0,250)
    return [track1,track2,track3]

def generateTrack2():
    width,height = 800,600
    track1 = Track(width/3-40,height*2/3,0,300)
    track2 = Track(width/3-40+300,height*4/5,0,300)
    track3 = Track(width/3-40+650,height*4/5,45,300)
    track4  = Track(width/3-40+900,height*1/2-40,0,300)
    return[track1,track2,track3,track4]

def generateTrack3():
    width,height = 800,600
    track1 = Track(width/3-40,height*2/3,0,300)
    track2 = Track(width/3-40+300,height*4/5,0,300)
    track3 = Track(width/3-40+650,height*4/5,45,700)
    track4 = Track(width/3-40+1500,height*3/4,0,300)
    return[track1,track2,track3,track4]

def generateTrack4():
    width,height = 800,600
    track1 = Track(width/3-40,height*2/3,0,300)
    track2 = Track(width/3-40+360,height*2/3,20,300)
    track3 = Track(width/3-40+700,height*2/3,30,300)
    track4 = Track(width/3-40+1000,height*2/3,40,300)
    track5 = Track(width/3-40+1200,height*4/5,0,300)
    track6 = Track(width/3-40+1530,height*4/5,20,300)
    track7 = Track(width/3-40+1900,height*4/5,40,300)
    track8 = Track(width/3-40+2130,height*4/5,50,500)
    track9 = Track(width/3-40+2550,height*4/5,0,300)
    return[track1,track2,track3,track4,track5,track6,track7,track8,track9]

def almostEquals(a,b):
    if abs(a-b)<= 1:return True
    return False


class Game(PygameGame):
    track1 = generateTrack1()
    track2 = generateTrack2()
    track3 = generateTrack3()
    track4 = generateTrack4()
    presetTrackList = [track1,track2,track3,track4]
    track1Time = None
    track2Time = None
    track3Time = None
    track4Time = None
    savedTrack1 = None
    savedTrack2 = None
    savedTrack3 = None
    savedTrackList = [savedTrack1,savedTrack2,savedTrack3]

    def reset():
        Game.track1 = generateTrack1()
        Game.track2 = generateTrack2()
        Game.track3 = generateTrack3()
        Game.track4 = generateTrack4()

    
    def init(self):
        self.FlagImage = pygame.image.load('Flag.png')
        self.bike = Bike(self.width/3,self.height*2/3)
        self.hardmode = False
        self.trackList = None
        self.bikeGroup = pygame.sprite.GroupSingle(self.bike)
        self.currentTrack = None
        self.visitedTrackList = []
        self.splashScreenMode = True
        self.instructionMode = False
        self.centerx = None
        self.centery = None
        self.startTime = None
        self.elapsedTime = 0
        self.completed = False
        self.gameOver = False
        self.restart = False
        self.replay = None
        self.gameMode = False
        self.trackSelectionMode = False
        self.manualTrackSelectionMode = False
        self.saveTrack = False
        self.displaySaveOption = False
        self.displayViewSavedTracksOption = False
    
    def setTrack(self):
        self.trackList = generateRandomHardTrack() if(self.hardmode) else generateRandomTrack()
        self.trackList[len(self.trackList)-1].drawFlag()
        self.trackGroup = pygame.sprite.Group(track for track in self.trackList)

    def savedReset(self):
        for track in Game.savedTrackList:
            if(track!=None):
                for subTrack in track:
                    delta = subTrack.originalx - subTrack.x
                    subTrack.x += delta
                    
    def mousePressed(self, x, y):
        screenWidth,screenHeight = 800,600
        if(self.instructionMode):
            self.instructionMode = False
            self.splashScreenMode = True
        elif(self.splashScreenMode):
            if(x in range(screenWidth//2-90,screenWidth//2+90)):
                if(y in range(screenHeight//2+60,screenHeight//2+100)):
                    self.splashScreenMode = False
                    self.instructionMode = False
                    self.trackSelectionMode = True
                if(y in range(screenHeight//2+110,screenHeight//2+150)):
                    self.splashScreenMode = False
                    self.instructionMode = True
        elif(self.trackSelectionMode):
            if(x in range(screenWidth//2-90,screenWidth//2+90)):
                if(y in range(screenHeight//2+40,screenHeight//2+80)):
                    self.trackSelectionMode = False
                    self.gameMode = True
                    self.startTime = time.time()
                    self.setTrack()
                if(y in range(screenHeight//2+90,screenHeight//2+130)):
                    self.trackSelectionMode = False
                    self.hardmode = True
                    self.gameMode = True
                    self.startTime = time.time()
                    self.setTrack()
                if(y in range(screenHeight//2+130,screenHeight//2+170)):
                    self.trackSelectionMode = False                    
                    self.displayViewSavedTracksOption = True
                if(y in range(screenHeight//2+180,screenHeight//2+220)):
                    self.trackSelectionMode = False
                    self.manualTrackSelectionMode = True    
        elif(self.manualTrackSelectionMode):
            if(x in range(screenWidth//2-90,screenWidth//2+90)):
                if(y in range(screenHeight//2-100,screenHeight//2-60)):
                    self.trackList = Game.track1
                    self.trackList[len(self.trackList)-1].drawFlag()
                    self.trackGroup = pygame.sprite.Group(track for track in self.trackList)
                    self.manualTrackSelectionMode = False
                    self.gameMode = True
                    self.startTime = time.time()
            if(x in range(screenWidth//2-90,screenWidth//2+90)):
                if(y in range(screenHeight//2-50,screenHeight//2-10)):
                    self.trackList = Game.track2
                    self.trackList[len(self.trackList)-1].drawFlag()
                    self.trackGroup = pygame.sprite.Group(track for track in self.trackList)
                    self.manualTrackSelectionMode = False
                    self.gameMode = True
                    self.startTime = time.time()
            if(x in range(screenWidth//2-90,screenWidth//2+90)):
                if(y in range(screenHeight//2,screenHeight//2+40)):
                    self.trackList = Game.track3
                    self.trackList[len(self.trackList)-1].drawFlag()
                    self.trackGroup = pygame.sprite.Group(track for track in self.trackList)
                    self.manualTrackSelectionMode = False
                    self.gameMode = True
                    self.startTime = time.time()
            if(x in range(screenWidth//2-90,screenWidth//2+90)):
                if(y in range(screenHeight//2+40,screenHeight//2+90)):
                    self.trackList = Game.track4
                    self.trackList[len(self.trackList)-1].drawFlag()
                    self.trackGroup = pygame.sprite.Group(track for track in self.trackList)
                    self.manualTrackSelectionMode = False
                    self.gameMode = True
                    self.startTime = time.time()
        elif(self.displayViewSavedTracksOption):
            if(x in range(screenWidth//2-90,screenWidth//2+90)):
                if(y in range(screenHeight//2-20,screenHeight//2+20)):
                    self.savedReset()
                    self.trackList = Game.savedTrackList[0]
                    self.trackList[len(self.trackList)-1].drawFlag()
                    self.trackGroup = pygame.sprite.Group(track for track in self.trackList)
                    self.displayViewSavedTracksOption = False
                    self.gameMode = True
                    self.startTime = time.time()
            if(x in range(screenWidth//2-90,screenWidth//2+90)):
                if(y in range(screenHeight//2+20,screenHeight//2+60)):
                    self.savedReset()
                    self.trackList = Game.savedTrackList[1]
                    self.trackList[len(self.trackList)-1].drawFlag()
                    self.trackGroup = pygame.sprite.Group(track for track in self.trackList)
                    self.displayViewSavedTracksOption = False
                    self.gameMode = True
                    self.startTime = time.time()
            if(x in range(screenWidth//2+50,screenWidth//2+90)):
                if(y in range(screenHeight//2+60,screenHeight//2+100)):
                    self.savedReset()
                    self.trackList = Game.savedTrackList[2]
                    self.trackList[len(self.trackList)-1].drawFlag()
                    self.trackGroup = pygame.sprite.Group(track for track in self.trackList)
                    self.displayViewSavedTracksOption = False
                    self.gameMode = True
                    self.startTime = time.time()


    def keyPressed(self, code, mod):
        if((self.gameOver or self.completed) and pygame.key.get_pressed()[pygame.K_r] != 0):
            self.restart = True
        if(self.gameOver and pygame.key.get_pressed()[pygame.K_s] != 0):
            self.saveTrack = True
            self.saveTrackToList()  
            self.restart = True  
        if(pygame.key.get_pressed()[pygame.K_BACKSPACE ] != 0):
            if(self.trackSelectionMode):
                self.trackSelectionMode = False
                self.splashScreenMode = True
            if(self.manualTrackSelectionMode):
                self.manualTrackSelectionMode = False
                self.trackSelectionMode = True
            if(self.displayViewSavedTracksOption):
                self.displayViewSavedTracksOption = False
                self.trackSelectionMode = True  
    def timerFired(self, dt):
        if(self.gameMode):
            self.trackGroup.update((self.bike.velocity[0],self.bike.velocity[1]))
            self.bikeGroup.update(dt, self.isKeyPressed, self.width, self.height)
        
    def detectGameOver(self):
        if(self.bike.y>self.height):self.gameOver = True
        if(abs(self.bike.angle)*math.pi/180 > math.pi*7/8 and
            self.bike.y<self.currentTrack.presentY(self.bike.x)+30): 
            self.gameOver = True
        if(self.trackList not in Game.presetTrackList):
            self.displaySaveOption = True
            

    def checkCollision(self):
        self.bike.freezeControls = False
        for track in self.trackList:
            if track.rect.colliderect(self.bike.rect):    
                if(track not in self.visitedTrackList):
                    if(self.bike.y<track.presentY(self.bike.x)):
                        self.visitedTrackList.append(track)
                        self.currentTrack = track
                        self.bike.baseAngle = track.angle*(180/math.pi)
                        vx,vy = self.bike.velocity[0],self.bike.velocity[1]
                        theta = self.currentTrack.angle
                        self.bike.velocity = (-vy*math.cos(theta),vy*math.sin(theta))

           
        if(self.bike.y+45<self.currentTrack.presentY(self.bike.x) or
            (int(self.bike.x) not in self.currentTrack.xRange())):
            self.bike.freezeControls = True
            self.bike.y+=8
            
    def checkFreeSlide(self):
        x,y = (self.bike.velocity)[0], (self.bike.velocity)[1]
        if(almostEquals(x,0) and almostEquals(y,0)):
            self.bike.isFreeSlide = True

    def displayTimer(self,screen):
        self.elapsedTime = (time.time() - self.startTime)
        font = pygame.font.Font(None, 30)
        text = font.render("Time Elapsed: "+str(self.elapsedTime)[0:5],1,(10, 10, 10)) 
        textpos = text.get_rect()
        textpos.topright = screen.get_rect().topright
        screen.blit(text, textpos)
    
    def displayFlag(self,screen):
        for track in self.trackList:
            if(track.isLastTrack):
                lastTrack = track
        screen.blit(self.FlagImage,(lastTrack.flagPoint-150,lastTrack.y-120))

    def saveTrackToList(self):
        if(self.saveTrack):
            for i in range (len(Game.savedTrackList)):
                if(Game.savedTrackList[i]==None):
                    Game.savedTrackList[i] = self.trackList
                    return
            Game.savedTrackList = [None]*3
            self.saveTrackToList()#use of recursion

    def displaySplashScreen(self,screen):
        font = pygame.font.Font(None, 50)
        text = font.render("Bike Race 1.0", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery
        screen.blit(text, textpos)
        text = font.render("Play", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery+80
        screen.blit(text, textpos)
        text = font.render("Instructions", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery+130
        screen.blit(text, textpos)

    def displayInstructions(self,screen):
        font = pygame.font.Font(None, 25)
        instruction1 = "Try to complete track as fast as possible!" 
        instruction2 = "Press right arrow key to accelerate. Use up and" 
        instruction3 = "down arrow keys to wheelie. Caution:Do not wheelie at an edge or your bike will fall!"
        instruction4 = "Have Fun! Click Again to go back"
        text = font.render(instruction1, 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery-20
        screen.blit(text, textpos)
        text = font.render(instruction2, 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery
        screen.blit(text, textpos)
        text = font.render(instruction3, 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery+20
        screen.blit(text, textpos)
        text = font.render(instruction4, 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery+40
        screen.blit(text, textpos)

    def detectCompletion(self):
        for track in self.trackList:
            if(track.isLastTrack):
                lastTrack = track
        if(self.bike.x>lastTrack.flagPoint and self.bike.y < 
            (lastTrack.presentY(self.bike.x))):
            self.completed = True
        if(self.completed):
            if(self.trackList == Game.track1):
                if(Game.track1Time==None or self.elapsedTime<Game.track1Time):
                    Game.track1Time = self.elapsedTime
            if(self.trackList == Game.track2):
                if(Game.track2Time==None or self.elapsedTime<Game.track2Time):
                    Game.track2Time = self.elapsedTime
            if(self.trackList == Game.track3):
                if(Game.track3Time==None or self.elapsedTime<Game.track3Time):
                    Game.track3Time = self.elapsedTime
            if(self.trackList == Game.track4):
                if(Game.track4Time==None or self.elapsedTime<Game.track4Time):
                    Game.track4Time = self.elapsedTime
            Game.reset()

    def displayTrackSelectionScreen(self,screen):
        font = pygame.font.Font(None, 50)
        text = font.render("Try Randomly Generated Track!", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery
        screen.blit(text, textpos)
        text = font.render("Easy", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery+60
        screen.blit(text, textpos)
        text = font.render("Hard", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery+110
        screen.blit(text, textpos)
        text = font.render("Or View Saved Tracks", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery+150
        screen.blit(text, textpos)
        text = font.render("Or select preset Track", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery+200
        screen.blit(text, textpos)

    def displayManualTrackSelectionScreen(self,screen):
        font = pygame.font.Font(None, 50)
        text = font.render("Track 1", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery-80
        screen.blit(text, textpos)
        font = pygame.font.Font(None, 30)
        text = font.render("Best Time:"+str(Game.track1Time)[0:5], 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx+200
        textpos.centery = self.centery-80
        screen.blit(text, textpos)
        font = pygame.font.Font(None, 50)
        text = font.render("Track 2", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery-30
        screen.blit(text, textpos)
        font = pygame.font.Font(None, 30)
        text = font.render("Best Time:"+str(Game.track2Time)[0:5], 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx+200
        textpos.centery = self.centery-30
        screen.blit(text, textpos)
        font = pygame.font.Font(None, 50)
        text = font.render("Track 3", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery+20
        screen.blit(text, textpos)
        font = pygame.font.Font(None, 30)
        text = font.render("Best Time:"+str(Game.track3Time)[0:5], 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx+200
        textpos.centery = self.centery+20
        screen.blit(text, textpos)
        font = pygame.font.Font(None, 50)
        text = font.render("Track 4", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx
        textpos.centery = self.centery+70
        screen.blit(text, textpos)
        font = pygame.font.Font(None, 30)
        text = font.render("Best Time:"+str(Game.track4Time)[0:5], 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.centerx+200
        textpos.centery = self.centery+70
        screen.blit(text, textpos)
    
    def displaySavedTracks(self,screen):
        if(Game.savedTrackList[0]!=None):
            font = pygame.font.Font(None, 50)
            text = font.render("Saved Track 1", 1, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = self.centerx
            textpos.centery = self.centery
            screen.blit(text, textpos)
        if(Game.savedTrackList[1]!=None):
            font = pygame.font.Font(None, 50)
            text = font.render("Saved Track 2", 1, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = self.centerx
            textpos.centery = self.centery+40
            screen.blit(text, textpos)
        if(Game.savedTrackList[2]!=None):
            font = pygame.font.Font(None, 50)
            text = font.render("Saved Track 3", 1, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = self.centerx
            textpos.centery = self.centery+ 80
            screen.blit(text, textpos)
    
    def displayCompletionScreen(self,screen):
        font = pygame.font.Font(None, 50)
        text = font.render("Track completed!", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = screen.get_rect().centery
        screen.blit(text, textpos)
        text = font.render("Your Time:" +str(self.elapsedTime)[0:5],1,(10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = screen.get_rect().centery+30
        screen.blit(text, textpos)
        text = font.render("Press \"R\" to restart", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = screen.get_rect().centery+60
        screen.blit(text, textpos)
        if(self.restart):
            self.init()
            self.restart = False
    
    def displayGameOverScreen(self,screen):
        font = pygame.font.Font(None, 50)
        if(self.displaySaveOption):
            text = font.render("Press \"S\" to save track", 1, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = screen.get_rect().centerx
            textpos.centery = screen.get_rect().centery+60
            screen.blit(text, textpos)
        text = font.render("Game Over", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = screen.get_rect().centery
        screen.blit(text, textpos)
        text = font.render("Press \"R\" to restart", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = screen.get_rect().centery+30
        screen.blit(text, textpos)
        if(self.restart):
            Game.reset()
            self.init()
            self.restart = False

    def redrawAll(self, screen):
        self.centerx = screen.get_rect().centerx
        self.centery = screen.get_rect().centery
        if(self.splashScreenMode):
            self.displaySplashScreen(screen)
        elif(self.instructionMode):
            self.displayInstructions(screen)
        elif(self.trackSelectionMode):
            self.displayTrackSelectionScreen(screen)
        elif(self.manualTrackSelectionMode):
            self.displayManualTrackSelectionScreen(screen)
        elif(self.gameOver):
            self.displayGameOverScreen(screen)
        elif(self.displayViewSavedTracksOption):
            self.displaySavedTracks(screen)
        elif(self.completed):
            self.displayCompletionScreen(screen)
        elif(self.gameMode):
            self.detectGameOver()
            self.detectCompletion()
            self.displayTimer(screen)
            self.bikeGroup.draw(screen)
            self.trackGroup.draw(screen)
            self.checkCollision()
            self.displayFlag(screen)
            self.checkFreeSlide()

Game(800, 600).run()
