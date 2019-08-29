import pygame
import random
import sys
import os
import time
from pygame.locals import *
import time 
import winsound
import pyttsx3


disp=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
infoObject = pygame.display.Info()
WINDOWWIDTH, WINDOWHEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
line10 = (WINDOWWIDTH-270)//20
TEXTCOLOR = (0, 0, 0)
background=pygame.image.load("image/car1.png")
BACKGROUNDCOLOR = (245, 245, 220)
pygame.image.load("image/car1.png")


FPS = 100
BADDIEMINSIZE = 8
BADDIEMAXSIZE = 8
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 8
PLAYERMOVERATE = line10
print(PLAYERMOVERATE)
count = 3


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    terminate()
                return
def distance_alert(playerRect, baddies):
    freq_left = 10000
    freq_right = 1000
    freq = 5000
    dur = 10
    x_player = playerRect.x
    y_player = playerRect.y

    
    for baddy in baddies:
        x_distance = baddy['rect'].x - x_player
        y_distance = abs( baddy['rect'].y - y_player)

        if x_distance == 0: 
            if y_distance < 6*line10:
                
                winsound.Beep(freq, dur)
        #right
        elif (x_distance > 0) and (x_distance < 2*line10) and (y_distance < 2*line10):
            
            winsound.Beep(freq_right, dur)
        #left
        elif (x_distance < 0) and (abs(x_distance) < 2*line10) and (y_distance < 2*line10):
            
            winsound.Beep(freq_left, dur)

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

# fonts
font = pygame.font.SysFont(None, 30)

# sounds
gameOverSound = pygame.mixer.Sound('music/crash.wav')
pygame.mixer.music.load('music/theme.mp3')
pygame.mixer.music.set_volume(0.25)
laugh = pygame.mixer.Sound('music/laugh.wav')


# Car version images
#playerImage = pygame.image.load('image/car1.png')
#playerImage=pygame.transform.scale(playerImage,[line10,line10])
#car3 = pygame.image.load('image/car3.png')
#car4 = pygame.image.load('image/car4.png')
#playerRect = playerImage.get_rect()
#baddieImage = pygame.image.load('image/car2.png')
#sample = [car3,car4,baddieImage]
wallLeft = pygame.image.load('image/left.png')
wallRight = pygame.image.load('image/right.png')

#knight version images
playerImage = pygame.image.load('image/Knight.png')
playerImage=pygame.transform.scale(playerImage,[line10,line10])
arrow1 = pygame.image.load('image/arrows.png')
arrow2 = pygame.image.load('image/arrows.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('image/arrows.png')
sample = [arrow1,arrow2,baddieImage]
#wallLeft = pygame.image.load('image/Left_side.png')
#wallRight = pygame.image.load('image/Right_side.png')



# "Start" screen
disp.fill((255,255,255))
drawText('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
drawText('And Enjoy', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3) + 30)
pygame.display.update()
engine = pyttsx3.init()
engine.say("Welcome to the new brand game, 'Speed-Of-Sound'")
engine.say("Instractions: Press the keys, left and right to move.")
engine.say("You will need to dash from upcoming arrows")
engine.say("You will hear 3 diffrent voices. They will worn you from hitting an arrow")
engine.say("Press any key to start the game!. Enjoy")
engine.runAndWait()

waitForPlayerToPressKey()
zero = 0
if not os.path.exists("data/save.dat"):
    f = open("data/save.dat",'w')
    f.write(str(zero))
    f.close()   
v = open("data/save.dat",'r')
topScore = int(v.readline())
v.close()
def paused(pause):
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('p'):
                    pause = False
        clock = pygame.time.Clock()
        pygame.display.update()
        clock.tick(15)
score = 0
while (count > 0):
    # start of the game
    baddies = []
    
    playerRect.topleft = (132 + (line10*10), WINDOWHEIGHT/1.2)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop
        score += 1 # increase score

        for event in pygame.event.get():
            
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('p'):
                    pause = True
                    paused(pause)
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()
            

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            

        # Add new baddies at the top of the screen
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = line10 
            randnum = random.randint(0,((WINDOWWIDTH - (132*2)) // line10) - 1)
            newBaddie = {'rect': pygame.Rect((132 + (randnum * PLAYERMOVERATE)), -line10,line10, line10),
                        'speed': random.randint(line10//5,line10//5),
                        'surface':pygame.transform.scale(random.choice(sample), (line10, line10)),
                        }
            baddies.append(newBaddie)
            sideLeft = {'rect': pygame.Rect(0,0,132,WINDOWHEIGHT),        
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallLeft, (132, WINDOWHEIGHT)),
                       }
            baddies.append(sideLeft)
            sideRight = {'rect': pygame.Rect(WINDOWWIDTH - 132,0,132,WINDOWHEIGHT),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallRight, (132, WINDOWHEIGHT)),
                       }
            baddies.append(sideRight)
        # notify if the cars are in the lane
            

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            time.sleep(0.02)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
            time.sleep(0.02)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
            time.sleep(0.02)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)
            time.sleep(0.02)
        
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)
        pygame.Rect(0,0,50,50)
      
      # Draw the score and top score.
        score_rect = pygame.draw.rect(disp, (0,0,0), (175, 75, 200, 100), 2)
        drawText('Score: %s' % (score), font, windowSurface, 200, 100)
        drawText('Top Score: %s' % (topScore), font, windowSurface,200, 120)
        drawText('Rest Life: %s' % (count), font, windowSurface,200, 140)
        
        windowSurface.blit(playerImage, playerRect)

        
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        distance_alert(playerRect, baddies)
        # Check if any of the car have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                g = open("data/save.dat",'w')
                g.write(str(score))
                g.close()
                topScore = score
            break

        mainClock.tick(FPS)

    # "Game Over" screen.
    pygame.mixer.music.stop()
    count = count - 1
    gameOverSound.play()
    time.sleep(1.5)
    engine.say(" %s lives Remaining " % (count) )
    engine.runAndWait()
    time.sleep(4)
    if (count == 0):
        laugh.play()
        drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)

        pygame.display.update()
        engine.say("Your score is:%s" % (score))
        engine.say("Game Over!. Press any key to play again")
        engine.runAndWait()
        time.sleep(2)
        waitForPlayerToPressKey()
        count = 3
        score = 0
        gameOverSound.stop()
        