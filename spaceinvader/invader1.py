import pygame
import os


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space 1v1 by Chilly")

# Colors in RGB format 0 - 255
WHITE = (255, 255, 255)

# Hard coded fps
FPS = 60
VEL = 5

# Spaceship images
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("spaceinvader", "assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("spaceinvader", "assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def draw_window(yellow: pygame.Rect, red: pygame.Rect):
    WIN.fill(WHITE)

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    pygame.display.update()


def handle_yellow_movement(yellow: pygame.Rect, keys_pressed: pygame.key):

    if keys_pressed[pygame.K_w]:  # yellow up
        yellow.y -= VEL
    if keys_pressed[pygame.K_a]:  # yellow left
        yellow.x -= VEL
    if keys_pressed[pygame.K_s]:  # yellow down
        yellow.y += VEL
    if keys_pressed[pygame.K_d]:  # yellow right
        yellow.x += VEL


def handle_red_movement(red: pygame.Rect, keys_pressed: pygame.key):

    if keys_pressed[pygame.K_UP]:  # red up
        red.y -= VEL
    if keys_pressed[pygame.K_LEFT]:  # red left
        red.x -= VEL
    if keys_pressed[pygame.K_DOWN]:  # red down
        red.y += VEL
    if keys_pressed[pygame.K_RIGHT]:  # red right
        red.x += VEL


def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(yellow, keys_pressed)
        handle_red_movement(red, keys_pressed)

        draw_window(yellow, red)

    pygame.quit()


if __name__ == "__main__":
    main()
