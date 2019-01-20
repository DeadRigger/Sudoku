from sudoku import Sudoku
from pygame.locals import *
from functions import *


# Initialization objects pygame
pygame.init()
clock = pygame.time.Clock()
size = [WIDTH, HEIGHT]

# Установка размера ячейки в зависимости от ширины экрана
size_ceil = int((WIDTH - START_POINT[0] * 2) / 9)

# Размер текста соответствует размеру ячейки
font_size = size_ceil

screen = pygame.display.set_mode(size)
pygame.display.set_caption(NAME_APP)

size_field = size_ceil * 9

# Меню, в котором можно выбрать сложность уровня и начать его
panel = pygame.Rect(START_POINT[0], 0, WIDTH - START_POINT[0], START_POINT[1])

# Rect, на котором будет располагаться сетка судоку
grid = pygame.Rect(START_POINT[0], START_POINT[1], size_field, size_field)

# Клавиатура при нажатии, на которую активная ячейка будет заполнена тем числом, на которое нажали
pos_x = START_POINT[0]
pos_y = START_POINT[1] + size_field
keyboard = pygame.Rect(pos_x, pos_y, WIDTH - pos_x, HEIGHT - pos_y)

border = {
    'block': 2,
    'ceil': 1,
    'color': BASE_COLOR
}

s = Sudoku(screen, grid, START_POINT, size_ceil, border, size=SIZE)

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(1)

        elif event.type == KEYDOWN:
            if 0 < event.key - 48 < 10:
                number = event.key - 48
                s.activateCeil(s.active_ceil, number)
                pygame.display.update()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button

            if grid.collidepoint(mouse_pos) and event.button == 1:
                # prints current location of mouse
                ceil = [int((mouse_pos[1] - START_POINT[1]) / size_ceil),
                        int((mouse_pos[0] - START_POINT[0]) / size_ceil)]

                s.activateCeil(ceil)
                pygame.display.update()
            elif keyboard.collidepoint(mouse_pos) and event.button == 1:
                print('Keyboard click')
            elif panel.collidepoint(mouse_pos) and event.button == 1:
                print('Panel click')

    clock.tick(FPS)
