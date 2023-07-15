import pygame
import os
import time
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space 1v1 by Chilly")

# Colors in RGB format 0 - 255
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("spaceinvader", "assets", "space.png")),
    (WIDTH, HEIGHT))

# Sounds (.mp3)
BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join("spaceinvader", "assets", "hitSound.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join("spaceinvader", "assets", "fireSound.mp3"))

# Hard coded fps and player speed
FPS = 60
VEL = 5

# Bullet settings
BULLET_VEL = 8
MAX_BULLETS = 3

# The border separating players
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Spaceship images
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
UFO_WIDTH, UFO_HEIGHT = 100, 90

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("spaceinvader", "assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("spaceinvader", "assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# UFO
UFO_IMAGE = pygame.image.load(
    os.path.join("spaceinvader", "assets", "UFO.png"))
UFO = pygame.transform.scale(
    UFO_IMAGE, (UFO_WIDTH, UFO_HEIGHT))
UFO_VEL = 1


def draw_window(
    yellow: pygame.Rect,
    red: pygame.Rect,
    ufo_rect: pygame.Rect,
    yellow_bullets: list,
    red_bullets: list,
    yellow_heath: int,
    red_heath: int
):
    # Background
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Health bar
    yellow_health_text = HEALTH_FONT.render(f"Heath {yellow_heath}", 1, WHITE)
    red_heath_text = HEALTH_FONT.render(f"Heath {red_heath}", 1, WHITE)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_heath_text, (WIDTH - red_heath_text.get_width() - 10, 10))

    # Spaceships
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    #UFO
    WIN.blit(UFO, (ufo_rect.x, ufo_rect.y))

    bullet: pygame.Rect
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    bullet: pygame.Rect
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

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
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):  # yellow hits red
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    bullet: pygame.Rect
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL

        if yellow.colliderect(bullet):  # red hits yellow
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    text_width = draw_text.get_width()
    text_height = draw_text.get_height()
    x = WIDTH // 2 - text_width // 2
    y = HEIGHT // 2 - text_height // 2
    WIN.blit(draw_text, (x, y))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    start_time = time.time()

    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    ufo_rect = pygame.Rect(WIDTH // 2 - UFO_WIDTH //2, -100, UFO_WIDTH, UFO_HEIGHT)

    yellow_bullets, red_bullets = [], []
    yellow_health, red_health = 10, 10

    winner_text = ""

    ufo_spawned = False
    ufo_direction = 1  # aka down

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():

            # X-ing a window
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # YELLOW FIRE
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_LCTRL
                    and len(yellow_bullets) < MAX_BULLETS
                ):
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,  # x pos
                        yellow.y + yellow.height//2 + 5,  # y pos
                        10, 5)  # width and height
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                # RED FIRE
                if (
                    event.key == pygame.K_RCTRL
                    and len(red_bullets) < MAX_BULLETS
                ):
                    bullet = pygame.Rect(
                        red.x,  # x pos
                        red.y + red.height//2 + 5,  # y pos
                        10, 5)  # width and height
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                BULLET_HIT_SOUND.play()
                yellow_health -= 1

            if event.type == RED_HIT:
                BULLET_HIT_SOUND.play()
                red_health -= 1

        if red_health <= 0:
            winner_text = "Yellow wins"

        if yellow_health <= 0:
            winner_text = "Red wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

        time_now = time.time()
        passed_time = time_now - start_time

        if passed_time > 10.0 and not ufo_spawned:
            ufo_spawned = True

        if ufo_spawned:
            ufo_rect.y += UFO_VEL * ufo_direction
        
        if ufo_rect.y > 200:
            ufo_direction = -1

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(yellow, keys_pressed)
        handle_red_movement(red, keys_pressed)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red,
                    ufo_rect,
                    yellow_bullets, red_bullets,
                    yellow_health, red_health)

    main()


if __name__ == "__main__":
    main()
