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
		self.difficult = DIFFICULTY_LIST[DIFFICULTY]
		self.start_table = []
		self.table = []
		self.generate_field(size, self.difficult)

	# Generate
	@staticmethod
	def count_filled(grid):
		size = len(grid)
		count = 0
		for r in range(size):
			for c in range(size):
				if grid[r][c]:
					count += 1

		return count

	@staticmethod
	def print_grid(grid):
		fill = 0
		size = int(pow(len(grid), 0.5))
		for br in range(size):
			for r in range(size):
				for bc in range(size):
					for c in range(size):
						row, col = br * size + r, bc * size + c
						if grid[row][col]:
							fill += 1
							sys.stdout.write(str(grid[row][col]) + '\t')
						else:
							sys.stdout.write('.\t')
					if bc != size - 1:
						sys.stdout.write('|\t')
				sys.stdout.write('\n')
			if br != size - 1:
				for i in range(size ** 2 + 2):
					sys.stdout.write('-\t')
				sys.stdout.write('\n')
		sys.stdout.write('Filled ceil\'s ' + str(fill))
		sys.stdout.write('\n\n')

	@staticmethod
	def get_row_values(grid, row):
		return set(grid[row][:])

	@staticmethod
	def get_column_values(grid, column):
		return {grid[r][column] for r in range(len(grid))}

	@staticmethod
	def get_block_values(grid, row, column):
		size = int(pow(len(grid), 0.5))
		blockRowStart = size * (row // size)
		blockColumnStart = size * (column // size)
		return {
			grid[blockRowStart + r][blockColumnStart + c]
			for r in range(size)
			for c in range(size)
		}

	def find_possible_values(self, grid, row, column):
		if grid[row][column] == 0:
			values = {v for v in range(1, len(grid) + 1)}
			values -= self.get_row_values(grid, row)
			values -= self.get_column_values(grid, column)
			values -= self.get_block_values(grid, row, column)
			return values
		else:
			return

	def generate_field(self, size, difficult):
		tm = time.time()
		grid = self.generate_base_field(size)

		self.mix_field(grid)

		if self.filled(grid):
			result = self.erase_ceils(grid, difficult)
			self.print_grid(result)
			print('Generate field ' + str(time.time() - tm) + ' sec.\n')
			self.start_table = copy.deepcopy(result)
			self.table = result
		else:
			print("Поле судоку сгенерировано неправильно")
			exit(2)

	@staticmethod
	def generate_base_field(size):
		grid = [[0 for i in range(size ** 2)] for j in range(size ** 2)]
		numbers = [i + 1 for i in range(size ** 2)]
		for brow in range(size):
			for row in range(size):
				for bcol in range(size):
					for col in range(size):
						r, c = brow * size + row, bcol * size + col
						if not row and not brow:
							grid[r][c] = numbers.pop()
						else:
							grid[r][c] = grid[r - brow * size - row][(c - size * row - brow) % size ** 2]
		return grid

	def mix_field(self, grid):
		mix_func = ['self.swap_big_row(grid)',
					'self.swap_big_col(grid)',
					'self.swap_small_row(grid)',
					'self.swap_small_col(grid)']

		for i in range(1, 30):
			id_func = r.randrange(0, len(mix_func))
			eval(mix_func[id_func])

	@staticmethod
	def swap_big_row(grid):
		min_size = int(pow(len(grid), 0.5))

		row1 = r.randrange(0, min_size)
		row2 = r.randrange(0, min_size)

		while row1 == row2:
			row2 = r.randrange(0, min_size)

		for i in range(min_size):
			grid[row1 * min_size + i], grid[row2 * min_size + i] = \
				grid[row2 * min_size + i], grid[row1 * min_size + i]

	@staticmethod
	def swap_big_col(grid):
		size = len(grid)
		min_size = int(pow(size, 0.5))

		col1 = r.randrange(0, min_size)
		col2 = r.randrange(0, min_size)

		while col1 == col2:
			col2 = r.randrange(0, min_size)

		for c in range(min_size):
			for i in range(size):
				grid[i][col1 * min_size + c], grid[i][col2 * min_size + c] = \
					grid[i][col2 * min_size + c], grid[i][col1 * min_size + c]

	@staticmethod
	def swap_small_row(grid):
		min_size = int(pow(len(grid), 0.5))

		row = r.randrange(0, min_size)
		smallRow1 = r.randrange(0, min_size)
		smallRow2 = r.randrange(0, min_size)

		while smallRow1 == smallRow2:
			smallRow2 = r.randrange(0, min_size)

		grid[row * min_size + smallRow1], grid[row * min_size + smallRow2] = \
			grid[row * min_size + smallRow2], grid[row * min_size + smallRow1]

	@staticmethod
	def swap_small_col(grid):
		size = len(grid)
		min_size = int(pow(size, 0.5))

		col = r.randrange(0, min_size)
		smallCol1 = r.randrange(0, min_size)
		smallCol2 = r.randrange(0, min_size)

		while smallCol1 == smallCol2:
			smallCol2 = r.randrange(0, min_size)

		for i in range(size):
			grid[i][col * min_size + smallCol1], grid[i][col * min_size + smallCol2] = \
				grid[i][col * min_size + smallCol2], grid[i][col * min_size + smallCol1]

	def filled(self, grid):
		size = len(grid)
		for row in range(size):
			for col in range(size):
				if not grid[row][col] or \
						len(self.get_row_values(grid, row)) != size or \
						len(self.get_column_values(grid, col)) != size or \
						len(self.get_block_values(grid, row, col)) != size:
					return False

		return True

	def erase_ceils(self, grid, complication):
		size = len(grid)

		main_i = 0
		while True:
			main_i += 1
			grid_copy = copy.deepcopy(grid)
			for i in range(complication[1]):
				row = r.randrange(0, size)
				col = r.randrange(0, size)
				while not grid[row][col]:
					row = r.randrange(0, size)
					col = r.randrange(0, size)

				copy_copy = copy.deepcopy(grid_copy)
				if i > 3:
					copy_copy[row][col] = 0
					if self.solver(copy_copy):
						grid_copy[row][col] = 0
				else:
					grid_copy[row][col] = 0

				count = self.count_filled(grid_copy)
				if complication[0][0] <= count < complication[0][1]:
					print('Difficult is ' + str(count))
					print('Iterations:\n\t(main)' + str(main_i) + '\n\t(sub)' + str(i))
					return grid_copy

	def solver(self, grid):
		diff = 1
		count = self.count_filled(grid)
		while diff > 0:

			if self.one_choice(grid):
				return True

			if self.algorithm_with_block(grid):
				return True

			if self.algorithm_with_row(grid):
				return True

			if self.algorithm_with_column(grid):
				return True

			curr_count = self.count_filled(grid)
			diff = curr_count - count
			count = curr_count

		return False

	def make_possible_grid(self, grid, naked=True):
		size = len(grid)
		possible_grid = [[False for i in range(size)] for j in range(size)]

		# Массив со значение False, где не пустая ячейка и с возможными значениями, где пустая
		for row in range(size):
			for col in range(size):
				if not grid[row][col]:
					p_vals = self.find_possible_values(grid, row, col)
					possible_grid[row][col] = p_vals

		if naked:
			# Голая пара для строк
			self.naked_row(grid, size, possible_grid)

			# Голая пара для колонок
			self.naked_column(grid, size, possible_grid)

			# Голая пара для блоков
			self.naked_block(grid, int(size ** 0.5), possible_grid)

		return possible_grid

	def naked_row(self, grid, size, possible_grid):
		for r in range(size):
			values = {v for v in range(len(grid) + 1)}
			values -= self.get_row_values(grid, r)

			if 0 not in values:
				possible_val_row = []

				# Запись возможных значений в каждую ячейку строки
				for c in range(size):
					if not grid[r][c]:
						possible_val_row.append(((r, c), possible_grid[r][c]))

				self.naked_pairs(possible_val_row)

	def naked_column(self, grid, size, possible_grid):
		for c in range(size):
			values = {v for v in range(len(grid) + 1)}
			values -= self.get_column_values(grid, c)

			if 0 not in values:
				possible_val_col = []

				# Запись возможных значений в каждую ячейку строки
				for r in range(size):
					if not grid[r][c]:
						possible_val_col.append(((r, c), possible_grid[r][c]))

				self.naked_pairs(possible_val_col)

	def naked_block(self, grid, size, possible_grid):
		for br in range(size):
			for bc in range(size):
				values = {v for v in range(len(grid) + 1)}
				values -= self.get_block_values(grid, br * size, bc * size)

				if 0 not in values:
					possible_val_block = []

					# Запись возможных значений в каждую ячейку блока
					for r in range(size):
						for c in range(size):
							row, col = br * size + r, bc * size + c
							if not grid[row][col]:
								possible_val_block.append(((row, col), possible_grid[row][col]))

					self.naked_pairs(possible_val_block)

	@staticmethod
	def naked_pairs(possible_values):
		# Добавляем в массив ячейки, уоторые имеют 2 возможных значения
		pairs = []
		values = possible_values.copy()
		size = len(values)
		for i in range(size):
			val = values.pop()

			if len(val[1]) == 2:
				for possible_value in values:
					if val[1] == possible_value[1]:
						pairs.append(val[1])

		for pair in pairs:
			for possible_value in possible_values:
				if pair != possible_value[1]:
					vals = possible_value[1]
					vals -= pair

	def one_choice(self, grid):
		change = True
		while change:
			change = False
			possible_grid = self.make_possible_grid(grid)
			for r, row in enumerate(possible_grid):
				for c, val in enumerate(row):
					if val:
						if len(val) == 1:
							grid[r][c] = val.pop()
							change = True

		return self.filled(grid)

	@staticmethod
	def last_hero(grid, possible_values):
		# Просмотр для каждой пустой ячейке блока, есть ли значение которое существует в единственном экземпляре
		change = False
		for possible_value in possible_values:
			pos = possible_value[0]
			value = possible_value[1].copy()
			for val in possible_values:
				if val[0] != pos:
					value -= val[1]
				if not len(value):
					break
			if len(value) == 1:
				grid[pos[0]][pos[1]] = value.pop()
				change = True

		return change

	def algorithm_with_block(self, grid):
		size = int(pow(len(grid), 0.5))
		possible_grid = self.make_possible_grid(grid)

		# Перебор блоков на возможные значения в них
		for br in range(size):
			for bc in range(size):
				values = {v for v in range(len(grid) + 1)}
				values -= self.get_block_values(grid, br * size, bc * size)

				if 0 not in values:
					possible_val_block = []

					# Запись возможных значений в каждую ячейку блока
					for r in range(size):
						for c in range(size):
							row, col = br * size + r, bc * size + c
							if not grid[row][col]:
								possible_val_block.append(((row, col), possible_grid[row][col]))

					# Просмотр для каждой пустой ячейки, есть ли значение которое существует в единственном экземпляре
					if self.last_hero(grid, possible_val_block):
						self.one_choice(grid)

		return self.filled(grid)

	def algorithm_with_row(self, grid):
		size = len(grid)
		possible_grid = self.make_possible_grid(grid)

		# Перебор блоков на возможные значения в них
		for r in range(size):
			values = {v for v in range(len(grid) + 1)}
			values -= self.get_row_values(grid, r)

			if 0 not in values:
				possible_val_row = []

				# Запись возможных значений в каждую ячейку строки
				for c in range(size):
					if not grid[r][c]:
						possible_val_row.append(((r, c), possible_grid[r][c]))

				# Просмотр для каждой пустой ячейки, есть ли значение которое существует в единственном экземпляре
				if self.last_hero(grid, possible_val_row):
					possible_grid = self.make_possible_grid(grid)

		return self.filled(grid)

	def algorithm_with_column(self, grid):
		size = len(grid)
		possible_grid = self.make_possible_grid(grid)

		# Перебор блоков на возможные значения в них
		for c in range(size):
			values = {v for v in range(len(grid) + 1)}
			values -= self.get_column_values(grid, c)

			if 0 not in values:
				possible_val_col = []

				# Запись возможных значений в каждую ячейку строки
				for r in range(size):
					if not grid[r][c]:
						possible_val_col.append(((r, c), possible_grid[r][c]))

				# Просмотр для каждой пустой ячейки, есть ли значение которое существует в единственном экземпляре
				if self.last_hero(grid, possible_val_col):
					possible_grid = self.make_possible_grid(grid)

		return self.filled(grid)

	# Display
	def activateCeil(self, ceil, number=None):
		if ceil is not None:
			self.active_ceil = ceil
			if number and not self.start_table[ceil[0]][ceil[1]]:
				print(str(ceil) + ': ' + str(number))
				if self.table[ceil[0]][ceil[1]] == number:
					self.table[ceil[0]][ceil[1]] = 0
				else:
					self.table[ceil[0]][ceil[1]] = number

			return self.drawField(self.table)

	def drawField(self, field):
		pygame.draw.rect(self.screen, BACKGROUND_FIELD, self.field)  # draw field

		for row in range(self.min_size):
			for col in range(self.min_size):
				size_block = self.size_ceil * self.min_size
				start_point = (self.start_point[0] + col * size_block,
							   self.start_point[1] + row * size_block)
				self.drawBlock(start_point, row, col, size_block, field)

		if self.filled(field):
			font = {'name': FONT['name'], 'size': int(self.size_ceil * 9 / 4)}
			self.drawText('Winner', START_POINT, self.size_ceil * 9, font, color=GREEN)
			return True

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
							(active_number and field[ceil[0]][ceil[1]] == active_number):
						self.drawCeil(pos, self.size_ceil, border=0)

				number = field[ceil[0]][ceil[1]]

				self.drawCeil(pos, self.size_ceil, self.border['ceil'])
				if number:
					if not self.start_table[ceil[0]][ceil[1]]:
						grid = copy.deepcopy(field)
						grid[ceil[0]][ceil[1]] = 0
						possibleValues = self.find_possible_values(grid, ceil[0], ceil[1])
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
