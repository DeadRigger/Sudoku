import copy
import random as r
import sys
import pygame

# Constants and variable

# Colors
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
RED = (255, 0, 0)

# Game
START_POSX_FIELD = 12
START_POSY_FIELD = 112
CEIL_SIZE = 64
BLOCK_SIZE = CEIL_SIZE * 3
DIFFICULTY_LIST = {
    'easy': 70,
    'medium': 31,
    'hard': 22
}
font_name = 'Arial'
font_size = 30
difficulty = 'easy'

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


def text_button(screen, coords, text):
    pygame.font.init()
    font = pygame.font.SysFont(font_name, font_size)
    number = font.render(text, False, BLACK)
    screen.blit(number, coords)


class Sudoku:

    def __init__(self):
        self.complete = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 3, 4, 8, 9, 1, 5, 6, 7],
            [5, 6, 7, 2, 3, 4, 8, 9, 1],
            [8, 9, 1, 5, 6, 7, 2, 3, 4],
            [3, 4, 5, 9, 1, 2, 6, 7, 8],
            [6, 7, 8, 3, 4, 5, 9, 1, 2],
            [9, 1, 2, 6, 7, 8, 3, 4, 5]
        ]
        self.pos_x = START_POSX_FIELD
        self.pos_y = START_POSY_FIELD
        self.width = CEIL_SIZE * 9
        self.height = self.width
        self.count_unfilled_ceil = 0
        self.field = [[None for i in range(9)] for j in range(9)]
        self.bin_field = [[False for i in range(9)] for j in range(9)]
        self.solution = [[None for i in range(9)] for j in range(9)]
        self.cycle_generate = r.randrange(10, 30)
        self.hint_ceil = None
        self.generate()

    def generate(self):
        for i in range(self.cycle_generate):
            self.SwapBigRow()
            self.SwapBigColumn()
            for j in range(self.cycle_generate):
                self.SwapSmallRow()
                self.SwapSmallColumn()

        self.field = copy.deepcopy(self.complete)
        self.hideNumbers()

    def SwapBigRow(self):
        row1 = r.randrange(0, 3)
        row2 = r.randrange(0, 3)

        while row1 == row2:
            row2 = r.randrange(0, 3)

        for i in range(3):
            self.complete[row1 * 3 + i], self.complete[row2 * 3 + i] = \
                self.complete[row2 * 3 + i], self.complete[row1 * 3 + i]

    def SwapBigColumn(self):
        col1 = r.randrange(0, 3)
        col2 = r.randrange(0, 3)

        while col1 == col2:
            col2 = r.randrange(0, 3)

        for c in range(3):
            for i in range(9):
                self.complete[i][col1 * 3 + c], self.complete[i][col2 * 3 + c] = \
                    self.complete[i][col2 * 3 + c], self.complete[i][col1 * 3 + c]

    def SwapSmallRow(self):
        row = r.randrange(0, 3)
        smallRow1 = r.randrange(0, 3)
        smallRow2 = r.randrange(0, 3)

        while smallRow1 == smallRow2:
            smallRow2 = r.randrange(0, 3)

        self.complete[row * 3 + smallRow1], self.complete[row * 3 + smallRow2] = \
            self.complete[row * 3 + smallRow2], self.complete[row * 3 + smallRow1]

    def SwapSmallColumn(self):
        col = r.randrange(0, 3)
        smallCol1 = r.randrange(0, 3)
        smallCol2 = r.randrange(0, 3)

        while smallCol1 == smallCol2:
            smallCol2 = r.randrange(0, 3)

        for i in range(9):
            self.complete[i][col * 3 + smallCol1], self.complete[i][col * 3 + smallCol2] = \
                self.complete[i][col * 3 + smallCol2], self.complete[i][col * 3 + smallCol1]

    def hideNumbers(self):
        for row in range(9):
            for col in range(9):
                if r.randrange(0, 81) > DIFFICULTY_LIST[difficulty]:
                    self.field[row][col] = 0
                    self.bin_field[row][col] = True
                    self.count_unfilled_ceil += 1

    def solve(self):
        solution = copy.deepcopy(self.field)
        if self.solveHelper(solution):
            self.solution = solution
            return self.solution
        return None

    def solveHelper(self, solution):
        while True:
            minPossibleValueCountCell = None
            for rowIndex in range(9):
                for columnIndex in range(9):
                    if solution[rowIndex][columnIndex] != 0:
                        continue
                    possibleValues = self.findPossibleValues(rowIndex, columnIndex, solution)
                    possibleValueCount = len(possibleValues)
                    if possibleValueCount == 0:
                        return False
                    if possibleValueCount == 1:
                        solution[rowIndex][columnIndex] = possibleValues.pop()
                    if not minPossibleValueCountCell or \
                            possibleValueCount < len(minPossibleValueCountCell[1]):
                        minPossibleValueCountCell = ((rowIndex, columnIndex), possibleValues)
            if not minPossibleValueCountCell:
                return True
            elif 1 < len(minPossibleValueCountCell[1]):
                break
        r, c = minPossibleValueCountCell[0]
        for v in minPossibleValueCountCell[1]:
            solutionCopy = copy.deepcopy(solution)
            solutionCopy[r][c] = v
            if self.solveHelper(solutionCopy):
                for r in range(9):
                    for c in range(9):
                        solution[r][c] = solutionCopy[r][c]
                return True
        return False

    # display sudoku field
    def show(self, screen, pos_click=None):
        # check for click
        if pos_click is not None:
            ceil_x = int((pos_click[1] - START_POSY_FIELD) / CEIL_SIZE)
            ceil_y = int((pos_click[0] - START_POSX_FIELD) / CEIL_SIZE)

            if 0 <= ceil_x < 9 and 0 <= ceil_y < 9 and self.bin_field[ceil_x][ceil_y]:
                if self.hint_ceil is not None:
                    self.drawCeil(screen, self.hint_ceil[0], self.hint_ceil[1], CEIL_SIZE, WHITE)
                self.hint_ceil = (ceil_x, ceil_y)
                self.drawCeil(screen, ceil_x, ceil_y, CEIL_SIZE, LIGHT_BLUE)
        # check for hint ceil
        elif self.hint_ceil is not None:
            # draw a blue ceil
            self.drawCeil(screen, self.hint_ceil[0], self.hint_ceil[1], CEIL_SIZE, LIGHT_BLUE)

        for brow in range(3):
            for bcol in range(3):
                # draw block 3x3
                self.drawCeil(screen, brow, bcol, BLOCK_SIZE, BLACK, 2)
                for srow in range(3):
                    for scol in range(3):
                        ceil_x = brow * 3 + srow
                        ceil_y = bcol * 3 + scol
                        value = self.field[ceil_x][ceil_y]
                        pos_ceil = self.drawCeil(screen, ceil_x, ceil_y, CEIL_SIZE, BLACK, 1)

                        pygame.font.init()
                        font = pygame.font.SysFont(font_name, font_size)
                        if value == 0:
                            number = font.render('', True, BLACK)
                        else:
                            # check for value editable
                            if self.bin_field[ceil_x][ceil_y]:
                                copy_field = copy.deepcopy(self.field)
                                copy_field[ceil_x][ceil_y] = 0

                                # checking for correct value
                                if value in self.findPossibleValues(ceil_x, ceil_y, copy_field):
                                    # a blue digit
                                    number = font.render(str(value), True, BLUE)
                                else:
                                    # a red digit
                                    number = font.render(str(value), True, RED)
                                copy_field.clear()
                            else:
                                # a black digit
                                number = font.render(str(value), True, BLACK)
                        screen.blit(number, (pos_ceil[0] + 25, pos_ceil[1] + 10))

        if self.count_unfilled_ceil == 0 and self.check_correct(self.field):
            win = pygame.Surface((self.width, self.height))
            win.set_alpha(100)
            win.fill(WHITE)
            text_button(win, (250, 250), 'WINNER')
            screen.blit(win, (START_POSX_FIELD, START_POSY_FIELD))

        # Display update
        pygame.display.update()

    # change value in ceil
    def changeNumber(self, screen, coord, num):
        if self.field[coord[0]][coord[1]] is not num:
            self.field[coord[0]][coord[1]] = num
            self.count_unfilled_ceil -= 1
        else:
            self.field[coord[0]][coord[1]] = 0
            self.count_unfilled_ceil += 1

        self.show(screen)

    @staticmethod
    def drawCeil(screen, row, col, size, color_rect=BLACK, border_width=None):
        POSX_CEIL = START_POSX_FIELD + size * col
        POSY_CEIL = START_POSY_FIELD + size * row
        if border_width is None:
            pygame.draw.rect(screen, color_rect,
                             (POSX_CEIL, POSY_CEIL,
                              size, size))
        else:
            pygame.draw.rect(screen, color_rect,
                             (POSX_CEIL, POSY_CEIL,
                              size, size),
                             border_width)

        return POSX_CEIL, POSY_CEIL

    # find the missing value
    @staticmethod
    def findPossibleValues(rowIndex, columnIndex, puzzle):
        values = {v for v in range(1, 10)}
        values -= Sudoku.getRowValues(rowIndex, puzzle)
        values -= Sudoku.getColumnValues(columnIndex, puzzle)
        values -= Sudoku.getBlockValues(rowIndex, columnIndex, puzzle)
        return values

    @staticmethod
    def getRowValues(rowIndex, puzzle):
        return set(puzzle[rowIndex][:])

    @staticmethod
    def getColumnValues(columnIndex, puzzle):
        return {puzzle[r][columnIndex] for r in range(9)}

    @staticmethod
    def getBlockValues(rowIndex, columnIndex, puzzle):
        blockRowStart = 3 * (rowIndex // 3)
        blockColumnStart = 3 * (columnIndex // 3)
        return {
            puzzle[blockRowStart + r][blockColumnStart + c]
            for r in range(3)
            for c in range(3)
        }

    @staticmethod
    def check_correct(field):
        for row in range(9):
            for col in range(9):
                if field[row][col] == 0 or \
                        len(Sudoku.getRowValues(row, field)) != 9 or \
                        len(Sudoku.getColumnValues(col, field)) != 9 or \
                        len(Sudoku.getBlockValues(row, col, field)) != 9:
                    return False

        return True
