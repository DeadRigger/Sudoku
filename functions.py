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


class Button:
    def __init__(self, screen, rect, text=None, bg=WHITE, border=BLACK, text_color=BLACK,
                 font={'name': 'Comic San', 'size': 25}):
        self.screen = screen
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.rect = rect
        self.text = text
        self.background = bg
        self.border = border
        self.color = text_color
        self.font = font

    def draw(self):
        font = pygame.font.SysFont(self.font['name'], self.font['size'])
        text = font.render(str(self.text), True, self.color)

        pygame.draw.rect(self.screen, self.background, self.rect)
        pygame.draw.rect(self.screen, self.border, self.rect, 1)

        pos_x = self.x + (self.width - text.get_width()) / 2
        pos_y = self.y + (self.height - text.get_height()) / 2
        self.screen.blit(text, (pos_x, pos_y))
