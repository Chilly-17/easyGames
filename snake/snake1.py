import pygame

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dimensions
WIDTH = 500
ROWS = 20

# Screen
WIN = pygame.display.set_mode((WIDTH, WIDTH))


class Cube(object):

    def __innit__(self, start, dirnx=1, dirny=0, color=RED):
        pass

    def move(self, dirnx, dirny):
        pass

    def draw(self, surface, eyes=False):
        pass


class Snake(object):

    body: list = []
    turns: set = {}

    def __init__(self, color: tuple[int, int, int], pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        for _ in keys:
            if keys[pygame.K_A]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:] = [self.dirnx, self.dirny]]
            if keys[pygame.K_D]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:] = [self.dirnx, self.dirny]]
            if keys[pygame.K_W]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:] = [self.dirnx, self.dirny]]
            if keys[pygame.K_S]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:] = [self.dirnx, self.dirny]]

    def reset(self, pos):
        pass

    def addCube(self):
        pass

    def draw(self, surface):
        pass


def drawGrid(w, rows, surface):
    sizeBetween = w // rows

    x = 0
    y = 0
    for _ in range(rows):

        x += sizeBetween
        y += sizeBetween

        pygame.draw.line(surface, WHITE, (x, 0), (x, w))
        pygame.draw.line(surface, WHITE, (0, y), (w, y))


def redrawWindow(surface: pygame.display):
    global ROWS, WIDTH
    surface.fill(BLACK)
    drawGrid(WIDTH, ROWS, surface)
    pygame.display.update()


def randomSnack(rows, items):
    pass


def messageBox(subject, content):
    pass


def main():

    s = Snake(RED, (10, 10))
    run = True

    clock = pygame.time.Clock()
    while run:

        # time control
        pygame.time.delay(50)
        clock.tick(10)

        redrawWindow(WIN)


if __name__ == "__main__":
    main()
