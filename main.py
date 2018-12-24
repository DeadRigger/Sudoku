import time
import copy
import sys
import random as r
import pygame

# COLORS #

# Primary
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Others
LIGHT_BLUE = (135, 206, 250)
GRAY = (175, 175, 175)
YELLOW = (255, 255, 0)

# Shades
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TILE_WIDTH = 90
TILE_SIZE = (TILE_WIDTH, TILE_WIDTH)

BLOCK_WIDTH = 274
BLOCK_SIZE = (BLOCK_WIDTH, BLOCK_WIDTH)

# Init font for global use
pygame.font.init()
FONT = pygame.font.Font(None, 104)
BOLD_FONT = pygame.font.Font(None, 104)
BOLD_FONT.set_bold(True)


# Class make block 3x3
class Block:
    def __init__(self, pos):
        self.pos = pos
        self.rect = pygame.Rect(self.pos, BLOCK_SIZE)

        self.surface = pygame.Surface(BLOCK_SIZE).convert()
        self.surface.fill(BLACK)

        self.tiles = []


class Tile:

    def __init__(self, block, pos, number, is_hint=False):
        self.block = block
        self.pos = pos

        # Actual answer
        self.number = number

        # Current provided answer
        self.entered_number = ""

        # If this tile was given to the player at the start
        self.is_hint = is_hint

        # Calculate global rectangle pos
        block_x_pos = self.block.rect.x
        block_y_pos = self.block.rect.y
        rect_pos_x = block_x_pos + self.pos[0]
        rect_pos_y = block_y_pos + self.pos[1]
        rect_pos = (rect_pos_x,
                    rect_pos_y)

        self.rect = pygame.Rect(rect_pos, TILE_SIZE)

        self.surface = pygame.Surface(TILE_SIZE).convert()

        self.surface.fill(WHITE)

        if self.is_hint is True:
            self.draw_number(entry_text=self.number)
        else:
            self.draw_number()

    # This will draw self.entered_number unless entry_text is passed
    # Entry text is passed when a user selects this tile and types
    def draw_number(self, entry_text=None):

        # Render entry text if given, otherwise render the current entered number
        if entry_text is None:
            number_surface = FONT.render(str(self.entered_number), 1, BLACK)
        else:
            number_surface = FONT.render(str(entry_text), 1, BLACK)

        surface_center_x = self.surface.get_width() / 2
        surface_center_y = self.surface.get_height() / 2

        number_place_x = surface_center_x - number_surface.get_width() / 2
        number_place_y = surface_center_y - number_surface.get_height() / 2
        number_place = (number_place_x,
                        number_place_y)
        self.surface.blit(number_surface, number_place)

    def set_as_hint(self):
        self.entered_number = self.number
        self.draw_number(entry_text=self.number)
        self.is_hint = True


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
        self.field = [[None] * 9] * 9
        self.solution = [[None] * 9] * 9
        self.cycle_generate = r.randrange(10, 30)
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
        for i in range(9):
            for c in range(9):
                if r.randrange(0, 81) < 32:
                    self.field[i][c] = 0

    def solve(self):
        solution = copy.deepcopy(self.field)
        if Sudoku.solveHelper(solution):
            self.solution = solution
            return self.solution
        return None

    def solveHelper(solution):
        while True:
            minPossibleValueCountCell = None
            for rowIndex in range(9):
                for columnIndex in range(9):
                    if solution[rowIndex][columnIndex] != 0:
                        continue
                    possibleValues = Sudoku.findPossibleValues(rowIndex, columnIndex, solution)
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
            if Sudoku.solveHelper(solutionCopy):
                for r in range(9):
                    for c in range(9):
                        solution[r][c] = solutionCopy[r][c]
                return True
        return False

    def findPossibleValues(rowIndex, columnIndex, puzzle):
        values = {v for v in range(1, 10)}
        values -= Sudoku.getRowValues(rowIndex, puzzle)
        values -= Sudoku.getColumnValues(columnIndex, puzzle)
        values -= Sudoku.getBlockValues(rowIndex, columnIndex, puzzle)
        return values

    def getRowValues(rowIndex, puzzle):
        return set(puzzle[rowIndex][:])

    def getColumnValues(columnIndex, puzzle):
        return {puzzle[r][columnIndex] for r in range(9)}

    def getBlockValues(rowIndex, columnIndex, puzzle):
        blockRowStart = 3 * (rowIndex // 3)
        blockColumnStart = 3 * (columnIndex // 3)
        return {
            puzzle[blockRowStart + r][blockColumnStart + c]
            for r in range(3)
            for c in range(3)
        }


class Game:

    def __init__(self):
        # Boring pygame init stuff #
        pygame.init()
        self.clock = pygame.time.Clock()

        # Game Width
        self.GW = 843
        # Game Height
        self.GH = 843
        # Tuple of game size
        self.GS = (self.GW, self.GH)

        flags = pygame.DOUBLEBUF
        self.game_window = pygame.display.set_mode(self.GS, flags)

        game_surface_size = (self.GW, self.GH)
        self.game_surface = pygame.Surface(game_surface_size).convert()

        self.tile_spacer = 2
        self.block_spacer = 5

        self.blocks = []

        self.playing = True

        self.generate_field()
        for block in self.blocks:
            for tile in block.tiles:
                output(tile.number)
                output(' ')
            output('\n')
        self.main()

    def main(self):
        while self.playing:
            self.game_surface.fill(BLACK)
            for block in self.blocks:

                block.surface.fill(BLACK)
                # draw tiles to block surface
                for tile in block.tiles:
                    block.surface.blit(tile.surface, tile.pos)
                self.game_surface.blit(block.surface, block.pos)

            self.game_window.fill(BLACK)
            self.game_window.blit(self.game_surface, (0, 0))
            pygame.display.flip()

            self.clock.tick(60)

    def generate_field(self):
        S = Sudoku()
        puzzle = S.field

        x_pos = self.block_spacer
        y_pos = self.block_spacer
        for y in range(3):
            for x in range(3):
                newpos = (x_pos, y_pos)
                newblock = Block(newpos)

                tile_grid_x = 0
                tile_grid_y = 0
                for tile_y in range(3):
                    for tile_x in range(3):
                        newpos = (tile_grid_x, tile_grid_y)
                        number = puzzle[x * 3 + tile_x][y * 3 + tile_y]

                        newtile = Tile(block=newblock,
                                       pos=newpos,
                                       number=number)

                        newblock.tiles.append(newtile)

                        tile_grid_x += (TILE_WIDTH + self.tile_spacer)
                    tile_grid_y += (TILE_WIDTH + self.tile_spacer)
                    tile_grid_x = 0

                self.blocks.append(newblock)
                x_pos += (BLOCK_WIDTH + self.block_spacer)
            y_pos += (BLOCK_WIDTH + self.block_spacer)
            x_pos = self.block_spacer


def output(a):
    sys.stdout.write(str(a))


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


def check_correct(field):
    for row in range(9):
        for col in range(9):
            if field[row][col] == 0 or \
                    len(Sudoku.getRowValues(row, field)) != 9 or \
                    len(Sudoku.getColumnValues(col, field)) != 9 or \
                    len(Sudoku.getBlockValues(row, col, field)) != 9:
                return False

    return True


Game()
