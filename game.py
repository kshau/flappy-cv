import pygame
pygame.init()

import math
import random
import os

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

PIPE_GAP_X = 220
PIPE_GAP_Y = 230

FPS = int(os.environ["FPS"])

class Ground:
    def __init__(self, x):
        self.x = x
          
class Pipe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.scored = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy")

clock = pygame.time.Clock()

bird_imgs = [
    pygame.transform.rotozoom(pygame.image.load("./assets/bird/bird-downflap.png"), 0, 1.2),
    pygame.transform.rotozoom(pygame.image.load("./assets/bird/bird-midflap.png"), 0, 1.2),
    pygame.transform.rotozoom(pygame.image.load("./assets/bird/bird-upflap.png"), 0, 1.2)
]
bird_img_height = bird_imgs[0].get_height()

bird_imgs_current_idx = 0

ground_img = pygame.image.load("./assets/ground.png")
ground_img = pygame.transform.rotozoom(ground_img, 0, 1.2)
ground_img_width = ground_img.get_width()
ground_img_height = ground_img.get_height()
ground_y = SCREEN_HEIGHT - ground_img_height + 50

background_img = pygame.image.load("./assets/background.png")
background_img = pygame.transform.rotozoom(background_img, 0, 1.2)

pipe_img = pygame.image.load("./assets/pipe.png")
pipe_img = pygame.transform.rotozoom(pipe_img, 0, 1.2)
pipe_img_flipped = pygame.transform.flip(pipe_img, False, True)
pipe_img_width = pipe_img.get_width()
pipe_img_height = pipe_img.get_height()

game_over_img = pygame.image.load("./assets/game-over.png")
game_over_img = pygame.transform.rotozoom(game_over_img, 0, 1.2)
game_over_img_width = game_over_img.get_width()

score_font = pygame.font.Font("./assets/flappy-font.ttf", 50)
restart_font = pygame.font.Font("./assets/flappy-font.ttf", 20)

num_initial_grounds = math.ceil(SCREEN_WIDTH / ground_img_width) + 2
grounds = []
for i in range(num_initial_grounds):
    grounds.append(Ground(i * ground_img_width))

game_state = "waiting"
frame_count = 0

pipes = []

bird_y = SCREEN_WIDTH / 2
bird_yv = 0

score = 0

def do_game_over():
    global game_state
    game_state = "ended"

def restart_game():
    global game_state, score, pipes, bird_y
    game_state = "waiting"
    score = 0
    pipes = []
    bird_y = SCREEN_WIDTH / 2

def handle_grounds():
    global grounds

    new_grounds = []
    for ground in grounds:

        if ground.x + ground_img_width >= 0:
            new_grounds.append(ground)

        if game_state != "ended":
            ground.x -= 5

        screen.blit(ground_img, (ground.x, ground_y))

    if not new_grounds or new_grounds[-1].x + ground_img_width < SCREEN_WIDTH:
        new_grounds.append(Ground(new_grounds[-1].x + ground_img_width if new_grounds else SCREEN_WIDTH))

    grounds = new_grounds
    

def handle_pipes(bird_rect):

    global pipes, game_state, score
     
    new_pipes = []

    for pipe in pipes:

        if pipe.x + pipe_img_width >= 0:
            new_pipes.append(pipe)

        if game_state == "playing":

            pipe.x -= 5

            top_pipe_rect = pygame.Rect(pipe.x, pipe.y - 50, pipe_img_width, pipe_img_height)
            bottom_pipe_rect = pygame.Rect(pipe.x, PIPE_GAP_Y + pipe.y + 200, pipe_img_width, pipe_img_height)

            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                do_game_over()

            if not pipe.scored and pipe.x + pipe_img_width // 2 < 100:
                score += 1
                pipe.scored = True

        screen.blit(pipe_img_flipped, (pipe.x, pipe.y - 50))
        screen.blit(pipe_img, (pipe.x, PIPE_GAP_Y + pipe.y + 200))

    if not new_pipes or new_pipes[-1].x + PIPE_GAP_X < SCREEN_WIDTH:
        new_pipes.append(Pipe(new_pipes[-1].x + PIPE_GAP_X if new_pipes else SCREEN_WIDTH, random.randint(-250, -80)))

    pipes = new_pipes

def run_game(delta_left_eye_y):

    global bird_y, bird_yv, grounds, pipes, frame_count, bird_imgs_current_idx, game_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "waiting":
                    game_state = "playing"
                elif game_state == "ended":
                    restart_game()

    screen.blit(background_img, (0, -50))
    screen.blit(background_img, (background_img.get_width(), -50))

    bird_rect = bird_imgs[0].get_rect(topleft=(100, bird_y))
    handle_pipes(bird_rect)

    handle_grounds()

    if game_state == "ended":
        screen.blit(game_over_img, ((SCREEN_WIDTH / 2) - (game_over_img_width / 2), 180))
        restart_text = restart_font.render("Press SPACE to restart", True, (255, 255, 255))
        screen.blit(restart_text, ((SCREEN_WIDTH - restart_text.get_width()) // 2, 250))

    else:

        if frame_count % 5 == 0:
            bird_imgs_current_idx += 1
            if bird_imgs_current_idx > len(bird_imgs) - 1:
                bird_imgs_current_idx = 0

        bird_yv += delta_left_eye_y

    bird_yv *= 0.75
    bird_y += bird_yv

    if game_state == "playing" and (bird_y + bird_img_height > ground_y):
        bird_y = ground_y - bird_img_height
        do_game_over()

    rotated_bird_img = pygame.transform.rotozoom(bird_imgs[bird_imgs_current_idx], -2 * bird_yv, 1.0)
    screen.blit(rotated_bird_img, (100, bird_y))

    if game_state != "waiting":
        score_text = score_font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH / 2 - 20, 40))

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

    return True