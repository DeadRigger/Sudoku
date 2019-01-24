import copy
import random as r
from functions import *
from itertools import product
import pygame
import time


class Sudoku:
	"""docstring for Sudoku"""

	def __init__(self, screen, field, position, size_ceil, border, size=3):
		super(Sudoku, self).__init__()
		self.base_table = [
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
		self.screen = screen
		self.field = field
		self.start_point = position
		self.size_ceil = size_ceil
		self.min_size = size
		self.size = size ** 2
		self.border = border
		self.height = size_ceil * size
		self.width = size_ceil * size
		self.active_ceil = None
		self.table = [[None for i in range(self.size)] for j in range(self.size)]
		self.empty_ceils = []
		self.solution = []
		self.difficult = DIFFICULTY

		self.cycle_generate = 30
		self.generate()

	# Generate
	def generate(self):
		tm = time.time()

		self.table = copy.deepcopy(self.base_table)

		mix_func = ['self.swapBigRow()',
					'self.swapBigCol()',
					'self.swapSmallRow()',
					'self.swapSmallCol()']

		for i in range(1, self.cycle_generate):
			id_func = r.randrange(0, len(mix_func), 1)
			eval(mix_func[id_func])

		iteration = 0
		while True:
			iteration += 1
			grid = copy.deepcopy(self.table)
			self.empty_ceils = [[False for i in range(self.size)] for j in range(self.size)]
			tm_diff = time.time()
			diff = self.changeDifficult(grid)
			print('Change  difficult iteration ' + str(iteration) + ' ' + str(time.time()-tm_diff) + ' sec.')
			if DIFFICULTY_LIST[self.difficult][0] < diff <= DIFFICULTY_LIST[self.difficult][1]:
				self.table = grid
				print_field(self.table)
				print("Difficult {}, iterations {}".format(str(diff), str(iteration)))
				print('Generation time ' + str(time.time()-tm) + ' sec.')
				grid = copy.deepcopy(self.table)
				c = 0
				for i in self.solve_sudoku(grid):
					c += 1
				print('Decisions ' + str(c))
				return

	def swapBigRow(self):
		row1 = r.randrange(0, self.min_size)
		row2 = r.randrange(0, self.min_size)

		while row1 == row2:
			row2 = r.randrange(0, self.min_size)

		for i in range(self.min_size):
			self.table[row1 * self.min_size + i], self.table[row2 * self.min_size + i] = \
				self.table[row2 * self.min_size + i], self.table[row1 * self.min_size + i]

	def swapBigCol(self):
		col1 = r.randrange(0, self.min_size)
		col2 = r.randrange(0, self.min_size)

		while col1 == col2:
			col2 = r.randrange(0, self.min_size)

		for c in range(self.min_size):
			for i in range(self.size):
				self.table[i][col1 * self.min_size + c], self.table[i][col2 * self.min_size + c] = \
					self.table[i][col2 * self.min_size + c], self.table[i][col1 * self.min_size + c]

	def swapSmallRow(self):
		row = r.randrange(0, self.min_size)
		smallRow1 = r.randrange(0, self.min_size)
		smallRow2 = r.randrange(0, self.min_size)

		while smallRow1 == smallRow2:
			smallRow2 = r.randrange(0, self.min_size)

		self.table[row * self.min_size + smallRow1], self.table[row * self.min_size + smallRow2] = \
			self.table[row * self.min_size + smallRow2], self.table[row * self.min_size + smallRow1]

	def swapSmallCol(self):
		col = r.randrange(0, self.min_size)
		smallCol1 = r.randrange(0, self.min_size)
		smallCol2 = r.randrange(0, self.min_size)

		while smallCol1 == smallCol2:
			smallCol2 = r.randrange(0, self.min_size)

		for i in range(self.size):
			self.table[i][col * self.min_size + smallCol1], self.table[i][col * self.min_size + smallCol2] = \
				self.table[i][col * self.min_size + smallCol2], self.table[i][col * self.min_size + smallCol1]

	def changeDifficult(self, grid):
		count_ceils = SIZE ** 4
		count = 0
		remove_ceils = list()
		while True:
			count += 1
			row = r.randrange(0, self.size)
			col = r.randrange(0, self.size)
			while self.empty_ceils[row][col]:
				row = r.randrange(0, self.size)
				col = r.randrange(0, self.size)

			if count % 10 == 9:
				if not self.complicate(grid, row, col):
					for i in range(10):
						ceil = remove_ceils.pop()
						self.empty_ceils[ceil[0]][ceil[1]] = False
						grid[ceil[0]][ceil[1]] = ceil[2]
						if self.complicate(grid, ceil[0], ceil[1]):
							self.empty_ceils[ceil[0]][ceil[1]] = True
							grid[ceil[0]][ceil[1]] = None
							return count_ceils - len(remove_ceils) + 1

			remove_ceils.append((row, col, grid[row][col]))
			self.empty_ceils[row][col] = True
			grid[row][col] = None

	def complicate(self, grid, r, c):
		table = copy.deepcopy(grid)
		table[r][c] = None

		count = 0
		for i in self.solve_sudoku(table):
			count += 1
		if count == 1:
			return True

		return False

	# Display
	def activateCeil(self, ceil, number=None):
		if ceil is not None:
			self.active_ceil = ceil
			if number is not None:
				print(str(ceil) + ': ' + str(number))
				if self.table[ceil[0]][ceil[1]] == number:
					self.table[ceil[0]][ceil[1]] = None
				else:
					self.table[ceil[0]][ceil[1]] = number

			self.drawField(self.table)

	def drawField(self, field):
		pygame.draw.rect(self.screen, BACKGROUND_FIELD, self.field)  # draw field

		for row in range(self.min_size):
			for col in range(self.min_size):
				size_block = self.size_ceil * self.min_size
				start_point = (self.start_point[0] + col * size_block,
							   self.start_point[1] + row * size_block)
				self.drawBlock(start_point, row, col, size_block, field)

		if self.check_correct(field):
			font = {'name': FONT['name'], 'size': int(self.size_ceil * 9 / 4)}
			self.drawText('Winner', START_POINT, self.size_ceil * 9, font, color=GREEN)

	def drawBlock(self, start_point, block_row, block_col, size, field):
		self.drawCeil(start_point, size, self.border['block'])

		for row in range(self.min_size):
			for col in range(self.min_size):
				pos = (start_point[0] + col * self.size_ceil,
					   start_point[1] + row * self.size_ceil)
				ceil = [block_row * self.min_size + row, block_col * self.min_size + col]

				if self.active_ceil is not None:
					active_number = field[self.active_ceil[0]][self.active_ceil[1]]
					if self.active_ceil == ceil or \
							(active_number is not None and field[ceil[0]][ceil[1]] == active_number):
						self.drawCeil(pos, self.size_ceil, border=0)

				number = field[ceil[0]][ceil[1]]

				self.drawCeil(pos, self.size_ceil, self.border['ceil'])
				if number is not None:
					if self.empty_ceils[ceil[0]][ceil[1]]:
						grid = copy.deepcopy(field)
						grid[ceil[0]][ceil[1]] = None
						possibleValues = self.findPossibleValues(grid, ceil[0], ceil[1])
						if number in possibleValues:
							self.drawText(number, pos, self.size_ceil, FONT, color=COLOR_EDIT_NUM)
						else:
							self.drawText(number, pos, self.size_ceil, FONT, color=RED)
					else:
						self.drawText(number, pos, self.size_ceil, FONT)

	def drawCeil(self, start_point, size, border=1):
		if not border:
			pygame.draw.rect(self.screen, COLOR_ACTIVE_CEIL,
							 (start_point[0], start_point[1],
							  size, size))
		else:
			pygame.draw.rect(self.screen, self.border['color'],
							 (start_point[0], start_point[1],
							  size, size),
							 border)

	def drawText(self, text, start_point, size_ceil, font, color=BASE_COLOR_FONT):
		font = pygame.font.SysFont(font['name'], font['size'])
		number = font.render(str(text), True, color)
		pos_num_x = start_point[0] + (size_ceil - number.get_width()) / 2
		pos_num_y = start_point[1] + (size_ceil - number.get_height()) / 2
		self.screen.blit(number, (pos_num_x, pos_num_y))

	# Test
	def solve_sudoku(self, grid):
		""" An efficient Sudoku solver using Algorithm X."""
		R = self.min_size
		C = self.min_size
		N = R * C
		X = dict()
		for prod in product(range(N), range(1, N + 1)):
			X[("rc", (prod[0], prod[1]-1))] = set()
			X[("rn", prod)] = set()
			X[("cn", prod)] = set()
			X[("bn", prod)] = set()

		Y = dict()
		for r, c, n in product(range(N), range(N), range(1, N + 1)):
			b = (r // R) * R + (c // C)  # Box number
			Y[(r, c, n)] = [
				("rc", (r, c)),
				("rn", (r, n)),
				("cn", (c, n)),
				("bn", (b, n))]
			X[("rc", (r, c))].add((r, c, n))
			X[("rn", (r, n))].add((r, c, n))
			X[("cn", (c, n))].add((r, c, n))
			X[("bn", (b, n))].add((r, c, n))

		for i, row in enumerate(grid):
			for j, n in enumerate(row):
				if n:
					self.select(X, Y, (i, j, n))
		for solution in self.solve(X, Y, []):
			for (r, c, n) in solution:
				grid[r][c] = n
			yield grid

	def solve(self, X, Y, solution):
		if not X:
			yield list(solution)
		else:
			c = min(X, key=lambda c: len(X[c]))
			for r in list(X[c]):
				solution.append(r)
				cols = self.select(X, Y, r)
				for s in self.solve(X, Y, solution):
					yield s
				self.deselect(X, Y, r, cols)
				solution.pop()

	@staticmethod
	def select(X, Y, r):
		cols = []
		for j in Y[r]:
			for i in X[j]:
				for k in Y[i]:
					if k != j:
						X[k].remove(i)
			cols.append(X.pop(j))
		return cols

	@staticmethod
	def deselect(X, Y, r, cols):
		for j in reversed(Y[r]):
			X[j] = cols.pop()
			for i in X[j]:
				for k in Y[i]:
					if k != j:
						X[k].add(i)

	def findPossibleValues(self, puzzle, rowIndex, columnIndex):
		if puzzle[rowIndex][columnIndex] is None:
			values = {v for v in range(1, self.size + 1)}
			values -= self.getRowValues(puzzle, rowIndex)
			values -= self.getColumnValues(puzzle, columnIndex)
			values -= self.getBlockValues(puzzle, rowIndex, columnIndex)
			return values
		else:
			return

	def check_correct(self, field):
		for row in range(self.size):
			for col in range(self.size):
				if field[row][col] is None or \
						len(self.getRowValues(field, row)) != self.size or \
						len(self.getColumnValues(field, col)) != self.size or \
						len(self.getBlockValues(field, row, col)) != self.size:
					return False

		return True

	@staticmethod
	def getRowValues(puzzle, rowIndex):
		return set(puzzle[rowIndex][:])

	@staticmethod
	def getColumnValues(puzzle, columnIndex):
		return {puzzle[r][columnIndex] for r in range(len(puzzle))}

	@staticmethod
	def getBlockValues(puzzle, rowIndex, columnIndex):
		size = int(pow(len(puzzle), 0.5))
		blockRowStart = size * (rowIndex // size)
		blockColumnStart = size * (columnIndex // size)
		return {
			puzzle[blockRowStart + r][blockColumnStart + c]
			for r in range(size)
			for c in range(size)
		}
