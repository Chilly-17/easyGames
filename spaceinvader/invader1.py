import pygame
import os
import time
import random
pygame.font.init()
pygame.mixer.init()


# Dimensions
WIDTH, HEIGHT = 900, 500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
UFO_WIDTH, UFO_HEIGHT = 50, 75
EXPLOSION_WIDTH, EXPLOSION_HEIGHT = 100, 100

# Game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space 1v1 by Chilly")

# Colors in RGB format 0 - 255, used in the project
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Static objects
SPACE_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Sounds (.mp3)
BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join("spaceinvader", "assets", "hitSound.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join("spaceinvader", "assets", "fireSound.mp3"))
UFO_LASER_SOUND = pygame.mixer.Sound(
    os.path.join("spaceinvader", "assets", "ufoLaser.mp3"))

# Hard coded fps and object speed
FPS = 60
VEL = 5
BULLET_VEL = 8
LASER_VEL = 10
UFO_VEL = 1

# Maximums
MAX_BULLETS = 3

# Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
UFO_TOP = pygame.USEREVENT + 3
UFO_BOTTOM = pygame.USEREVENT + 4
YELLOW_HIT_UFO = pygame.USEREVENT + 5
RED_HIT_UFO = pygame.USEREVENT + 6

# PNGs
SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("spaceinvader", "assets", "space.png")),
    (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("spaceinvader", "assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("spaceinvader", "assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

UFO_IMAGE = pygame.image.load(
    os.path.join("spaceinvader", "assets", "UFO.png"))
UFO = pygame.transform.scale(
    UFO_IMAGE, (UFO_WIDTH, UFO_HEIGHT))

EXPLOSION_IMAGE = pygame.image.load(
    os.path.join("spaceinvader", "assets", "explosion.png"))
EXPLOSION = pygame.transform.scale(
    EXPLOSION_IMAGE, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))

# Timers
UFO_SPAWN = 0  # time in seconds


def draw_window(
    yellow: pygame.Rect,
    red: pygame.Rect,
    ufo_rect: pygame.Rect,
    yellow_bullets: list,
    red_bullets: list,
    yellow_heath: int,
    red_heath: int,
    yellow_lasers: list,
    red_lasers: list,
    exploded: bool
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

    # UFO
    if not exploded and exploded is not None:
        WIN.blit(
            EXPLOSION, (
                ufo_rect.x - EXPLOSION_WIDTH // 2 + UFO_WIDTH // 2,
                ufo_rect.y - EXPLOSION_HEIGHT // 2 + UFO_HEIGHT // 2
            ))

    WIN.blit(UFO, (ufo_rect.x, ufo_rect.y))

    bullet: pygame.Rect
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    bullet: pygame.Rect
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    laser: pygame.Rect
    for laser in yellow_lasers:
        pygame.draw.rect(WIN, GREEN, laser)

    for laser in red_lasers:
        pygame.draw.rect(WIN, GREEN, laser)
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


# moves the bullets and lasers, checks for collisions
def handle_bullets(
    yellow_bullets: list,
    red_bullets: list,
    yellow: pygame.Rect,
    red: pygame.Rect,
    ufo_rect: pygame.Rect,
    yellow_lasers: list,
    red_lasers: list
):
    bullet: pygame.Rect
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):  # yellow hits red
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif ufo_rect.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT_UFO))

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    bullet: pygame.Rect
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL

        if yellow.colliderect(bullet):  # red hits yellow
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

        elif ufo_rect.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT_UFO))

        elif bullet.x < 0:
            red_bullets.remove(bullet)

    laser: pygame.Rect
    for laser in yellow_lasers:
        laser.x -= LASER_VEL

        if laser.x < -100:
            yellow_lasers.remove(laser)

        elif laser.colliderect(yellow):
            yellow_lasers.remove(laser)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))

    laser: pygame.Rect
    for laser in red_lasers:
        laser.x += LASER_VEL

        if laser.x > WIDTH + 100:
            red_lasers.remove(laser)

        elif laser.colliderect(red):
            red_lasers.remove(laser)
            pygame.event.post(pygame.event.Event(RED_HIT))


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    text_width = draw_text.get_width()
    text_height = draw_text.get_height()
    x = WIDTH // 2 - text_width // 2
    y = HEIGHT // 2 - text_height // 2
    WIN.blit(draw_text, (x, y))
    pygame.display.update()
    pygame.time.delay(5000)


# functions for:
    # moving the ufo
    # creating laser objects, which target both red and yellow
    # "deleting ufo" (just puts it not in the players view)
class Ufo:

    def __init__(self, ufo_rect: pygame.Rect, isDead: bool):
        self.ver = 1
        self.hor = random.randrange(-2, 2)
        self.ufo = ufo_rect
        self.isDead = isDead

    def move(self, start_time: float):
        if self.isDead:
            self.ufo.y = -100
        else:
            now_time = time.time()
            if now_time - start_time > UFO_SPAWN:
                self.movement()

    def movement(self):
        self.ufo.y += UFO_VEL * self.ver
        self.ufo.x += self.hor
        if self.ufo.y < 0 - 100:
            self.ver = 1
            self.hor = random.randrange(-2, 2)
        if self.ufo.y > HEIGHT + 100:
            self.ver = -1
            self.hor = random.randrange(-2, 2)
        if self.ufo.x > WIDTH + 100:
            self.hor = random.randrange(-2, 0)
        if self.ufo.x < 0 - 100:
            self.hor = random.randrange(0, 2)

    def shoot_yellow(self, tick: int):
        if tick % 60 == 0 and self.ufo.colliderect(SPACE_RECT):
            laser: pygame.Rect = pygame.Rect(
                self.ufo.x - 50,
                self.ufo.y + self.ufo.height // 2 + 5,
                50,
                5
            )
            UFO_LASER_SOUND.play()
            return laser

    def shoot_red(self, tick: int):
        if tick % 60 == 48 and self.ufo.colliderect(SPACE_RECT):
            laser: pygame.Rect = pygame.Rect(
                self.ufo.x + self.ufo.width,
                self.ufo.y + self.ufo.height // 2 + 5,
                50,
                5
            )
            UFO_LASER_SOUND.play()
            return laser

    def explode(self, ufo_explode_starting_tick, tick: int, explode_starting_tick):

        if explode_starting_tick == 0:  # sets starting tick to current one
            explode_starting_tick = tick

        print(tick - explode_starting_tick)
        return tick - explode_starting_tick >= 60


def main():

    # time variables
    tick = 0
    start_time = time.time()
    clock = pygame.time.Clock()
    ufo_explode_starting_tick = 0

    # hit-boxes
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    ufo_rect = pygame.Rect(
        WIDTH // 2 - UFO_WIDTH // 2, -100, UFO_WIDTH, UFO_HEIGHT)

    # bullets and lasers
    yellow_bullets, red_bullets = [], []
    yellow_lasers, red_lasers = [], []

    # health variables
    yellow_health, red_health = 10, 10
    ufo_health = 25

    # color of the player who won
    winner_text = ""

    # ufo related variables
    ufo = Ufo(ufo_rect, isDead=False)
    ufo_targets_red, ufo_targets_yellow = False, False

    # events
    exploded = None
    is_tick_set = False

    run = True
    while run:
        tick += 1
        print(f"tick: {tick}")
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

            # Hits
            if event.type == YELLOW_HIT:
                BULLET_HIT_SOUND.play()
                yellow_health -= 1
            if event.type == RED_HIT:
                BULLET_HIT_SOUND.play()
                red_health -= 1
            if event.type == YELLOW_HIT_UFO:
                BULLET_HIT_SOUND.play()
                ufo_targets_yellow = True
                ufo_health -= 1
            if event.type == RED_HIT_UFO:
                BULLET_HIT_SOUND.play()
                ufo_targets_red = True
                ufo_health -= 1

        if ufo_targets_yellow:
            yellow_laser = ufo.shoot_yellow(tick)
            if yellow_laser is not None:
                yellow_lasers.append(yellow_laser)
        if ufo_targets_red:
            red_laser = ufo.shoot_red(tick)
            if red_laser is not None:
                red_lasers.append(red_laser)

        if red_health <= 0:
            winner_text = "Yellow wins"
        if yellow_health <= 0:
            winner_text = "Red wins"

        if ufo_health <= 0:
            exploded = ufo.explode(is_tick_set, tick, ufo_explode_starting_tick)
            print(exploded)
            print()
            if exploded:
                ufo = Ufo(ufo_rect, isDead=True)

        if winner_text != "":
            draw_winner(winner_text)
            break

        ufo.move(start_time)

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(yellow, keys_pressed)
        handle_red_movement(red, keys_pressed)

        # moves the bullets and lasers, checks for collisions
        handle_bullets(
            yellow_bullets, red_bullets,
            yellow, red,
            ufo_rect,
            yellow_lasers, red_lasers
        )

        # draws the background
        # images of spaceships and the ufo,
        # bullets and lasers and players' health
        draw_window(yellow, red,
                    ufo_rect,
                    yellow_bullets, red_bullets,
                    yellow_health, red_health,
                    yellow_lasers, red_lasers,
                    exploded
                    )

    # if the while loop is broken by a player winning
    # the game loops again
    main()


if __name__ == "__main__":
    main()
