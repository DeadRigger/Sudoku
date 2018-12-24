import pygame
from pygame.locals import *

from sudoku import Sudoku


# Constants and variable

# Colors
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)

# Event
POS_DOWN = (0, 0)
POS_UP = (0, 0)

# Game
START_POSX_FIELD = 12
START_POSY_FIELD = 12
CEIL_SIZE = 64
BLOCK_SIZE = CEIL_SIZE * 3
FPS = 1
display_width = 600
display_height = 600
name_app = 'Sudoku'
count = 1

# Initialization objects pygame
pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption(name_app)
clock = pygame.time.Clock()
s = Sudoku()

game_display.fill(WHITE)


# Functions
def event_handler():
    for event in pygame.event.get():
        if event.type == QUIT or (
                event.type == KEYDOWN and (
                event.key == K_ESCAPE or
                event.key == K_q
        )):
            pygame.quit()
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            POS_DOWN = event.pos
        elif event.type == MOUSEBUTTONUP:
            if event.pos == POS_DOWN:
                print(event.pos)


for brow in range(3):
    for bcol in range(3):
        POSX_BLOCK = START_POSX_FIELD + BLOCK_SIZE * bcol
        POSY_BLOCK = START_POSX_FIELD + BLOCK_SIZE * brow
        pygame.draw.rect(game_display, BLACK,
                         (POSX_BLOCK,
                          POSY_BLOCK,
                          BLOCK_SIZE, BLOCK_SIZE), 2)
        for srow in range(3):
            for scol in range(3):
                POSX_CEIL = POSX_BLOCK + CEIL_SIZE * scol
                POSY_CEIL = POSY_BLOCK + CEIL_SIZE * srow
                value = s.field[brow*3 + srow][bcol*3 + scol]

                pygame.draw.rect(game_display, BLACK,
                                 (POSX_CEIL, POSY_CEIL,
                                  CEIL_SIZE, CEIL_SIZE), 1)
                pygame.font.init()
                font = pygame.font.SysFont('Comic Sans MS', 30)
                if value == 0:
                    number = font.render('', False, BLACK)
                else:
                    number = font.render(str(value), False, BLACK)
                game_display.blit(number, (POSX_CEIL + 25, POSY_CEIL + 10))

# Display update
pygame.display.update()

# Main loop
while True:
    # Delay
    clock.tick(FPS)

    # Event handler
    event_handler()
