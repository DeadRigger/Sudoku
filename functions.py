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
                if cell == 0 or isinstance(cell, set):
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


def text_button(screen, coords, text, size=FONT['size']):
    pygame.font.init()
    font = pygame.font.SysFont(FONT['name'], size)
    number = font.render(text, False, BLACK)
    screen.blit(number, coords)
