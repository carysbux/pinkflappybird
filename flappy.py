import pygame
from pygame.locals import *
import random

pygame.init()


clock = pygame.time.Clock()
fps = 60

screen_width = 864

screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Flappy Bird')


#define game variables




ground_scroll = 0

scroll_speed = 5 #pixels

flying = False

game_over = False

pipe_gap = 350 #pixels


pipe_frequency = 1500 #milliseconds

last_pipe = pygame.time.get_ticks() - pipe_frequency #starts as soon as game does

#load background and images

bg = pygame.image.load('images/bg.png')

ground_img = pygame.image.load('images/ground.png')

button_img = pygame.image.load('images/start_btn.png')


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    
#sprite classes

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0 #starts with first imnage
        self.counter = 0 #controlling animation speed

        for num in range (1,4): 
            img = pygame.image.load(f'images/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
    
        #gravity 
        if flying:
            self.vel += 0.5
        if self.vel > 8:
            self.vel = 8
        if self.rect.top <= 0:
            self.vel = 0
        if self.rect.bottom < 768:
            self.rect.y += int(self.vel)

        if game_over == False:
            #jumping
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            flap_cool = 5

            if self.counter > flap_cool:
                self.counter = 0
                self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

        
            
        #rotating bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:  
            self.image = pygame.transform.rotate(self.images[self.index], -90)
        
 #keeping track of alll the birds       

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/pipe.png')
        self.rect = self.image.get_rect()
        #pos 1 is from the top, -1 is from bottom

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


    def draw(self):

        action = False 

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if pygame.mouse.get_pressed()[0] == 1:
                action = True


        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action




bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

button = Button(screen_width // 3, screen_height // 2 - 75, button_img)


run = True 
while run:

    clock.tick(fps)

    screen.blit(bg, (0,0))

    #add bird

    bird_group.update()

    bird_group.draw(screen)
    
   
    pipe_group.draw(screen)
    pipe_group.update()


    screen.blit(ground_img, (ground_scroll, 768))

    # check collisions w tubes

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # double T/F above, true results in deleting collided object 


    # see if bird fell yet
    
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        # game running so generate new pipes

        time_now = pygame.time.get_ticks()
        
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
             
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now




        ground_scroll -= scroll_speed 
        if abs(ground_scroll) > 35:
            ground_scroll = 0
            pipe_group.update()



    if game_over == True:
       if button.draw() == True:
           game_over = False
           reset_game()


    #make image move by adjusting x coord (replacing 0 w groundf scroll)
    #event handling

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()
