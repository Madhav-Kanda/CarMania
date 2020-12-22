#Modules Used
import pygame
import os
import random
import sys

#Initialising Module
pygame.mixer.init()   #FOR IMAGES AND SOUNDS
pygame.init()         #FOR INITIALISING PYGAME MODULES LIKE FONT....

#Variables
white=(255,255,255)     #SETTING VALUES FOR WHITE COLOR
fps=32                  #VARIABLE FOR NUMBER OF FRAMES PER SECOND
screen_width=289
screen_height=511
screen=pygame.display.set_mode((screen_width,screen_height))      #SETTING UP THE DISPLAY 
Game_sprites={}
Game_sound={}
font=pygame.font.SysFont(None,30)
clock=pygame.time.Clock()                                   
pygame.display.set_caption("Car Game By Madhav")             #SETTING THE CAPTION 

#Images
Game_sprites['background']=pygame.image.load("IMAGES/background.jpeg").convert()
Game_sprites['background'] = pygame.transform.scale(Game_sprites['background'], (screen_width, screen_height)).convert_alpha()
Game_sprites['car']=pygame.image.load("IMAGES/Car.png").convert_alpha()
Game_sprites['end']=pygame.image.load("IMAGES/end.jpeg").convert()
Game_sprites['end'] = pygame.transform.scale(Game_sprites['end'], (screen_width, screen_height)).convert_alpha()
Game_sprites['road']=road=pygame.image.load("IMAGES/Roadedited.jpg")
Game_sprites['road']=pygame.transform.scale(road,(screen_width,screen_height)).convert_alpha()
Game_sprites['background']=pygame.image.load("IMAGES/background.jpeg").convert()
Game_sprites['background']= pygame.transform.scale(Game_sprites['background'], (screen_width, screen_height)).convert_alpha()
Game_sprites['truck']=pygame.image.load("IMAGES/truck topview2new.jpg").convert_alpha()
Game_sprites['tree']=pygame.image.load('IMAGES/tree.png').convert_alpha()
    
#Sounds
Game_sound['crash']=(pygame.mixer.Sound('SOUND/car crash.mp3'))
Game_sound['start']=(pygame.mixer.Sound('SOUND/carstartgarage.mp3'))
Game_sound['background']=(pygame.mixer.Sound('SOUND/Initial Background.mp3'))
Game_sound['turn']=(pygame.mixer.Sound('SOUND/turn.mp3'))

#DEFINING FUNCTION
#FOR WRITING TEXT ON SCREEN
def text_screen(text, color, x, y):
    screen_text = font.render(text,True,color)
    screen.blit(screen_text, [x,y])

#FOR GENERATING RANDOM TRUCKS ON SCREEN (ONE ABOVE AND ONE BELOW)
def Randomtruck():
    y1=random.randint(100,145)              #VALUES TAKEN SUCH THAT THE TOP MOST CORNER DOES NOT GO INTO THE 
    y2=y1+170                               #THE GREEN PART
    truckX=screen_width+10
    truck=[
        {'x':truckX, 'y':y2},
        {'x':truckX, 'y':y1}
    ]
    return truck

def Randomtree():
    y1=random.randint(10,70)               
    y2=random.randint(410,470)                            
    treeX=screen_width+10
    tree=[
        {'x':treeX, 'y':y2},
        {'x':treeX, 'y':y1}
    ]
    return tree


#DEFINING WHEN THE COLLISION BETWEEN CAR AND TRUCK OCCURS
def iscollide(car_x,car_y,uppertruck,lowertruck):
    for truck in uppertruck:
        truckheight = Game_sprites['truck'].get_height()
        if(car_y < int(truckheight/1.5) + truck['y'] and abs(car_x - truck['x']) < Game_sprites['truck'].get_width()):
            Game_sound['crash'].play()
            return True

    for truck in lowertruck:
        if (car_y + int(Game_sprites['car'].get_height()/1.5) > truck['y']) and abs(car_x - truck['x']) < Game_sprites['truck'].get_width():
            Game_sound['crash'].play()
            return True

    return False



#DEFINING THE VARIOUS SCREENS
#WELCOME SCREEN
def welcome_screen():
    while True:
        for event in pygame.event.get():
            if (event.type==pygame.QUIT) or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): 
                pygame.quit()
                sys.exit()
            
            elif (event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN):
                return

            else:
                screen.blit(Game_sprites['background'], (0, 0))       
                pygame.display.update()
                Game_sound['background'].play()
                clock.tick(fps)

#MAIN GAME 
def Maingame():
    score=0
    car_x=int(screen_width/6)   
    car_y=int(screen_height/2)
    Game_sound['background'].stop()
    Game_sound['start'].play()

#Creating Random Trucks on road
    newtruck1=Randomtruck()        
    newtruck2=Randomtruck()

#Frame Velocity so that the car appears moving forward
    truckvelX=-10

    uppertruck=[
        {'x':screen_width+200 ,'y':newtruck1[1]['y']},
        {'x':screen_width+200+(screen_width/2) ,'y':newtruck2[1]['y']}
        ]
    lowertruck=[
        {'x':screen_width+200 ,'y':newtruck1[0]['y']},
        {'x':screen_width+200+(screen_width/2) ,'y':newtruck2[0]['y']}
        ]


#Creating Random Trees
    newtree1=Randomtree()        
    newtree2=Randomtree()

#Frame Velocity so that the car appears moving forward
    treevelX=-10

    uppertree=[
        {'x':screen_width+150 ,'y':newtree1[1]['y']},
        {'x':screen_width+150+(screen_width/2) ,'y':newtree2[1]['y']}
        ]
    lowertree=[
        {'x':screen_width+200 ,'y':newtree1[0]['y']},
        {'x':screen_width+200+(screen_width/2) ,'y':newtree2[0]['y']}
        ]


#Checking Highscore
    global hiscore
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

#CONTROLS OF CAR
            if event.type==pygame.KEYDOWN and event.key==pygame.K_UP:
                velocity_y=10
                car_y=car_y-velocity_y
                Game_sound['turn'].play()

            
            if event.type==pygame.KEYDOWN and event.key==pygame.K_DOWN:
                velocity_y=10
                car_y=car_y+velocity_y
                Game_sound['turn'].play()

            if event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT:
                car_x=car_x+6
                Game_sound['turn'].play()

            if event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT:
                car_x=car_x-6
                Game_sound['turn'].play()

#CHEATCODES
            if event.type==pygame.KEYDOWN and event.key==pygame.K_1:
                score=score+5

        crashTest=iscollide(car_x,car_y,uppertruck,lowertruck)
        if crashTest:
            return

#INCRASING THE SCORE WHEN THE CAR 'S x COORDINATE BECOMES MORE THAN THE x COORDINATE OF TRUCK
        Carmidpos=car_x+Game_sprites['car'].get_width()/2
        for truck in lowertruck:
            truckmidpos=truck['x']+Game_sprites['truck'].get_width()/2
            if truckmidpos<Carmidpos<truckmidpos+7:
                score=score+1
                if score>int(hiscore):
                    hiscore=score

#Move truck to the end of screen
        for t1,t2 in zip(uppertruck,lowertruck):
            t1['x']+=truckvelX
            t2['x']+=truckvelX

#MOVE TREES TO THE END OF SCREEN
        for t1,t2 in zip(uppertree,lowertree):
            t1['x']+=treevelX
            t2['x']+=treevelX


#Add new truck when old gets out of the screen
        if 0<uppertruck[0]['x']<10:
            truck = Randomtruck()
            lowertruck.append(truck[0])
            uppertruck.append(truck[1])

#when truck out of screen remove it
        if uppertruck[0]['x']<-32:
            uppertruck.pop(0)
            lowertruck.pop(0)
        

#Add new tree when old gets out of the screen
        if 0<uppertree[0]['x']<10:
            tree = Randomtree()
            lowertree.append(tree[0])
            uppertree.append(tree[1])

#when tree out of screen remove it
        if uppertree[0]['x']<-32:
            uppertree.pop(0)
            lowertree.pop(0)
#Blitting the game
        screen.blit(Game_sprites['road'],(0,0))
        for ut,lt in zip(uppertruck,lowertruck):
            screen.blit(pygame.transform.rotate(Game_sprites['truck'],180),(ut['x'],ut['y']))
            screen.blit(Game_sprites['truck'],(lt['x'],lt['y']))

#ROTATE FUNCTION ROTATES THE TRUCK 180 DEGREE FOR THE TRUCK ABOVE ROAD


        for utt,ltt in zip(uppertree,lowertree):
            screen.blit(Game_sprites['tree'],(utt['x'],utt['y']))
            screen.blit(Game_sprites['tree'],(ltt['x'],ltt['y']))
        

        screen.blit(Game_sprites['car'],(car_x,car_y))
        text_screen(f'Score: {str(score)} Hi Score: {str(hiscore)}',white,6,10)
        pygame.display.update()
        clock.tick(fps)

#EXIT SCREEN
def exit_screen():
    while True:
        for event in pygame.event.get():
            if (event.type==pygame.QUIT) or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): 
                pygame.quit()
                sys.exit()
            elif (event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE):
                return
            else:
                with open("hiscore.txt","w")as f:
                    f.write(str(hiscore))
                screen.blit(Game_sprites['end'],(0,0))
                pygame.display.update()
                clock.tick(fps)

#RUNING THE SCREENS           
while True:
    welcome_screen()
    Maingame()
    exit_screen()