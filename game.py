import random  # for generating random number ...game need randomness it is a module  for flappy bird pipe
import sys         # for exiting the game when pressed X 
import pygame       
from pygame.locals import *      # Basic pygame imports

# Global variable 
FPS = 32   # Frame per sec...No of img randering
SCREENWIDTH = 289
SCREENHEIGHT =511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))          # Initial window...Creates a screen ----- Dimensionals and coordinates
GROUNDY = SCREENHEIGHT * 0.8   #     base.png
GAME_SPRITES ={}          #display img
GAME_AUDIO ={}   # play audio
PLAYER = 'sprite/flap.png'
BACKGROUND ='sprite/bag.png'
PIPE ='sprite/pipe.png'

def welcome():
    """ Shows welcome image"""
    playerx = int(SCREENWIDTH/5)
    playery= int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex= int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey= int(SCREENHEIGHT*0.13)
    basex=0
    while True:
        for event in pygame.event.get():           # key and click is told by pygame.event.get
            # If user clickes X button
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):     # for escaping
                pygame.quit()
                sys.exit()

                # If the user presses space or upkey start the game for them
            elif event.type==KEYDOWN and (event.key == K_SPACE or event.key== K_UP):
                return
            else:
                # BLIT ---copy image
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()     # Screen doesnt channge until this func
                FPSCLOCK.tick(FPS)
    
def maingame():
    score = 0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENHEIGHT/2)    #position of bird
    basex=0
    
    # create two pipes for bliting on screen
    newpipe1 = getRandompipe()
    newpipe2 = getRandompipe()

    # list of upper pipes
    upperpipes = [
        {'x':SCREENWIDTH+200, 'y':newpipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newpipe2[1]['y']}
    ]
    lowerpipes = [
        {'x':SCREENWIDTH+200, 'y':newpipe2[0]['y']},
        {'x':SCREENWIDTH+200*(SCREENWIDTH/2), 'y':newpipe2[1]['y']}
        
    ]
    pipevelx = -4
    playervely=-9
    playerMaxvely =10
    playerMinvely =-8
    playerAccy=1 

    playerFlapVel =-8  #bird spped while flaapping
    playerFlapped =False #only true when bird is flying

    while True:
        for event in pygame.event.get():
            if event.type ==quit or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key == K_SPACE or event.key== K_UP):
                if playery > 0:
                    playervely =playerFlapVel
                    playerFlapped=True
                    GAME_AUDIO['wing'].play()
        
        crashTest =isCollide(playerx,playery,upperpipes,lowerpipes) # returns true if player crashed
        if crashTest:
            return

        #check score
        playerMeid = playerx + GAME_SPRITES['player'].get_width()/2      
        for pipe in upperpipes:
            pipeMid = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2  
            if pipeMid<=playerMeid<pipeMid+4:
                score+=1
                print(f"Your score is {score}")
                GAME_AUDIO['point'].play()
        if playervely<playerMaxvely and not playerFlapped:
            playervely += playerAccy

        if playerFlapped:
            playerFlapped =False
        playerheight =GAME_SPRITES['player'].get_height()
        playery =playery+min(playervely,GROUNDY -playery -playerheight)
        # move pipes to left
        for upperp,lowerp in  zip(upperpipes,lowerpipes):    # zip -----  combines 1st element of each list....then 2nd...3rd
            upperp['x']+=pipevelx
            lowerp['x']+=pipevelx
            #add a new pipe when first is abt to go to the leftmost part of screen
        if 0< upperpipes[0]['x']<5:
            newpipes =getRandompipe()
            upperpipes.append(newpipes[0])
            lowerpipes.append(newpipes[1])


        # pipe is out of screen remove it
        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        # let blit our sprites

        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperp,lowerp in  zip(upperpipes,lowerpipes):    # zip -----  combines 1st element of each list....then 2nd...3rd
            upperp['x']+=pipevelx
            lowerp['x']+=pipevelx
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperp['x'],upperp['y']))   
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerp['x'],lowerp['y'])) 

        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))

        mydigits =[int(x) for x in list(str(score))]
        width =0
        for digit in mydigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset =(SCREENWIDTH-width)/2
        
        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset,SCREENHEIGHT*0.12))
            xoffset+=GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update()     # Screen doesnt channge until this func
            FPSCLOCK.tick(FPS)

       
def isCollide(playerx,playery,upperpipes,lowerpipes):
    return False

def getRandompipe():
    # generate position of 2 pipes 1. straight and 2. toprotated

    pipeheight= GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height( )-1.2*offset))
    pipex =SCREENWIDTH+10
    y1 =pipeheight-y2+offset
    pipe =[
        {'x':pipex, 'y': -y1},    #upper pipe
        {'x':pipex, 'y': y2}
    ]
    return pipe
    
        

    


if __name__ == '__main__':   # THIS will be the main point from where our game will start.
    pygame.init()            # Initialize all pygame's module
    FPSCLOCK =pygame.time.Clock()     # controls fps of game i.e. no more frame higher than given clock value
    pygame.display.set_caption('Flappy bird by rashmi')           # sets caption on window
    GAME_SPRITES['numbers'] =( 
        pygame.image.load('sprite/10.png').convert_alpha(),
        pygame.image.load('sprite/1.png').convert_alpha(),
        pygame.image.load('sprite/2.png').convert_alpha(),
        pygame.image.load('sprite/3.png').convert_alpha(),
        pygame.image.load('sprite/4.png').convert_alpha(),
        pygame.image.load('sprite/5.png').convert_alpha(),
        pygame.image.load('sprite/6.png').convert_alpha(),
        pygame.image.load('sprite/7.png').convert_alpha(),
        pygame.image.load('sprite/8.png').convert_alpha(),
        pygame.image.load('sprite/9.png').convert_alpha(),
    ) # convert alpha is used for faster randering or optimizations

    GAME_SPRITES['message'] =pygame.image.load('sprite/message.webp').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('sprite/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),  #pygame.transform.rotate to rotate image by 180
    pygame.image.load(PIPE).convert_alpha()
    )

    # GAME SOUNDS
    GAME_AUDIO['die'] = pygame.mixer.Sound('audio/die.mp3')
    GAME_AUDIO['hit'] = pygame.mixer.Sound('audio/hit.mp3')
    GAME_AUDIO['point'] = pygame.mixer.Sound('audio/point.mp3')
    GAME_AUDIO['wing'] = pygame.mixer.Sound('audio/wing.mp3')
    GAME_AUDIO['swoosh'] = pygame.mixer.Sound('audio/swoosh.mp3')


    GAME_SPRITES['background'] =pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] =pygame.image.load(PLAYER).convert_alpha()
    
    while True:
        welcome()                    # show welcome untile button not pressed
        maingame()                # main game function




