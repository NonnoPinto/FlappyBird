#pygame flappyBird
#fatto grazie a https://www.geeksforgeeks.org/how-to-make-flappy-bird-game-in-pygame/

import random #for random heights
import sys
import pygame
from pygame.locals import*

#variabili globali
window_width = 600
window_height = 499

#settare altezza e larghezza
window = pygame.display.set_mode((window_width, window_height)) #da provare pygame.FULLSCREEN
elevation = window_height * 0.8
game_images = {}
fps = 32
pipeimage = 'images/pipe.png'
bk_image = 'images/bk.jpg'
birdpl_image = 'images/bird.png'
sealevel_image = 'images/base.jfif'

def createPipe():
    offset = window_height/3
    pipeHeight = game_images['pipeimage'][0].get_height()

    y2 = offset + random.randrange(0, int(window_height - game_images['sea_level'].get_height()))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset

    pipe = [
        #tubo sopra
        {'x': pipeX, 'y': -y1},
        #tubo sotto
        {'x': pipeX, 'y': y2}
    ]
    return pipe

#ma quando perde sto sfigato?
def isGameOver(hor, vert, up_pipes, down_pipes):
    #livello del mare
    if vert > elevation - 25 or vert < 0:
        return True
    #se ha beccato il palo sopra
    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if (vert < pipeHeight +  pipe['y'] and abs(hor - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
    #o magari quello sotto
    for pipe in down_pipes:
        if (vert + game_images['flappybird'].get_height() > pipe['y']) and abs(hor - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True

    #altrimenti non stai facendo schifo
    return False

def flappygame():
    score = 0
    hor = int(window_width/5)
    vert = int(window_width/2)
    ground = 0
    mytempheight = 100

    #primi due tubi
    first_pipe = createPipe()
    second_pipe = createPipe()

    #list di tubi inferiori
    down_pipes = [
        {'x': window_width+300-mytempheight,
        'y': first_pipe[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),
        'y': second_pipe[1]['y']},
    ]

    #list di tubi superiori
    up_pipes = [
        {'x': window_width+300-mytempheight,
        'y': first_pipe[0]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),
        'y': second_pipe[0]['y']},
    ]

    pipeVelX = -4

    bird_velY = -9
    bird_maxY = 10
    bird_velX = -8
    bird_AccY = 1
    bird_flap = -8
    bird_flapped = False
    while True:
        #leggo i comandi da tastiera
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vert > 0:
                    bird_velY = bird_flap
                    bird_flapped = True
        
        game_over = isGameOver(hor, vert, up_pipes, down_pipes)
        if game_over:
            return

        #controllo punteggio
        playerMidPos = hor + game_images['flappybird'].get_width()
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Yout score is {score}")

        if bird_velY < bird_maxY and not bird_flapped:
            bird_velY += bird_AccY
        
        if bird_flapped:
            bird_flapped = False
        
        playerHeight = game_images['flappybird'].get_height()
        vert = vert + min(bird_velY, elevation - vert - playerHeight)

        #sposto i tubi
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
        
        #nuovo tubo
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])
        
        #tolgo il tubo uscito dallo schermo
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
        
        #disegniamo il mondo
        window.blit(game_images['bk'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))
        
        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (hor, vert))
        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(score))]
        width = 0
          
        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1
          
        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num], (Xoffset, window_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()
              
        # Refreshing the game window and displaying the score.
        pygame.display.update()

        fps_clock.tick(fps)

#inizio del gioco
if __name__ == "__main__":

    #per i moduli di pygame
    pygame.init()
    fps_clock = pygame.time.Clock()

    #titolo
    pygame.display.set_caption(('Flappy Bird'))

    #carica le immagini
    game_images['scoreimages'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha(),
    )
    game_images['flappybird'] = pygame.image.load((birdpl_image)).convert_alpha()
    game_images['sea_level'] = pygame.image.load((sealevel_image)).convert_alpha()
    game_images['bk'] = pygame.image.load((bk_image)).convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
                                pygame.image.load(pipeimage).convert_alpha())
    
    print("Benvenuto su Flappy Bird")
    print("Premi lo spazio per giocare")
    
    #da dove parte l'uccellino?
    hor = int(window_width/5)
    vert = int((window_height - game_images['flappybird'].get_height()))

    #imposto livello del mare
    ground = 0
    while True:
        for event in pygame.event.get():

            #per uscire dal gioco
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()

                sys.exit()

            #se invece il tipo sa giocare
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                flappygame()
            
            #ogni volta che non tocco nulla
            else:
                window.blit(game_images['bk'], (0,0))
                window.blit(game_images['flappybird'], (hor, vert))
                window.blit(game_images['sea_level'], (ground, elevation))

                #refresh dello schermo
                pygame.display.update()

                fps_clock.tick(fps)