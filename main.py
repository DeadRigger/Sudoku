from sudoku import Sudoku
from pygame.locals import *
from functions import *


# Initialization objects pygame
pygame.init()
clock = pygame.time.Clock()
size = [WIDTH, HEIGHT]

# Установка размера ячейки в зависимости от ширины экрана
size_ceil = int((WIDTH - START_POINT[0] * 2) / 9)
font_size = size_ceil

screen = pygame.display.set_mode(size)

size_field = size_ceil * 9
field = pygame.Rect(START_POINT[0], START_POINT[1],
                    size_field, size_field)
border = {
    'block': 2,
    'ceil': 1,
    'color': BLACK
}

s = Sudoku(screen, field, START_POINT, size_ceil, border, size=SIZE)

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(1)

        elif event.type == KEYDOWN:
            pass

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button

            if field.collidepoint(mouse_pos):
                # prints current location of mouse
                ceil = {
                    'row': int((mouse_pos[1] - START_POINT[1]) / size_ceil),
                    'col': int((mouse_pos[0] - START_POINT[0]) / size_ceil)
                }

                s.activateCeil(ceil)
                pygame.display.update()

    clock.tick(FPS)
