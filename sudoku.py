import copy
import random as r
import sys


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

    @staticmethod
    def findPossibleValues(rowIndex, columnIndex, puzzle):
        values = {v for v in range(1, 10)}
        values -= Sudoku.getRowValues(puzzle)
        values -= Sudoku.getColumnValues(puzzle)
        values -= Sudoku.getBlockValues(columnIndex, puzzle)
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


s = Sudoku()
print_field(s.field)
