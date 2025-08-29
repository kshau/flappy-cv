import pygame
pygame.init()

import math
import random
import os

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

FPS = int(os.environ["FPS"])

class Ground:
    def __init__(self, x):
        self.x = x
          
class Pipe:
    def __init__(self, x, y):
        self.x = x
        self.y = y

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy")

clock = pygame.time.Clock()

bird_img = pygame.image.load("./assets/bird.png")
bird_img = pygame.transform.rotozoom(bird_img, 0, 1.2)

ground_img = pygame.image.load("./assets/ground.png")
ground_img = pygame.transform.rotozoom(ground_img, 0, 1.2)
ground_img_width = ground_img.get_width()
ground_img_height = ground_img.get_height()

background_img = pygame.image.load("./assets/background.png")
background_img = pygame.transform.rotozoom(background_img, 0, 1.2)

pipe_img = pygame.image.load("./assets/pipe.png")
pipe_img = pygame.transform.rotozoom(pipe_img, 0, 1.2)
pipe_img_flipped = pygame.transform.flip(pipe_img, False, True)
pipe_img_width = pipe_img.get_width()
pipe_img_height = pipe_img.get_height()

pipe_gap = 230
pipe_spacing = 220

num_initial_grounds = math.ceil(SCREEN_WIDTH / ground_img_width) + 2
grounds = []
for i in range(num_initial_grounds):
    grounds.append(Ground(i * ground_img_width))
    
pipes = []

bird_y = SCREEN_WIDTH / 2

def handle_grounds():
    global grounds

    new_grounds = []
    for ground in grounds:
        if ground.x + ground_img_width >= 0:
            new_grounds.append(ground)
        ground.x -= 5
        screen.blit(ground_img, (ground.x, SCREEN_HEIGHT - ground_img_height + 50))

    if not new_grounds or new_grounds[-1].x + ground_img_width < SCREEN_WIDTH:
        new_grounds.append(Ground(new_grounds[-1].x + ground_img_width if new_grounds else SCREEN_WIDTH))

    grounds = new_grounds
    

def handle_pipes():
    global pipes
     
    new_pipes = []
    for pipe in pipes:
        if pipe.x + pipe_img_width >= 0:
            new_pipes.append(pipe)
        pipe.x -= 5
        screen.blit(pipe_img_flipped, (pipe.x, pipe.y - 50))
        screen.blit(pipe_img, (pipe.x, pipe_gap + pipe.y + 200))

    if not new_pipes or new_pipes[-1].x + pipe_spacing < SCREEN_WIDTH:
        #-250
        new_pipes.append(Pipe(new_pipes[-1].x + pipe_spacing if new_pipes else SCREEN_WIDTH, random.randint(-250, -80)))

    pipes = new_pipes

def run_game(delta_left_eye_y):
    global bird_y, grounds, pipes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    screen.blit(background_img, (0, -50))
    screen.blit(background_img, (background_img.get_width(), -50))

    handle_pipes()
    handle_grounds()

    bird_y += delta_left_eye_y * 2
    screen.blit(bird_img, (100, bird_y))

    pygame.display.flip()
    clock.tick(FPS)

    return True