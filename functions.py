import sys
import pygame
from constants import *


def output(a):
    sys.stdout.write(str(a))


# we derive the Sudoku field in a readable form
def print_field(*args):
    if not args:
        output("No solution")
        return

    for i in range(9):
        for f in args:
            for j in range(9):
                cell = f[i][j]
                if cell is None or isinstance(cell, set):
                    output('.')
                else:
                    output(cell)
                if (j + 1) % 3 == 0 and j < 8:
                    output(' |')

                output(' ')
            output('  ')
        output('\n')

        if (i + 1) % 3 == 0 and i < 8:
            for f in args:
                output("- - - + - - - + - - -   ")
            output('\n')


def drawCenterText(screen, text, rect, font=FONT, color=BASE_COLOR_FONT):
    font = pygame.font.SysFont(font['name'], font['size'])
    number = font.render(str(text), True, color)
    pos_num_x = rect[0] + (rect[2] - number.get_width()) / 2
    pos_num_y = rect[1] + (rect[3] - number.get_height()) / 2
    screen.blit(number, (pos_num_x, pos_num_y))
