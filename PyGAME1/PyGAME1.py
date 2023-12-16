from ctypes.wintypes import DOUBLE
import string
import sys
from tokenize import Double, String
sys.path.append('imports')
import pygame #pygame is definetly being imported.  idk why it complains here
from ast import Delete, Try
from math import log2, pi, sqrt
from tkinter import CURRENT
import random
from turtle import window_height, window_width
import os
import math


SWORD = []  #the images of the sword
SWORD_WARMUP = [] #basically the first rotation of sword as images
AllProjectiles= []
glow = []
BossShots =[]

currentStage= -1
topStage = currentStage
with open("Assets/data.txt", "r") as file:
    my_var = file.read()
    topStage=int(my_var)



pygame.init()
objects = []  
spikes= []
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h
rect_x = SCREEN_WIDTH // 4
rect_y = SCREEN_HEIGHT // 2
rect_width = (int)((SCREEN_WIDTH  / 4100) *  100)
rect_height =  (int)((SCREEN_HEIGHT  / 2160)  * 100)

rect_color = (255, 0, 0) # Red color
rect_speed = SCREEN_WIDTH/500
inMenue = True
mouseIsPressed = False
Sword_Cooldow = 50
BackgroundColor =(0,0,0)
globalScreen= ... #just a variable so i can use screen
global_tick=0     
global_clock = ...
clock =...
currentlyInANimation=False
transition_tick = 0  #just to make the level transition wait a sec
endless_mode_speed= 0.7
death_messages= [["death",""],["you are dead"],["try","again"],["murdered","in broad","daylight"],["try", "a little","harder"],["skill","issue"],["destructed"],["you","got","deleted"],["respawn", "or", "ragequit?"],["404", "skill", "not found"],["was that", "even", "an attempt?"],["uninstalling", "yet?"],["rest", "in", "pixels"],["running out of ideas", "for","death messages"],["i can","make fun of you", "all day"],["never gonna","stop insulting","you"], ["17 deaths?","are you even","trying?"],["well, good on you", "for not","giving up"], ["you","got","this"],["i believe","in","you"],["hmmmmmmmmmmmmmmmmmmm","mmmmmmmmmmmmmmmm","hmmmmmmm"],["ergf","rgfwefrhththhhhhhh"],["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"],["so yeah, making death messages at 1am", "what are you","doing ?"],["jk, ","not that i can hear","you"], ["unless....","",""],["ok i ","can't anymore",""]]
Death_noise =[]
Viper_trash_talk= [["When you get to hell, ","tell them Alpha sent you.",""], ["You hear that rining in your ears, son?","",""],["You hitched your last ride, son","",""], ["This is your stop","",""],[ "You need to move a little faster than that, son. ","Speed is life",""],["You're just too weak for the skies","",""]]
deathCounter=0
Faces = []
bossTick=1
bossNotDead=True
transparent_surface =...
playerIsDead= False
Invincible_cooldown= 1
SetToLevel7NOW= False
openedForTheFirstTime= True

def loadAssets():
    global SWORD
    global SWORD_WARMUP
    global glow
    global Death_noise
    for filename in os.listdir("Assets/SwordAssets"):
        img = pygame.image.load(os.path.join("Assets/SwordAssets", filename))
        scaled_image = pygame.transform.scale(img, (rect_width*3, rect_height*3))
        SWORD.append(scaled_image)
    for filename in os.listdir("Assets/SwordWarmupAnimation"):
        img = pygame.image.load(os.path.join("Assets/SwordWarmupAnimation", filename))
        scaled_image = pygame.transform.scale(img, (rect_width*3, rect_height*3))
        SWORD_WARMUP.append(scaled_image)
    for filename in os.listdir("Assets/Screens"):
        img = pygame.image.load(os.path.join("Assets/Screens", filename))
        scaled_image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        Death_noise.append(scaled_image)
    for filename in os.listdir("Assets/Face"):
        img = pygame.image.load(os.path.join("Assets/Face", filename))
        scaled_image = pygame.transform.scale(img, (rect_width*13, rect_width*13))
        Faces.append(scaled_image)




#fun fact 1: if you want your project to support an alpha channel, you have to build your whole project around that.
#fun fact 2: this is one of the last functions i added.

#so yeah. glow with no alpha. :)
def draw_gradient_glow(surface, position,  max_radius):
    global BackgroundColor
    x, y = position
    max_radius = int(max_radius)  *1.1

    for i in range(1,15,+3):
    
     alpha = 52
     glow_color = (min(BackgroundColor[0] + i,255), 
                     min(BackgroundColor[1] + i, 255), 
                     min(BackgroundColor[2] + i+3, 255))
       

     final_glow_color = (*glow_color, alpha)

     pygame.draw.circle(surface, final_glow_color, (x, y), int(max_radius/i))   
   

def manage_cooldowns():
    global Sword_Cooldow
    global Invincible_cooldown
    if(Sword_Cooldow>0):
     Sword_Cooldow -=1
    if(Invincible_cooldown>0 ):
     Invincible_cooldown -=1



def updateScreen(screen):
    global currentStage
    global BackgroundColor
    global AllProjectiles
    global transition_tick
    global topStage

    screen.fill(BackgroundColor)
    for i in AllProjectiles:
        i.draw_glow()
    for i in objects:
        i.update(screen)
    for i in AllProjectiles:
        i.update()
    pygame.display.flip()

    if(len(objects)==1 and currentlyInANimation==False):
        transition_tick+=1
        if(transition_tick>=10):
         newStage()
        
         currentStage+=1
         global SetToLevel7NOW
         if(SetToLevel7NOW):
             currentStage=7
             SetToLevel7NOW=False
         if(currentStage>topStage):
             topStage+=1

class Spike():
    global globalScreen
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global spikes
    global BackgroundColor
    def __init__(self,x,y, allignment):
       self.x = x
       self.y=y
       self.stage =0
       self.tick = 0
       self.allignment = allignment #string 

       self.color = (BackgroundColor[0]+50, BackgroundColor[1]-20, BackgroundColor[2]-20)
       self.h = SCREEN_HEIGHT/8
       if(self.allignment=="tentacles"):
           #ok nevermind. i will be balling now
           self.subtick=0
           self.colorTick =0
           self.allTents =[]
           self.topTents= []
           self.midTents= []
           self.botTents=[]

           def y_func(x, H, m, c):
             a = (2*m - 1) / (2*H**2)
             b = -c/(2*H) + (3 - 8*m) / (4*H)
             return a*x**3 + b*x**2 + c*x + H   #funny slopE
   
           #top tent:
          
           for i in range(int(SCREEN_WIDTH/3),SCREEN_WIDTH,int(20) ):
              
                   t = (self.x-i, self.y*1.5+1  -  y_func(i,SCREEN_HEIGHT/2,1,1)/2, rect_width, rect_height,i)
                   self.topTents.append(t)


           

       if(self.allignment == "homing"):
           self.y = objects[0].y - self.h/2
    def detectColission(self,rc):
      if(self.tick>= 200):
       plyr = pygame.Rect(objects[0].x, objects[0].y, objects[0].width, objects[0].height)
       if ( rc.colliderect(plyr)):
           Death()
    
    def update(self):


      if(self.tick <= 200):
        percent = self.tick / 2
      else:
          percent=100

      if(self.allignment=="tentacles"):
          def colission():
              ...
          self.y+=6


          if(self.tick <= 5000):
             percent = self.tick / 10
          else:
           percent=100   
          for i in self.topTents:
              i = list(i)

              ie= pygame.Rect(i[0],i[1]-SCREEN_HEIGHT/2 +(SCREEN_HEIGHT/2 * percent/100),i[2],i[3])
              b0x =pygame.draw.rect(globalScreen, ((self.color[0]-50)+self.colorTick,self.color[1]-self.colorTick*0.3,self.color[2]-self.colorTick*0.3), ie)
              if(self.colorTick==99):
                  ...#wait what
                  self.detectColission(ie)
             
              i = tuple(i)
          if self.tick>= 5000:
             spikes.remove(self)
          self.tick+=1
          self.colorTick+=1
          if(self.colorTick>=100):
              self.colorTick=0
          return


       
      if(self.tick <= 200):
        percent = self.tick / 2
      else:
          percent=100   

      try:
       rc= pygame.draw.rect(globalScreen, self.color, (self.x, self.y+2,SCREEN_WIDTH*0.7, self.h -3))
       spikey = pygame.draw.rect(globalScreen, (self.color[0]+percent*1.5,self.color[1],self.color[2]), (self.x, self.y+self.h/2- ( self.h *(percent)/100)/2  ,SCREEN_WIDTH*0.7, self.h *(percent)/100))
       self.detectColission(rc)
      except:
          ...
      
      if self.tick>= 205:
          for i in spikes:
              if i == self:
                  spikes.remove(i)

      self.tick+=1

class Homing_laser():   #🔥🔥🔥🔥🔥🔥🔥🔥
    def __init__(self,destXstart,destYstart, destXend, destYend, originXstart, originYstart, originXend, originYend,lifespan,startMovingAt):
       
        self.destXstart = destXstart
        self.destYstart= destYstart
        self.destXend=destXend
        self.destYend=destYend
        self.originXstart=originXstart
        self.originYstart=originYstart
        self.originXend=originXend
        self.originYend=originYend
        self.tick=0
        self.lifespan = lifespan
        self.boxes= []
        self.startMovingAt  =startMovingAt
        self.numRecs =25
        self.scale = rect_width*3
        self.color =(72,5,5)
        
        self.initiate_triangles()
    

    def initiate_triangles(self):
        for i in range(0,self.numRecs):
         rec = ([0, 0, self.scale, self.scale])
         self.boxes.append(rec)

        #initiate the distance between origin x and dest x for start and end, and decide the size of steps that will be taken
        vecx1 = self.destXstart- self.destXend
        vecy1 = self.destYstart - self.destYend
        len1 = math.sqrt(vecx1**2 + vecy1**2)
        self.lenStepsdest = (len1-self.startMovingAt)/self.lifespan

        vecx1 = self.originXstart- self.originXend
        vecy1 = self.originYstart - self.originYend
        len1 = math.sqrt(vecx1**2 + vecy1**2)
        self.lenStepsorigin = len1-self.startMovingAt/(self.lifespan-self.startMovingAt)
        
        print("destXstart:  "+ str(self.destXstart)+  " originXStart: "+ str(self.originXstart))
        print("destYstart:  "+ str(self.destYstart)+  " originYStart: "+ str(self.originYstart))
        print("init")


    
        
    def update(self):
        global spikes
        
        #calculate current vector
        percent = (self.tick)/self.lifespan
        if(self.tick >= self.startMovingAt):

         vecx1 = self.destXstart- self.destXend
         vecy1 = self.destYstart - self.destYend

         len1 = math.sqrt(vecx1**2 + vecy1**2)
         if(len1==0):
             len1+=0.0000000001
         self.destXstart += (vecx1/len1) * self.lenStepsdest
         self.destYstart += (vecy1/len1) * self.lenStepsdest

         vecx2 = self.originXstart- self.originXend
         vecy2 = self.originYstart - self.originYend
         len2 = math.sqrt(vecx2**2 + vecy2**2)
         if(len2==0):
             len2+=0.0000000001
         self.originXstart += (vecx2/len2) * self.lenStepsorigin
         self.originYstart += (vecy2/len2) * self.lenStepsorigin
        
         

         #calculate new rect location
  
         dx = (self.destXstart - self.originXstart)*1.2
         dy = (self.destYstart - self.originYstart)*1.2



         distance = math.sqrt(dx**2 + dy**2)
         
         step_size = distance / self.numRecs


         angle = math.atan2(dy, dx)

         for i in range(0,self.numRecs):
  
          self.boxes[i][0] = self.originXstart + dx * (i / self.numRecs)
          self.boxes[i][1]= self.originYstart + dy * (i / self.numRecs)
        

        
        
        #draw rects
        for box in self.boxes:
         rect = pygame.Rect(box[0], box[1], box[2], box[3])
         pygame.draw.rect(globalScreen, self.color, rect)
         #draw color indicator
         cl = pygame.Rect(box[0] , box[1]+   (box[3]/2) - (box[3]/2)*percent  , box[2], box[3] *percent )
         pygame.draw.rect(globalScreen, (self.color[0]+150*percent,self.color[1]+10*percent,self.color[2]+10*percent), cl)
         
         #hitbox
         if(self.tick>=self.lifespan):
             plyr = pygame.Rect(objects[0].x,objects[0].y,objects[0].width,objects[0].height)
             if ( rect.colliderect(plyr)):
                 Death()

  



        self.tick+=1
        if(self.tick == self.lifespan+2):
         
         spikes.remove(self)

        
class simpleCubeShot():
    def __init__(self,x,y,speed):
        self.x = x
        self.y=y
        self.width = rect_width*0.7
        self.color = (20,90,20)
        self.speed = speed*4
        ...
    def colission(self,me):
       global rect_width
       plyr = pygame.Rect(objects[0].x, objects[0].y, objects[0].width, objects[0].height)
       for i in AllProjectiles:
           proj = pygame.Rect(i.originx, i.originy, rect_width * i.projectileScale, rect_width * i.projectileScale)
           if (me.colliderect(proj)):
               BossShots.remove(self)
       if ( me.colliderect(plyr)):
           Death()
     
    def update(self):
      #pos
      self.x =  self.x -  self.speed

      me= pygame.Rect(self.x,self.y,self.width,self.width)
      self.colission(me)

      pygame.draw.rect(globalScreen, self.color, me)


      #out of bounds
      if (self.x <=  (-100)):
          try:
           BossShots.remove(self)
          except:
              ...
      

def Menue(screen,clock):
    global Sword_Cooldow
    global inMenue
    global currentStage
    global openedForTheFirstTime
    quitButtonIndex=0  #funny
    mouseIsHeld=False
    jumpscared=False
    bkk_color = (80, 80, 80)
    if(inMenue): #initialize the menue


        Sword_Cooldow+=5

        screen.fill(bkk_color)
        title= "Title for a videogame. (idk haven't thought of one yet)"
        font1 = pygame.font.SysFont(None, (int)(SCREEN_HEIGHT/16), bold=True)
        text1 = font1.render(title, True, (255, 50, 50))
        #this is the shadow
        font2 = pygame.font.SysFont(None, (int)(SCREEN_HEIGHT/16), bold=True)
        text2 = font2.render(title, True, (50, 0, 0))
       
        text_rect2 = text2.get_rect()
        text_rect2.center = (SCREEN_WIDTH/2+5, SCREEN_HEIGHT/2 * 0.8)  # Adjust as needed
        screen.blit(text2, text_rect2)
       
        text_rect1 = text1.get_rect()
        text_rect1.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 * 0.8)  # Adjust as needed
        screen.blit(text1, text_rect1)
        #make a text box


        # Font setup
        width= 200
        height=50   
        text_box_pos_x = SCREEN_WIDTH/2-width/2
        text_box_pos_y= SCREEN_HEIGHT/2 *1.2
        
        font3 = pygame.font.SysFont(None, (int)(SCREEN_HEIGHT/20), bold=True)

         # Create a rectangle for the text box

        text_box = pygame.Rect(text_box_pos_x,text_box_pos_y, width, height)  # x, y, width, height
        #boss rect
        boss_box = pygame.Rect(text_box_pos_x+ SCREEN_WIDTH*0.3,text_box_pos_y, width, height)
        textBoss = font3.render('retry boss', True, (30, 30, 30))
        Boss_rect = textBoss.get_rect(center=boss_box.center)

        # Render text
        text3 = font3.render('play', True, (30, 30, 30))
        text_rect = text3.get_rect(center=text_box.center)
        pygame.draw.rect(screen, (180, 180, 180), text_box)
        screen.blit(text3, text_rect)


        #quit button

        text_box_pos_x1 = SCREEN_WIDTH/2-width/2
        text_box_pos_y1= SCREEN_HEIGHT/2 *1.3
        
         # Create a rectangle for the text box
        text_box7 = pygame.Rect(text_box_pos_x1,text_box_pos_y1, width, height)  # x, y, width, height
        text_box8 = pygame.Rect(text_box_pos_x1-width*1.5,text_box_pos_y1, width*4, height)  # x, y, width, height

        # Render text
        text4 = font3.render('quit', True, (30, 30, 30))
        text_rect4 = text4.get_rect(center=text_box7.center)
        pygame.draw.rect(screen, (180, 180, 180), text_box7)
        screen.blit(text4, text_rect4)

      
    while(inMenue): #update the menue
        jumpscared=False
        
        for event in pygame.event.get():   #mandatory update to get the mouse position
         if event.type == pygame.QUIT:
            running = False
        

        if pygame.mouse.get_pressed()[0]:
  
            if not mouseIsHeld:
             mouseIsPressed = True
             mouseIsHeld = True
            else:
  
               mouseIsPressed = False
        else:
   
           mouseIsHeld = False
           mouseIsPressed = False
       


        screen.fill(bkk_color)
        screen.blit(text2, text_rect2)
        screen.blit(text1, text_rect1)
        #screen.blit(textBoss, Boss_rect)
        x,y = pygame.mouse.get_pos()



        #Boss:::
        if((topStage>=7 and playerIsDead) or (topStage>=7 and openedForTheFirstTime )):
         if boss_box.collidepoint(x, y):
            boss_box = pygame.Rect(text_box_pos_x+ SCREEN_WIDTH*0.2,text_box_pos_y, width, height)
            textBoss = font3.render('retry boss', True, (30, 30, 30))
            Boss_rect = textBoss.get_rect(center=boss_box.center)
            pygame.draw.rect(screen, (240, 240, 240), boss_box)
            screen.blit(textBoss, Boss_rect)
       
            #here i have a try-except because of a bug that crashes the game
            try:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    inMenue=False
                     
                    currentStage=7
                    global SetToLevel7NOW
                    SetToLevel7NOW= True
 
                    
                    
                  

            except:
                ...
         else:
            boss_box = pygame.Rect(text_box_pos_x+ SCREEN_WIDTH*0.2,text_box_pos_y, width, height)
            textBoss = font3.render('retry boss', True, (30, 30, 30))
            Boss_rect = textBoss.get_rect(center=boss_box.center)
            pygame.draw.rect(screen, (180, 180, 180), boss_box)
            screen.blit(textBoss, Boss_rect)
        #end of boss


        if text_box.collidepoint(x, y):
            
            text3 = font3.render('play', True, (30, 30, 30))
            text_rect = text3.get_rect(center=text_box.center)
            pygame.draw.rect(screen, (240, 240, 240), text_box)
            screen.blit(text3, text_rect)
       
            #here i have a try-except because of a bug that crashes the game
            try:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    inMenue=False
                  

            except:
                ...
        else:
            text3 = font3.render('play', True, (30, 30, 30))
            text_rect = text3.get_rect(center=text_box.center)
            pygame.draw.rect(screen, (180, 180, 180), text_box)
            screen.blit(text3, text_rect)



        if(not jumpscared):
          if(quitButtonIndex==0):         
           if text_box7.collidepoint(x, y):
            text4 = font3.render('quit', True, (30, 30, 30))
            text_rect4 = text4.get_rect(center=text_box7.center)
            pygame.draw.rect(screen, (240, 240, 240), text_box7)
            screen.blit(text4, text_rect4)
       
            #here i have a try-except because of a bug that crashes the game
            try:
                if mouseIsPressed:
                     quitButtonIndex+=1
                     jumpscared=True

            except:
                ...
           else:
            text4 = font3.render('quit', True, (30, 30, 30))
            text_rect4 = text4.get_rect(center=text_box7.center)
            pygame.draw.rect(screen, (180, 180, 180), text_box7)
            screen.blit(text4, text_rect4)
        if(not jumpscared):
         if(quitButtonIndex==1):
          bkk_color = (120, 80, 80)
          if text_box7.collidepoint(x, y):
            text4 = font3.render('why?', True, (30, 30, 30))
            text_rect4 = text4.get_rect(center=text_box7.center)
            pygame.draw.rect(screen, (240, 150, 150), text_box7)
            screen.blit(text4, text_rect4)
       
            #here i have a try-except because of a bug that crashes the game
            try:
                if mouseIsPressed:
                     quitButtonIndex+=1
                     jumpscared=True
            except:
                ...
          else:
            text4 = font3.render('why?', True, (30, 30, 30))
            text_rect4 = text4.get_rect(center=text_box7.center)
            pygame.draw.rect(screen, (200, 130, 130), text_box7)
            screen.blit(text4, text_rect4)
        if(not jumpscared):
         if(quitButtonIndex==2):
          bkk_color = (180, 80, 80)
          if text_box8.collidepoint(x, y):
            text4 = font3.render('YOU WANT TO EXIT MY GAME?', True, (30, 30, 30))
            text_rect4 = text4.get_rect(center=text_box8.center)
            pygame.draw.rect(screen, (240, 50, 50), text_box8)
            screen.blit(text4, text_rect4)
       
            #here i have a try-except because of a bug that crashes the game
            try:
                if mouseIsPressed:
                     quitButtonIndex+=1
                     jumpscared=True
            except:
                ...
          else:
            text4 = font3.render('YOU WANT TO EXIT MY GAME?', True, (30, 30, 30))
            text_rect4 = text4.get_rect(center=text_box8.center)
            pygame.draw.rect(screen, (200, 0, 0), text_box8)
            screen.blit(text4, text_rect4)
        if(not jumpscared):
         if(quitButtonIndex==3):
          bkk_color = (80, 80, 80)
          if text_box7.collidepoint(x, y):
            text4 = font3.render('ok fine', True, (30, 30, 30))
            text_rect4 = text4.get_rect(center=text_box7.center)
            pygame.draw.rect(screen, (240, 240, 240), text_box7)
            screen.blit(text4, text_rect4)
       
            #here i have a try-except because of a bug that crashes the game
            try:
                if mouseIsPressed:
                      pygame.quit()
                      sys.exit()
            except:
                ...
          else:
            text4 = font3.render('ok fine', True, (30, 30, 30))
            text_rect4 = text4.get_rect(center=text_box7.center)
            pygame.draw.rect(screen, (180, 180, 180), text_box7)
            screen.blit(text4, text_rect4)
        
        #updating
        clock.tick(60)
        pygame.display.flip()
    openedForTheFirstTime=False
    
def BossFight():
    global globalScreen
    global spikes
    global currentStage
    global BossShots
    bossSize= rect_width*10
    bossNotDead= True
    global objects
    dialogue_voices = "Vodoo 1, Alpha on station", "Your jurney ends here, player", "This fight belongs to me","Nowhere to run","Nowhere to hide","Dodge this", "Alpha's got you in the pipe, 5x5", "0-9-0 for 20, coming in high", "I've for good tone", "Negative contact", "Raz 4 scanned - 0.0923", "Positive id on player visual, coming right", "Alpha-one lost control,",  "I'm losing control, mayday mayday"
    
    global bossTick
    bossTick=1

    BossShots.clear()
    def dialogue():
        global transparent_surface
        def txt(indx):
            font = pygame.font.SysFont(None, (int)(SCREEN_HEIGHT/16), bold=True)
            text1 = font.render(dialogue_voices[indx], True, (255, 255, 255))
            text2 = font.render(dialogue_voices[indx], True, (33, 33, 33))
            rect2 = text1.get_rect()
            rect1 = text1.get_rect()
            rect2.center = (SCREEN_WIDTH*0.5+4, SCREEN_HEIGHT*0.25+4)
            rect1.center = (SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.25)
            globalScreen.blit(text2,rect2)
            globalScreen.blit(text1,rect1)
        if(bossTick>650 and bossTick < 750):
            txt(0)
        if(bossTick>750 and bossTick < 850):
            txt(1)
        if(bossTick>850 and bossTick < 950):
            txt(2)
        if(bossTick>950 and bossTick < 1030):
            txt(3)
        if(bossTick>1030 and bossTick < 1110):
            txt(4)
        if(bossTick>200 and bossTick < 300):
            txt(10)
        if(bossTick>300 and bossTick < 400):
            txt(11)
        if(bossTick>2790 and bossTick < 2950):
            txt(6)
        if(bossTick>4750 and bossTick<4850):
            txt(8)
        if(bossTick>4850 and bossTick<4950):
            txt(5)
        if(bossTick>6500 and bossTick<6600):
            txt(12)

        if(bossTick>6600 and bossTick<6700):
            txt(13)
        #draw face
        #doing it this way cuz performance
        if(bossTick== 530):
         transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
         transparent_surface.fill((0, 0, 0, 0))  # Fully transparent (0 alpha)
         #transparent_surface.blit(Faces[2], (SCREEN_WIDTH/1.2 -bossSize/1.6 , (SCREEN_HEIGHT/2-bossSize/1.15)  *2.5))
         #the funny face may never be used again

         transparent_surface.blit(Faces[0], (SCREEN_WIDTH/1.2 -bossSize/1.6 , SCREEN_HEIGHT/2-bossSize/1.15  *1.1))
        if (bossTick>530):
            globalScreen.blit(transparent_surface, (0,0))

    def attacks():
       def pincer_attack(intial_tick):
         global bossTick
         dialogue()
         if(bossTick== intial_tick):
            spk = Spike(0,0," ")
            spikes.append(spk)
            spk = Spike(0,SCREEN_HEIGHT*7/8," ")
            spikes.append(spk)
         
         if(bossTick== intial_tick+60): 
            spk = Spike(0,SCREEN_HEIGHT/8," ")
            spikes.append(spk)
            spk = Spike(0,SCREEN_HEIGHT*6/8," ")
            spikes.append(spk)
        
         if(bossTick== intial_tick+120):
            spk = Spike(0,SCREEN_HEIGHT*2/8," ")
            spikes.append(spk)
            spk = Spike(0,SCREEN_HEIGHT*5/8," ")
            spikes.append(spk)
       global bossTick
       print(bossTick)
       if(bossTick<=4000):
        if(bossTick== 1180):
            spk = Spike(0,0," ")
            spikes.append(spk)
            spk = Spike(0,SCREEN_HEIGHT*7/8," ")
            spikes.append(spk)
        if(bossTick== 1240):
            spk = Spike(0,SCREEN_HEIGHT/8," ")
            spikes.append(spk)
            spk = Spike(0,SCREEN_HEIGHT*6/8," ")
            spikes.append(spk)
        if(bossTick== 1300):
            spk = Spike(0,SCREEN_HEIGHT*2/8," ")
            spikes.append(spk)
            spk = Spike(0,SCREEN_HEIGHT*5/8," ")
            spikes.append(spk)
        if(bossTick== 1390):
            spk = Spike(0,SCREEN_HEIGHT*3.5/8," ")
            spikes.append(spk)
        if (bossTick > 1450 and bossTick < 1490):
            if (bossTick %3==0):
               objects.append (Rectangle( SCREEN_WIDTH*0.7, SCREEN_HEIGHT* (( bossTick- 1450)/100)*2.4, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        if(bossTick ==  1550):
            spk = Spike(0,SCREEN_HEIGHT*3.5/8,"homing")
            spikes.append(spk)
        if (bossTick > 1550 and bossTick < 1590):
            if (bossTick %3==0):
               objects.append (Rectangle( SCREEN_WIDTH*0.7, SCREEN_HEIGHT* (( bossTick- 1550)/100)*2.4, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        if(bossTick ==  1590):
            spk = Spike(0,SCREEN_HEIGHT*3.5/8,"homing")
            spikes.append(spk)
        if (bossTick > 1690 and bossTick < 1850):
            if (bossTick %5==0):
               objects.append (Rectangle( SCREEN_WIDTH*0.7, SCREEN_HEIGHT* (( bossTick- 1690)/100)*0.5, rect_width, rect_height, (0,250,0), rect_speed*0.5, "basicEnemy"))
               objects.append (Rectangle( -200, SCREEN_HEIGHT* (( bossTick- 1690)/100)*0.5, rect_width, rect_height, (0,250,0), rect_speed*0.5, "basicEnemy"))
        if(bossTick == 1820):
            spk = Spike(0,SCREEN_HEIGHT*3.5/8,"homing")
            spikes.append(spk)
        if(bossTick == 1880):
            spk = Spike(0,0," ")
            spikes.append(spk)
            spk = Spike(0,SCREEN_HEIGHT*7/8," ")
            spikes.append(spk)
        if(bossTick == 1950):
            spk = Spike(0,SCREEN_HEIGHT*1/8," ")
            spikes.append(spk)
            spk = Spike(0,SCREEN_HEIGHT*6/8," ")
            spikes.append(spk)
        if(bossTick == 1950):
            spk = Spike(0,SCREEN_HEIGHT*3.5/8,"homing")
            spikes.append(spk)
        pincer_attack(2120)
        if (bossTick > 2100 and bossTick < 2150):
            if (bossTick %7==0):
               objects.append (Rectangle( SCREEN_WIDTH, SCREEN_HEIGHT* (( bossTick- 2100)/100)*2, rect_width, rect_height, (0,250,0), rect_speed*1.7, "basicEnemy"))
        if (bossTick > 2100 and bossTick < 2150):
            if (bossTick %7==0):
               objects.append (Rectangle( SCREEN_WIDTH* (( bossTick- 2100)/100)*2, 0, rect_width, rect_height, (0,250,0), rect_speed*0.7, "basicEnemy"))
        if (bossTick > 2300 and bossTick < 2350):
            if (bossTick %7==0):
               objects.append (Rectangle( SCREEN_WIDTH* (( bossTick- 2300)/100)*2, 0-SCREEN_HEIGHT*0.3, rect_width, rect_height, (0,250,0), rect_speed*0.6, "basicEnemy"))
               objects.append (Rectangle( SCREEN_WIDTH* (( bossTick- 2300)/100)*2, SCREEN_HEIGHT*1.3, rect_width, rect_height, (0,250,0), rect_speed*0.6, "basicEnemy"))
               spk = Spike(0,SCREEN_HEIGHT*3.5/8,"homing")
        if (bossTick ==2450):
            spk = Spike(0,SCREEN_HEIGHT*3.5/8,"homing")
        
        if(bossTick==2900):
            spk  = Homing_laser(-100, SCREEN_HEIGHT*0.9, -100,SCREEN_HEIGHT*0.9, SCREEN_WIDTH/1.2, SCREEN_HEIGHT/2, SCREEN_WIDTH/1.2, SCREEN_HEIGHT/2, 500,0 )
            spikes.append(spk)
            spk  = Homing_laser(-100, SCREEN_HEIGHT*0.1, -100,SCREEN_HEIGHT*0.1, SCREEN_WIDTH/1.2, SCREEN_HEIGHT/2, SCREEN_WIDTH/1.2, SCREEN_HEIGHT/2, 500,0 )
            spikes.append(spk)


        if(bossTick>= 3000 and bossTick <= 3999):
            index =  bossTick-3000

            if(bossTick%2==0):
              cb = simpleCubeShot(SCREEN_WIDTH/1.2, 0 +  SCREEN_HEIGHT* (math.ceil(index / 100) * 100-index)/100, 0.7)
              BossShots.append(cb)
              cb = simpleCubeShot(SCREEN_WIDTH/1.2, SCREEN_HEIGHT-  SCREEN_HEIGHT* (math.ceil(index / 100) * 100-index)/100,0.7)
              BossShots.append(cb)
         
        if (bossTick > 3100 and bossTick < 3150):
            if (bossTick %7==0):
               objects.append (Rectangle( SCREEN_WIDTH, SCREEN_HEIGHT* (( bossTick- 2100)/100)*2, rect_width, rect_height, (0,250,0), rect_speed*1.7, "basicEnemy"))
            if (bossTick %3==0):
               i = (bossTick - 3100)/50
               objects.append (Rectangle( SCREEN_WIDTH*i, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.6, "basicEnemy"))
               objects.append (Rectangle( SCREEN_WIDTH*i, 0, rect_width, rect_height, (0,250,0), rect_speed*0.6, "basicEnemy"))
               objects.append (Rectangle( SCREEN_WIDTH, SCREEN_HEIGHT*i, rect_width, rect_height, (0,250,0), rect_speed*1.3, "basicEnemy"))


        pincer_attack(3150)
        if(bossTick>= 4000 and bossTick <= 3700):
            index =  bossTick-4000

            if(bossTick%2==0):
              cb = simpleCubeShot(SCREEN_WIDTH/1.2, 0 +  SCREEN_HEIGHT* (math.ceil(index / 100) * 100-index)/100, 0.7)
              BossShots.append(cb)
              cb = simpleCubeShot(SCREEN_WIDTH/1.2, SCREEN_HEIGHT-  SCREEN_HEIGHT* (math.ceil(index / 100) * 100-index)/100,0.7)
              BossShots.append(cb)
        if(bossTick==3500):
            spk  = Homing_laser(-100, SCREEN_HEIGHT*1.1, -100,SCREEN_HEIGHT*1.1, SCREEN_WIDTH/1.2, SCREEN_HEIGHT/2, SCREEN_WIDTH/1.2, SCREEN_HEIGHT/2, 400,0 )
            spikes.append(spk)
            spk  = Homing_laser(-100, SCREEN_HEIGHT*0.1, -100,SCREEN_HEIGHT*0.1, SCREEN_WIDTH/1.2, SCREEN_HEIGHT/2, SCREEN_WIDTH/1.2, SCREEN_HEIGHT/2, 400,0 )
            spikes.append(spk)
        if(bossTick== 3550):
            spk = Spike(0,SCREEN_HEIGHT*3.5/8,"homing")
            spikes.append(spk)
        if(bossTick==3600):
            spk = Spike(0,SCREEN_HEIGHT*3.5/8,"homing")
            spikes.append(spk)
        if(bossTick >= 3600 and bossTick<= 3650):
            i = (bossTick - 3600)/50
            if(bossTick%3==0):
              objects.append (Rectangle( SCREEN_WIDTH*i, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.6, "basicEnemy"))
              objects.append (Rectangle( SCREEN_WIDTH*i, 0, rect_width, rect_height, (0,250,0), rect_speed*0.6, "basicEnemy"))
        if(bossTick==3650):
            spk = Spike(0,SCREEN_HEIGHT*3.5/8,"homing")
            spikes.append(spk)
            objects.append (Rectangle( SCREEN_WIDTH, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*2.5, "basicEnemy"))
            objects.append (Rectangle( SCREEN_WIDTH, 0, rect_width, rect_height, (0,250,0), rect_speed*2.5, "basicEnemy"))  #stage 1 and 2. added this "if" for performance reasons. Also, i know that putting hundreds of IFs in a row is bad practice but. Idk how else to do it.

       if(bossTick>4000):

        pincer_attack(4172)
        if (bossTick > 4150 and bossTick < 4200):
            if (bossTick %3==0):
               objects.append (Rectangle(SCREEN_WIDTH* (( bossTick- 4150)/100)*2, -500, rect_width, rect_height, (0,250,0), rect_speed*0.7, "basicEnemy"))
               objects.append (Rectangle(SCREEN_WIDTH* (( bossTick- 4150)/100)*2, SCREEN_HEIGHT+500, rect_width, rect_height, (0,250,0), rect_speed*0.7, "basicEnemy"))
               objects.append (Rectangle(SCREEN_WIDTH, SCREEN_HEIGHT* (( bossTick- 4150)/100)*2, rect_width, rect_height, (0,250,0), rect_speed*0.9, "basicEnemy"))
        if(bossTick>4750 and bossTick<4950):
            dialogue()

        if(bossTick==4960):
            plyrx = objects[0].x
            plyry = objects[0].y
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,80,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,80,0))
        if(bossTick==5080):
            plyrx = objects[0].x
            plyry = objects[0].y
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,80,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,80,0))
        if(bossTick==5200):
            plyrx = objects[0].x
            plyry = objects[0].y
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,80,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,80,0))

            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, SCREEN_HEIGHT,SCREEN_WIDTH+50, SCREEN_HEIGHT,80,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, 0,SCREEN_WIDTH+50, 0,80,0))
        if(bossTick==5320):
            plyrx = objects[0].x
            plyry = objects[0].y
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,80,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,80,0))

            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, SCREEN_HEIGHT,SCREEN_WIDTH+50, SCREEN_HEIGHT,80,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, 0,SCREEN_WIDTH+50, 0,80,0))
        if(bossTick==5440):
            plyrx = objects[0].x
            plyry = objects[0].y
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,100,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,100,0))

            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, SCREEN_HEIGHT,SCREEN_WIDTH+50, SCREEN_HEIGHT,100,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, 0,SCREEN_WIDTH+50, 0,100,0))

            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,  -200, 0,-200, 0,100,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,  -200, SCREEN_HEIGHT,-200, SCREEN_HEIGHT,100,0))
        if(bossTick==5560):
            plyrx = objects[0].x
            plyry = objects[0].y
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,100,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,100,0))

            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, SCREEN_HEIGHT,SCREEN_WIDTH+50, SCREEN_HEIGHT,100,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, 0,SCREEN_WIDTH+50, 0,100,0))

            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,  -200, 0,-200, 0,100,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,  -200, SCREEN_HEIGHT,-200, SCREEN_HEIGHT,100,0))
        if(bossTick==5680):
            plyrx = objects[0].x
            plyry = objects[0].y
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,100,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,100,0))

            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, SCREEN_HEIGHT,SCREEN_WIDTH+50, SCREEN_HEIGHT,100,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, 0,SCREEN_WIDTH+50, 0,100,0))

            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,  -200, 0,-200, 0,100,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,  -200, SCREEN_HEIGHT,-200, SCREEN_HEIGHT,100,0))
        if(bossTick>= 5100 and bossTick <= 8000):
            index = bossTick-5100
            if(bossTick%4==0):
              cb = simpleCubeShot(SCREEN_WIDTH/1.2, 0 +  SCREEN_HEIGHT* (math.ceil(index / 100) * 100-index)/100, 0.7)
              BossShots.append(cb)
              cb = simpleCubeShot(SCREEN_WIDTH/1.2, SCREEN_HEIGHT-  SCREEN_HEIGHT* (math.ceil(index / 100) * 100-index)/100,0.7)
              BossShots.append(cb)
        if(bossTick>=5400 and bossTick<=5500):
            if (bossTick %5==0):
              objects.append (Rectangle(SCREEN_WIDTH* (( bossTick- 5400)/100)*2, SCREEN_HEIGHT*1.2, rect_width, rect_height, (0,250,0), rect_speed*0.7, "basicEnemy"))
        pincer_attack(6000)   
        if(bossTick==6100):
            plyrx = objects[0].x
            plyry = objects[0].y
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*1.2,150,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,SCREEN_WIDTH*0.8, SCREEN_HEIGHT/2*0.8,150,0))

            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, SCREEN_HEIGHT,SCREEN_WIDTH+50, SCREEN_HEIGHT,150,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,SCREEN_WIDTH+50, 0,SCREEN_WIDTH+50, 0,150,0))

            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,  -200, 0,-200, 0,150,0))
            spikes.append(Homing_laser(plyrx,plyry,plyrx,plyry,  -200, SCREEN_HEIGHT,-200, SCREEN_HEIGHT,150,0))

            objects.append (Rectangle(SCREEN_WIDTH, 0, rect_width, rect_height, (0,250,0), rect_speed*2, "basicEnemy"))
            objects.append (Rectangle(SCREEN_WIDTH, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.4, "basicEnemy"))
            objects.append (Rectangle(SCREEN_WIDTH, 0, rect_width, rect_height, (0,250,0), rect_speed*2, "basicEnemy"))
            objects.append (Rectangle(SCREEN_WIDTH, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.4, "basicEnemy"))
        if(bossTick>6500 and bossTick<6700):
            dialogue()
        if(bossTick==6700):
            bossTick=1


    def Intoduction():
        global bossTick
        global BackgroundColor
        global globalScreen
        global clock
        global SCREEN_HEIGHT
        global SCREEN_WIDTH
        BackgroundColor = (55,55,55)
        bossTick=1
        bossSize= rect_width*10

      
          
        while (1):

         for event in pygame.event.get():   #mandatory update to get the mouse position
          if event.type == pygame.QUIT:
             running = False
         manage_cooldowns()
        

         globalScreen.fill(BackgroundColor)
     

         for i in AllProjectiles:
          i.draw_glow()

         #shadow
         Shadowcolor = (BackgroundColor[0]-20,BackgroundColor[1]-20,BackgroundColor[2]-20)
         pygame.draw.rect(globalScreen, Shadowcolor, (SCREEN_WIDTH/1.2 -bossTick*((bossTick**2)/250000)/2, SCREEN_HEIGHT/2-bossTick*((bossTick**2)/250000)/2, bossTick* ((bossTick**2)/250000) , bossTick*( (bossTick**2)/250000)))
         #boss dropping
         pygame.draw.rect(globalScreen, (30,250,30), (SCREEN_WIDTH/1.2 -bossTick/2, (SCREEN_HEIGHT/2-bossSize/2) -(bossSize-bossTick)*50, bossSize, bossSize))
         
         #scarry face lul
         globalScreen.blit(Faces[0], (SCREEN_WIDTH/1.2 -bossTick/1.6, (SCREEN_HEIGHT/2-bossSize/1.15) -(bossSize-bossTick)*50))
      

         for i in objects:
          i.update(globalScreen)
         for i in AllProjectiles:
          i.update()
         dialogue()


         Menue(globalScreen,clock)
         clock.tick(60)
         pygame.display.flip()
         if(bossTick==bossSize):
             return bossTick
         bossTick+=1

    def ForcePush(x_start):
     
        if(len(objects)!=0):
            if(objects[0].x > x_start):

             force = ((objects[0].x-x_start)**2 / 4000)+0.5
             if(force>100):
                 force=100
             objects[0].x-= force
    if(bossNotDead):
     bossTick = Intoduction()
    
    while(bossNotDead):

        for event in pygame.event.get():   #mandatory update to get the mouse position
          if event.type == pygame.QUIT:
             running = False
        manage_cooldowns()
        
        if(bossTick<200):
            break
        globalScreen.fill(BackgroundColor)
        
        ForcePush(SCREEN_WIDTH/2 * 0.85)
        for i in AllProjectiles:
          i.draw_glow()
        for i in spikes:
            i.update()
        pygame.draw.rect(globalScreen, (30,250,30), (SCREEN_WIDTH/1.2 -bossSize/2, (SCREEN_HEIGHT/2-bossSize/2) , bossSize, bossSize))
        
        for i in objects:
          i.update(globalScreen)
        for i in BossShots:
           i.update()
        for i in AllProjectiles:
          i.update()
        dialogue()
        attacks()
        Menue(globalScreen,clock)
        if(bossNotDead==False):
            currentStage=6
            return

        bossTick+=1
        clock.tick(60)
        pygame.display.flip()
def updateSaveData():
        global currentStage
        with open("Assets/data.txt", "r") as file:
          my_var = int(file.read())
        if(my_var<=currentStage):
         with open("Assets/data.txt", "w") as file:
          file.write(str(currentStage))
    
def newStage():
    global BackgroundColor
    global transition_tick
    global endless_mode_speed
    global topStage
    global playerIsDead
    transition_tick=0
    playerIsDead=False
    if(currentStage== (-1)):
        #tutorial

        Tutorial()

    if(currentStage==0):
        for i in AllProjectiles:
            AllProjectiles.remove(i)
        levelCutszene(["Level 1","ready","START!"])

        

        objects.append (Rectangle( 0, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        
    if(currentStage==1):

        for i in AllProjectiles:
            AllProjectiles.remove(i)
        levelCutszene(["Level 2", ])


        updateSaveData()
        BackgroundColor = (55,55,55)
        objects.append (Rectangle( 0, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( 0, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        
    if(currentStage==2):
        for i in AllProjectiles:
            AllProjectiles.remove(i)
        levelCutszene(["Level 3","Not bad"])
        updateSaveData()
        BackgroundColor = (15,55,55)
        objects.append (Rectangle( 0, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( 0, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
    if(currentStage==3):
        for i in AllProjectiles:
            AllProjectiles.remove(i)
        levelCutszene(["Level 4", "more enemies" ])
        updateSaveData()
        BackgroundColor = (55,15,55)
        objects.append (Rectangle( 0, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, SCREEN_HEIGHT/2, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( 0, SCREEN_HEIGHT/2, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( 0, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
    if(currentStage==4):
        for i in AllProjectiles:
            AllProjectiles.remove(i)
        levelCutszene(["Level 5", "MORE","ENEMIES" ])
        updateSaveData()
        BackgroundColor = (55,55,15)
        objects.append (Rectangle( 0, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, 0, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, SCREEN_HEIGHT/2, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( 0, SCREEN_HEIGHT/2, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( 0, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))

        objects.append (Rectangle( -500, -500, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, -500, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, SCREEN_HEIGHT+500, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH+500, -500, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH+500, SCREEN_HEIGHT/2, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( -500, SCREEN_HEIGHT/2, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, SCREEN_HEIGHT+500, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( -500, SCREEN_HEIGHT+500, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH+500, SCREEN_HEIGHT, rect_width, rect_height, (0,250,0), rect_speed*0.8, "basicEnemy"))

    if(currentStage==5):
        for i in AllProjectiles:
            AllProjectiles.remove(i)
        levelCutszene(["Level 6", "new","approach" ])
        updateSaveData()
        BackgroundColor = (80,40,40)
        objects.append (Rectangle( -500, -500, rect_width, rect_height, (0,250,0), rect_speed*1.5, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, -500, rect_width, rect_height, (0,250,0), rect_speed*1.5, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, SCREEN_HEIGHT+500, rect_width, rect_height, (0,250,0), rect_speed*1.5, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH+500, -500, rect_width, rect_height, (0,250,0), rect_speed*1.5, "basicEnemy"))
    if(currentStage==6):
        for i in AllProjectiles:
            AllProjectiles.remove(i)
        levelCutszene(["ok i am out of ideas",":(" ])
        updateSaveData()
        BackgroundColor = (89,0,15)


        for i in range(20):
         x_position = -500 if i % 2 == 0 else SCREEN_WIDTH + 500
         y_position = (i / 20) * (SCREEN_HEIGHT + 1000) - 500

         objects.append(Rectangle(x_position, y_position, rect_width, rect_height, (0, 250, 0), rect_speed * 0.8, "basicEnemy"))
        
        objects.append (Rectangle( -500, -500, rect_width, rect_height, (0,250,0), rect_speed*1.5, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, -500, rect_width, rect_height, (0,250,0), rect_speed*1.5, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH/2, SCREEN_HEIGHT+500, rect_width, rect_height, (0,250,0), rect_speed*1.5, "basicEnemy"))
        objects.append (Rectangle( SCREEN_WIDTH+500, -500, rect_width, rect_height, (0,250,0), rect_speed*1.5, "basicEnemy"))
    if(currentStage==7):
        ...
        if(topStage<= 7):
            topStage=7
        levelCutszene(["*airborne bogi aquired*","WARNING","WARNING"])
        updateSaveData()
        BossFight()
    if(currentStage==8):
        for i in AllProjectiles:
            AllProjectiles.remove(i)
        levelCutszene(["Endless","mode"])
        BackgroundColor = (88,88,88)
        
        for i in range(20):
         quadrant = random.randint(1,4)
         if(quadrant==1):
             x_position = random.randint(-500,0)
             y_position= random.randint(0,SCREEN_HEIGHT)
         if(quadrant==2):
             x_position = random.randint(0,SCREEN_WIDTH)
             y_position= random.randint(-500,0)   
         if(quadrant==3):
             x_position = random.randint(SCREEN_WIDTH,SCREEN_WIDTH+500)
             y_position= random.randint(0,SCREEN_HEIGHT)   
         if(quadrant==4):
             x_position = random.randint(0,SCREEN_WIDTH)
             y_position= random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT+500)   

         objects.append(Rectangle(x_position, y_position, rect_width, rect_height, (0, 250, 0), rect_speed *endless_mode_speed, "basicEnemy"))
        endless_mode_speed+=0.1
    if(currentStage>=9):
        for i in AllProjectiles:
            AllProjectiles.remove(i)
        levelCutszene(["faster","enemies"])
        updateSaveData()
        
        for i in range(20):
         quadrant = random.randint(1,4)
         if(quadrant==1):
             x_position = random.randint(-500,0)
             y_position= random.randint(0,SCREEN_HEIGHT)
         if(quadrant==2):
             x_position = random.randint(0,SCREEN_WIDTH)
             y_position= random.randint(-500,0)   
         if(quadrant==3):
             x_position = random.randint(SCREEN_WIDTH,SCREEN_WIDTH+500)
             y_position= random.randint(0,SCREEN_HEIGHT)   
         if(quadrant==4):
             x_position = random.randint(0,SCREEN_WIDTH)
             y_position= random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT+500)   

         objects.append(Rectangle(x_position, y_position, rect_width, rect_height, (0, 250, 0), rect_speed *endless_mode_speed, "basicEnemy"))
        endless_mode_speed+=0.1
       
def levelCutszene( Text):
   global clock
   global globalScreen
   local_tick=0
   offset=1
   cutszene =True
   global_tick = 0
   myTitles= []
   for i in Text:
    title= i

    font1 = pygame.font.SysFont(None, (int)(SCREEN_HEIGHT/16), bold=True)
    text1 = font1.render(title, True, (255, 50, 50))
     
    font2 = pygame.font.SysFont(None, (int)(SCREEN_HEIGHT/16), bold=True)
    text2 = font2.render(title, True, (50, 0, 0))

    text_rect2 = text2.get_rect()
    text_rect2.center = (SCREEN_WIDTH/2+5, SCREEN_HEIGHT/2 * 0.8*offset)  
   
    myTitles.append(text2)
    myTitles.append(text_rect2)
       
    text_rect1 = text1.get_rect()
    text_rect1.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 * 0.8*offset) 
    myTitles.append(text1)
    myTitles.append(text_rect1)
    offset= offset*1.2
   
   while(cutszene):
    for event in pygame.event.get():   #mandatory update to get the mouse position
         if event.type == pygame.QUIT:
            running = False
        #updating
    

    if(local_tick == len(Text) * 40):
        break
    if(local_tick<40):
        globalScreen.blit(myTitles[0],myTitles[1])
        globalScreen.blit(myTitles[2],myTitles[3])
        
    if(local_tick<80 and local_tick>40):
        globalScreen.blit(myTitles[4],myTitles[5])
        globalScreen.blit(myTitles[6],myTitles[7])

    if(local_tick<120 and local_tick>80):
        globalScreen.blit(myTitles[8],myTitles[9])
        globalScreen.blit(myTitles[10],myTitles[11])

    
    pygame.display.flip()
    local_tick+=1
    clock.tick(60)


def Death():
    global globalScreen
    global clock
    global inMenue
    global currentStage
    global BackgroundColor
    global death_messages
    global deathCounter
    global bossNotDead
    global spikes
    global bossTick
    global playerIsDead
    global Invincible_cooldown

    if(Invincible_cooldown!=0):
        return
    Invincible_cooldown=5
    for i in objects:
        pygame.draw.rect(globalScreen, i.color, (i.x, i.y, i.width, i.height))
    bossNotDead=False
    playerIsDead=True
    globalScreen.blit(Death_noise[0], (0,0))
    # Clear objects and AllProjectiles lists
    if(currentStage==7):
        r=  random.randint(0, len(Viper_trash_talk)-1)
        levelCutszene(Viper_trash_talk[r])
    else:
     if(deathCounter<len(death_messages)):
      levelCutszene(death_messages[deathCounter])
     else:
        levelCutszene(["Death","number", str(deathCounter+1)])
 
    deathCounter+=1
    objects.clear()
    AllProjectiles.clear()
    spikes.clear()
    bossNotDead = False  # Reset the boss fight flag
    bossTick = 1  # Reset the boss fight timer
    # Reset the current stage and re-add the player
    currentStage = -1
    objects.append(Rectangle(rect_x, rect_y, rect_width, rect_height, rect_color, rect_speed, "player"))
    BackgroundColor =(0,0,0)
    # Set the game to return to the menu
    inMenue = True
    Menue(globalScreen, clock)

def Tutorial():
   global clock
   global globalScreen
   global InTutorial
   global currentStage
   global rect_width
  
   while (1):
    for event in pygame.event.get():   #mandatory update to get the mouse position
         if event.type == pygame.QUIT:
            running = False
    globalScreen.fill(BackgroundColor)
    draw_gradient_glow(globalScreen, (SCREEN_WIDTH/2 + (rect_width+20),SCREEN_HEIGHT/2+(rect_width+50)),rect_width*3 )

    objects[0].update(globalScreen)

    trigger = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 200, 200)
    selF = pygame.Rect(objects[0].x,objects[0].y, rect_width, rect_height)
   
    globalScreen.blit(SWORD[2], (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
    
    if ( selF.colliderect(trigger)):
        globalScreen.fill(BackgroundColor)
        objects[0].update(globalScreen)
        currentStage+=1
        break
    pygame.display.flip()

    clock.tick(60)
    

class SwordProjectile():
    global AllProjectiles
    global SWORD
    global rect_speed
    Animationtick =0

    def __init__(self,originx,originy,  destx, desty):
       #super().__init__(originx,originy,  destx,desty)
       self.originx= originx
       self.originy = originy
       self.destx = destx
       self.desty=desty
       self.hitBoxShape = "square"
       self.projectileScale = 3 #projectileScale
       self.velocity= rect_speed * 5
       self.IsWarmupComplete = False #warmup as in animation warmup
       self.warmupIndex= 0
       
       #adjusting x and y for offset because anchor is topleft 
       self.originx= self.originx - (rect_width>>1)
       self.originy=  self.originy - (rect_height>>1)
       self.destx=   self.destx   - ((rect_width * self.projectileScale) >>1)
       self.desty=   self.desty   - ((rect_height * self.projectileScale) >>1)
       self.MAXanimation_index = len(SWORD)-1
       self.currentanimation_index = 0
       self.warmupAnimationIndex=0
       AllProjectiles.append(self)

    def draw_glow(self):
       
        draw_gradient_glow(globalScreen,(self.originx + rect_width*1.5,self.originy+rect_height*1.5),rect_width*1.5)
    def updateanimation(self):
        global globalScreen
        global BackgroundColor
        if( not self.IsWarmupComplete):
            
            globalScreen.blit(SWORD_WARMUP[self.warmupAnimationIndex], (self.originx,self.originy))
            
            if (len(SWORD_WARMUP)>self.warmupAnimationIndex+1):
                self.IsWarmupComplete=True
            else:
                if(self.warmupIndex %3==0):
                    self.warmupAnimationIndex+=1
        if(  self.IsWarmupComplete):
            
            globalScreen.blit(SWORD[self.currentanimation_index], (self.originx,self.originy))
           
            #print(self.warmupIndex)
            if(self.warmupIndex %3 ==0):
                if(self.currentanimation_index < self.MAXanimation_index):
                    self.currentanimation_index+=1
                else:
                    self.currentanimation_index= 0
        self.warmupIndex+=1


    def hitDetection(self):
        hitbox = pygame.Rect(self.originx, self.originy, rect_width*self.projectileScale, rect_height*self.projectileScale)
       
        for i in objects:
            if( i!= objects[0]):
                enemy_hitbox = pygame.Rect(i.x, i.y, i.width, i.height)
                if(hitbox.colliderect(enemy_hitbox)):
                    objects.remove(i)
    
    def update(self):
        
        #update sword position :
        vecx = self.destx - self.originx
        vecy = self.desty - self.originy
        length = math.sqrt(vecx**2 + vecy**2)
        if length != 0:
          vecx /= length
          vecy /= length
        self.destx += vecx * 5000
        self.desty += vecy * 5000
        self.originx += vecx * self.velocity
        self.originy += vecy * self.velocity


        #animation
        self.updateanimation()


        #hitbox:
        self.hitDetection()

        #check if projectile is out of bounds:
        if(self.originx <-300 or self.originx > SCREEN_WIDTH+3000 or self.originy <-300 or self.originy > SCREEN_HEIGHT+300):
         AllProjectiles.remove(self)
            


class Rectangle:
    health=100
   
    def __init__(self, x, y, width, height, color, speed,player):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.player = player #the kind of character. OPTIONS:     "player"  ,  "basicEnemy"
    def get_shape_(self):
      drips = []
      # Assuming globalScreen is a Pygame surface defined globally
      global globalScreen
      rect1 = pygame.Rect(self.x, self.y, self.width, self.height)
      rect1_ = (globalScreen,self.color, rect1)
      drips.append(rect1_)
      return drips
      
    def update(self,screen):
        global Sword_Cooldow
        global inMenue
        global mouseIsPressed
        global rect_width
        global rect_height
        global SCREEN_HEIGHT
        global SCREEN_WIDTH
        if(self.player == "player"):
         keys = pygame.key.get_pressed()
         if keys[pygame.K_a]:
            if(self.x>0):
                self.x -= self.speed
         if keys[pygame.K_d]:
             if(self.x< (SCREEN_WIDTH-rect_width)):
                self.x += self.speed
         if keys[pygame.K_w]:
             if(self.y>0):
              self.y -= self.speed
         if keys[pygame.K_s]:
             if(self.y<(SCREEN_HEIGHT-rect_width)):
              self.y += self.speed
         if keys[pygame.K_ESCAPE]:
             inMenue=True

         #attack ( i have to this cuz uh, otherwise you could hold down m1 for permanent attack loop)
         
         if pygame.mouse.get_pressed()[0] and mouseIsPressed==False:
             
             #implement attack by triggering the cooldown
             if(Sword_Cooldow==0):
                 Sword_Cooldow=70

                 mouse_x,mouse_y = pygame.mouse.get_pos()
                 SwordProjectile(self.x,self.y, mouse_x,mouse_y )

             mouseIsPressed=True
         if not pygame.mouse.get_pressed()[0]:
             mouseIsPressed= False
       



         #check for damage taken
         for i in objects:
             if(i!= self):
                
                if( sqrt(  (self.x-i.x)**2+ (self.y-i.y)**2 )<= self.width*1.5):
                    
                    Death()
        
        
                
                 

        if(self.player == "basicEnemy"):

            #hunt down player
            vecx = objects[0].x - self.x
            vecy = objects[0].y - self.y
            length = math.sqrt(vecx**2 + vecy**2)
            if length != 0:
              vecx /= length
              vecy /= length
            
            self.x += vecx * self.speed
            self.y += vecy * self.speed
        rectsss= self.get_shape_()
        for surface, color, rect in rectsss:
           pygame.draw.rect(surface, color, rect)
        

def main():
 global global_tick
 global globalScreen
 global clock
 loadAssets()





 # Set up the display
 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

 
 globalScreen = screen
 pygame.display.set_caption("MyGame")

 
 clock = pygame.time.Clock()


 objects.append (Rectangle( rect_x, rect_y, rect_width, rect_height, rect_color, rect_speed, "player"))
 # Main game loop
 running = True

 print("pygame launched")
 while running:
    Menue(screen,clock) #render the menue if menue is up
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    #things happen
   
    
    updateScreen(screen)
    manage_cooldowns()
    # Cap the frame rate
    global_tick+=1
    clock.tick(60)

 # Quit Pygame
 pygame.quit()
 sys.exit()

print("Launching game")
print("Please wait")

main()

