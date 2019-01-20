import copy
import random as r
from constants import *
from itertools import product
import pygame


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
		self.empty_ceils = [[False for i in range(self.size)] for j in range(self.size)]
		self.solution = []
		self.difficult = 30

		self.cycle_generate = 30
		self.generate()
		self.drawField(self.table)

	# Generate
	def generate(self):
		self.table = copy.deepcopy(self.base_table)

		mix_func = ['self.swapBigRow',
					'self.swapBigColumn',
					'self.swapSmallRow',
					'self.swapSmallColumn']

		for i in range(1, self.cycle_generate):
			id_func = r.randrange(0, len(mix_func), 1)
			eval(mix_func[id_func])

		self.changeDifficult()

	def swapBigRow(self):
		row1 = r.randrange(0, self.min_size)
		row2 = r.randrange(0, self.min_size)

		while row1 == row2:
			row2 = r.randrange(0, self.min_size)

		for i in range(self.min_size):
			self.table[row1 * self.min_size + i], self.table[row2 * self.min_size + i] = \
				self.table[row2 * self.min_size + i], self.table[row1 * self.min_size + i]

	def swapBigColumn(self):
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

	def swapSmallColumn(self):
		col = r.randrange(0, self.min_size)
		smallCol1 = r.randrange(0, self.min_size)
		smallCol2 = r.randrange(0, self.min_size)

		while smallCol1 == smallCol2:
			smallCol2 = r.randrange(0, self.min_size)

		for i in range(self.size):
			self.table[i][col * self.min_size + smallCol1], self.table[i][col * self.min_size + smallCol2] = \
				self.table[i][col * self.min_size + smallCol2], self.table[i][col * self.min_size + smallCol1]

	def changeDifficult(self):
		for i in range(self.size ** 2 - self.difficult):
			row = r.randrange(0, self.size)
			col = r.randrange(0, self.size)
			while self.empty_ceils[row][col] and self.complicate(row, col):
				row = r.randrange(0, self.size)
				col = r.randrange(0, self.size)

			self.empty_ceils[row][col] = True
			self.table[row][col] = None

	def complicate(self, r, c):
		grid = copy.deepcopy(self.table)
		grid[r][c] = None

		count = 0
		for i in self.solve_sudoku(grid):
			count += 1
		if count == 1:
			return True

		return False

	# Display
	def activateCeil(self, ceil):
		if self.empty_ceils[ceil['row']][ceil['col']]:
			self.active_ceil = [ceil['row'], ceil['col']]
			self.drawField(self.table)

			print(self.findPossibleValues(self.table, ceil['row'], ceil['col']))

	def drawField(self, field):
		self.screen.fill(BACKGROUND)
		pygame.font.init()
		pygame.draw.rect(self.screen, [200, 200, 200], self.field)  # draw field

		for row in range(self.min_size):
			for col in range(self.min_size):
				size_block = self.size_ceil * self.min_size
				start_point = (self.start_point[0] + col * size_block,
							   self.start_point[1] + row * size_block)
				self.drawBlock(start_point, row, col, size_block, field)

	def drawBlock(self, start_point, block_row, block_col, size, field):
		self.drawCeil(start_point, size, self.border['block'])

		for row in range(self.min_size):
			for col in range(self.min_size):
				pos = (start_point[0] + col * self.size_ceil,
					   start_point[1] + row * self.size_ceil)
				ceil = [block_row * self.min_size + row, block_col * self.min_size + col]

				if self.active_ceil == ceil:
					self.drawCeil(pos, self.size_ceil, border=0)

				number = field[ceil[0]][ceil[1]]

				self.drawCeil(pos, self.size_ceil, self.border['ceil'])
				if number is not None:
					self.drawNumber(number, pos, self.size_ceil)

	def drawCeil(self, start_point, size, border=1):
		if not border:
			pygame.draw.rect(self.screen, BLUE,
							 (start_point[0], start_point[1],
							  size, size))
		else:
			pygame.draw.rect(self.screen, self.border['color'],
							 (start_point[0], start_point[1],
							  size, size),
							 border)

	def drawNumber(self, text, start_point, size):
		font = pygame.font.SysFont(FONT['name'], FONT['size'])
		number = font.render(str(text), True, BLACK)
		pos_num_x = start_point[0] + (size - number.get_width()) / 2
		pos_num_y = start_point[1] + (size - number.get_height()) / 2
		self.screen.blit(number, (pos_num_x, pos_num_y))

	# Test
	def solve_sudoku(self, grid):
		""" An efficient Sudoku solver using Algorithm X."""
		R = self.min_size
		C = self.min_size
		N = R * C
		X = ([("rc", rc) for rc in product(range(N), range(N))] +
			 [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
			 [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
			 [("bn", bn) for bn in product(range(N), range(1, N + 1))])
		Y = dict()
		for r, c, n in product(range(N), range(N), range(1, N + 1)):
			b = (r // R) * R + (c // C)  # Box number
			Y[(r, c, n)] = [
				("rc", (r, c)),
				("rn", (r, n)),
				("cn", (c, n)),
				("bn", (b, n))]
		X, Y = self.exact_cover(X, Y)
		for i, row in enumerate(grid):
			for j, n in enumerate(row):
				if n:
					self.select(X, Y, (i, j, n))
		for solution in self.solve(X, Y, []):
			for (r, c, n) in solution:
				grid[r][c] = n
			yield grid

	@staticmethod
	def exact_cover(X, Y):
		X = {j: set() for j in X}
		for i, row in Y.items():
			for j in row:
				X[j].add(i)
		return X, Y

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
		values = {v for v in range(1, self.size + 1)}
		values -= self.getRowValues(puzzle, rowIndex)
		values -= self.getColumnValues(puzzle, columnIndex)
		values -= self.getBlockValues(puzzle, rowIndex, columnIndex)
		return values

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
