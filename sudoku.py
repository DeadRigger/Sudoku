import copy
import random as r
import sys

from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from constants import *
import time


class Cell(ToggleButton):
	coords = ListProperty()


class Grid(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.numbers = None
		self.active_ceil = None
		self.field = None
		self.possible_grid = None
		self.edit_cells = None
		self.sudoku_solution = False

	def generate(self, difficult):
		self.clear_widgets()

		size = self.cols ** 2
		size_block = self.cols
		self.active_ceil = None
		self.field = self.generate_field(size_block, DIFFICULTY_LIST[difficult])
		self.possible_grid = self.make_possible_grid(self.field)
		self.edit_cells = []
		for r in range(size):
			row = []
			for c in range(size):
				if not self.possible_grid[r][c]:
					row.append(False)
				else:
					row.append(True)
			self.edit_cells.append(row)

		for b in range(size):
			block = GridLayout(cols=3, spacing=2)
			for n in range(size):
				pos = (
					b // size_block * size_block + n // size_block,
					b % size_block * size_block + n % size_block
				)

				if self.field[pos[0]][pos[1]]:
					text = str(self.field[pos[0]][pos[1]])
				else:
					text = ""

				if self.edit_cells[pos[0]][pos[1]]:
					color = [0, 0, 1, 1]
				else:
					color = [0, 0, 0, 1]

				block.add_widget(Cell(
					coords=(pos[0], pos[1]),
					text=text,
					color=color,
					on_press=self.click
				))
			self.add_widget(block)

		# Virtual keyboard
		for i in range(size_block):
			self.add_widget(Widget(size_hint_y=0.3))

		for i in range(size_block):
			bl = BoxLayout(spacing=4, size_hint_y=0.3)
			for j in range(size_block):
				bl.add_widget(Button(
					text=str(i * size_block + j + 1),
					on_press=self.entry
				))
			self.add_widget(bl)

		if DISABLE_KEY_NUMBER: self.disabled_numbers()

	# Called when touch on a grid cell
	def click(self, instance):
		self.active_ceil = instance
		self.possible_grid = self.make_possible_grid(self.field)

		if IDENTICAL_NUMBER: self.identical_number()

		if HIGHLIGHT_POSSIBLE_VALUES and self.edit_cells[instance.coords[0]][instance.coords[1]]:
			self.highlighting()

	# Called when touch the virtual keyboard
	def entry(self, instance):
		if self.active_ceil is not None and \
				self.edit_cells[self.active_ceil.coords[0]][self.active_ceil.coords[1]]:
			r = self.active_ceil.coords[0]
			c = self.active_ceil.coords[1]
			if self.active_ceil.text == instance.text:
				self.active_ceil.text = ''
				self.field[r][c] = 0
			else:
				self.active_ceil.text = instance.text
				self.field[r][c] = int(instance.text)

			if self.active_ceil.text and int(self.active_ceil.text) not in self.possible_grid[r][c]:
				self.active_ceil.color = [1, 0, 0, 1]
			else:
				self.active_ceil.color = [0, 0, 1, 1]

			# Highlights the numbers that correspond to the active cell
			if IDENTICAL_NUMBER: self.identical_number()

			# Disables buttons on the keyboard that are not needed for filling
			if DISABLE_KEY_NUMBER: self.disabled_numbers()

			# Show popup that display you are winner
			if self.filled(self.field):
				self.sudoku_solution = True
				popup = ModalView(size_hint=(0.5, 0.5))
				popup.add_widget(Label(text="WINNER", color=[0, 1, 0, 1], font_size=36, bold=True))
				popup.open()

	def identical_number(self):
		if self.active_ceil.text:
			cells = ToggleButton.get_widgets('field')
			for cell in cells:
				if cell.text == self.active_ceil.text:
					cell.state = "down"
				else:
					cell.state = "normal"

	def disabled_numbers(self):
		self.count_numbers()
		for bl in self.children:
			if type(bl) == BoxLayout:
				for btn in bl.children:
					if self.numbers[int(btn.text) - 1] == self.cols ** 2:
						btn.disabled = True
					else:
						btn.disabled = False

	def count_numbers(self):
		self.numbers = [0 for i in range(9)]
		cells = ToggleButton.get_widgets('field')
		for cell in cells:
			if cell.text:
				self.numbers[int(cell.text) - 1] += 1

	def highlighting(self):
		try:
			for bl in self.children:
				if type(bl) == BoxLayout:
					for btn in bl.children:
						r = self.active_ceil.coords[0]
						c = self.active_ceil.coords[1]
						if int(btn.text) in self.possible_grid[r][c]:
							btn.state = 'down'
						else:
							btn.state = 'normal'
		except TypeError:
			pass

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
			return result
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
