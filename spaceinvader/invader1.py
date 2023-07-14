import pygame
import os


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space 1v1 by Chilly")

# Colors in RGB format 0 - 255
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Hard coded fps
FPS = 60
VEL = 5
BULLET_VEL = 8
MAX_BULLETS = 3

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

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
    pygame.draw.rect(WIN, BLACK, BORDER)

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    pygame.display.update()


def handle_yellow_movement(yellow: pygame.Rect, keys_pressed: pygame.key):

    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # yellow up
        yellow.y -= VEL
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # yellow left
        yellow.x -= VEL
    if (
        keys_pressed[pygame.K_s]
        and yellow.y + VEL + yellow.height < HEIGHT - 15
    ):  # yellow down
        yellow.y += VEL
    if (
        keys_pressed[pygame.K_d]
        and yellow.x + VEL + yellow.width < BORDER.x
    ):  # yellow right
        yellow.x += VEL


def handle_red_movement(red: pygame.Rect, keys_pressed: pygame.key):

    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # red up
        red.y -= VEL
    if (
        keys_pressed[pygame.K_LEFT]
        and red.x - VEL > BORDER.x + BORDER.width
    ):  # red left
        red.x -= VEL
    if (
        keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15
    ):  # red down
        red.y += VEL
    if (
        keys_pressed[pygame.K_RIGHT]
        and red.x + VEL + red.width < WIDTH
    ):  # red right
        red.x += VEL


def handle_bullets(
    yellow_bullets: list,
    red_bullets: list,
    yellow: pygame.Rect,
    red: pygame.Rect
):
    bullet: pygame.Rect
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, BLACK, bullet)
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):  # yellow hits red
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

    bullet: pygame.Rect
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        pygame.draw.rect(WIN, BLACK, bullet)

        if yellow.colliderect(bullet):  # red hits yellow
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)


def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets, red_bullets = [], []

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            # YELLOW FIRE
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_LCTRL
                    and len(yellow_bullets) < MAX_BULLETS
                ):
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,  # x pos
                        yellow.y + yellow.height//2 - 2,  # y pos
                        10, 5)  # width and height
                    yellow_bullets.append(bullet)

                # RED FIRE
                if (
                    event.key == pygame.K_RCTRL
                    and len(red_bullets) < MAX_BULLETS
                ):
                    bullet = pygame.Rect(
                        red.x,  # x pos
                        yellow.y + red.height//2 - 2,  # y pos
                        10, 5)  # width and height
                    red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(yellow, keys_pressed)
        handle_red_movement(red, keys_pressed)

        draw_window(yellow, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

    pygame.quit()


if __name__ == "__main__":
    main()
