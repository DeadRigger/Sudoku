import random as r
import sys
import copy
import time

TEST = False


def count_filled(grid):
	size = len(grid)
	count = 0
	for r in range(size):
		for c in range(size):
			if grid[r][c]:
				count += 1

	# print('Filled ceil\'s ' + str(count) + '\n')
	return count


def print_grid(grid):
	if not isinstance(grid, list):
		return
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


def get_row_values(grid, row):
	return set(grid[row][:])


def get_column_values(grid, column):
	return {grid[r][column] for r in range(len(grid))}


def get_block_values(grid, row, column):
	size = int(pow(len(grid), 0.5))
	blockRowStart = size * (row // size)
	blockColumnStart = size * (column // size)
	return {
		grid[blockRowStart + r][blockColumnStart + c]
		for r in range(size)
		for c in range(size)
	}


def find_possible_values(grid, row, column):
	if grid[row][column] == 0:
		values = {v for v in range(1, len(grid) + 1)}
		values -= get_row_values(grid, row)
		values -= get_column_values(grid, column)
		values -= get_block_values(grid, row, column)
		return values
	else:
		return


def generate_field(size, difficult):
	grid = generate_base_field(size)

	mix_field(grid)

	if filled(grid):
		return erase_ceils(grid, difficult)
	print("Поле судоку сгенерировано неправильно")
	exit(2)


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


def mix_field(grid):
	mix_func = ['swap_big_row(grid)',
				'swap_big_col(grid)',
				'swap_small_row(grid)',
				'swap_small_col(grid)']

	for i in range(1, 30):
		id_func = r.randrange(0, len(mix_func))
		eval(mix_func[id_func])


def swap_big_row(grid):
	min_size = int(pow(len(grid), 0.5))

	row1 = r.randrange(0, min_size)
	row2 = r.randrange(0, min_size)

	while row1 == row2:
		row2 = r.randrange(0, min_size)

	for i in range(min_size):
		grid[row1 * min_size + i], grid[row2 * min_size + i] = \
			grid[row2 * min_size + i], grid[row1 * min_size + i]


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


def swap_small_row(grid):
	min_size = int(pow(len(grid), 0.5))

	row = r.randrange(0, min_size)
	smallRow1 = r.randrange(0, min_size)
	smallRow2 = r.randrange(0, min_size)

	while smallRow1 == smallRow2:
		smallRow2 = r.randrange(0, min_size)

	grid[row * min_size + smallRow1], grid[row * min_size + smallRow2] = \
		grid[row * min_size + smallRow2], grid[row * min_size + smallRow1]


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


def filled(grid):
	size = len(grid)
	for row in range(size):
		for col in range(size):
			if not grid[row][col] or \
					len(get_row_values(grid, row)) != size or \
					len(get_column_values(grid, col)) != size or \
					len(get_block_values(grid, row, col)) != size:
				return False

	return True


def erase_ceils(grid, complication):
	size = len(grid)

	main_i = 0
	if TEST:
		iter_erase = (50, 200)
		iter_test = 10
		for e in range(iter_erase[0], iter_erase[1]):
			missing_steps = []
			for t in range(iter_test):
				main_i += 1
				grid_copy = copy.deepcopy(grid)
				for i in range(e):
					row = r.randrange(0, size)
					col = r.randrange(0, size)
					while not grid[row][col]:
						row = r.randrange(0, size)
						col = r.randrange(0, size)

					copy_copy = copy.deepcopy(grid_copy)
					if i > 3:
						copy_copy[row][col] = 0
						if solver(copy_copy):
							grid_copy[row][col] = 0
					else:
						grid_copy[row][col] = 0

				count = count_filled(grid_copy)

				# Test block for analyzing
				missing_steps.append(count)

			avg_filled = 0
			for c in missing_steps:
				avg_filled += c
			print('Test iteration with ' + str(e) + ' erases: average result ' + str(avg_filled / 10))
	else:
		while True:
			difficult = r.randrange(complication[0][0], complication[0][1])
			main_i += 1
			grid_copy = copy.deepcopy(grid)
			for i in range(complication[1]):
				row = r.randrange(0, size)
				col = r.randrange(0, size)
				while not grid[row][col]:
					row = r.randrange(0, size)
					col = r.randrange(0, size)

				copy_copy = copy.deepcopy(grid_copy)
				copy_copy[row][col] = 0
				if solver(copy_copy):
					grid_copy[row][col] = 0

				count = count_filled(grid_copy)
				if count == difficult:
					print('Difficult is ' + str(count))
					print('Iterations:\n\t(main)' + str(main_i) + '\n\t(sub)' + str(i))
					return grid_copy


def solver(grid):
	diff = 1
	count = count_filled(grid)
	while diff > 0:

		if one_choice(grid):
			return True

		if algorithm_with_block(grid):
			return True

		if algorithm_with_row(grid):
			return True

		if algorithm_with_column(grid):
			return True

		curr_count = count_filled(grid)
		diff = curr_count - count
		count = curr_count

	# for r in range(len(grid)):
	# 	for c in range(len(grid)):
	# 		if not grid[r][c]:
	# 			for val in find_possible_values(grid, r, c):
	# 				grid_copy = copy.deepcopy(grid)
	# 				grid_copy[r][c] = val
	# 				if solver(grid_copy):
	# 					grid = grid_copy
	# 					return True
	return False


def make_possible_grid(grid, naked=True):
	size = len(grid)
	possible_grid = [[False for i in range(size)] for j in range(size)]

	# Массив со значение False, где не пустая ячейка и с возможными значениями, где пустая
	for row in range(size):
		for col in range(size):
			if not grid[row][col]:
				p_vals = find_possible_values(grid, row, col)
				possible_grid[row][col] = p_vals

	if naked:
		# Голая пара для строк
		naked_row(grid, size, possible_grid)

		# Голая пара для колонок
		naked_column(grid, size, possible_grid)

		# Голая пара для блоков
		naked_block(grid, int(size ** 0.5), possible_grid)

	return possible_grid


def naked_row(grid, size, possible_grid):
	for r in range(size):
		values = {v for v in range(len(grid) + 1)}
		values -= get_row_values(grid, r)

		if 0 not in values:
			possible_val_row = []

			# Запись возможных значений в каждую ячейку строки
			for c in range(size):
				if not grid[r][c]:
					possible_val_row.append(((r, c), possible_grid[r][c]))

			naked_pairs(possible_val_row)


def naked_column(grid, size, possible_grid):
	for c in range(size):
		values = {v for v in range(len(grid) + 1)}
		values -= get_column_values(grid, c)

		if 0 not in values:
			possible_val_col = []

			# Запись возможных значений в каждую ячейку строки
			for r in range(size):
				if not grid[r][c]:
					possible_val_col.append(((r, c), possible_grid[r][c]))

			naked_pairs(possible_val_col)


def naked_block(grid, size, possible_grid):
	for br in range(size):
		for bc in range(size):
			values = {v for v in range(len(grid) + 1)}
			values -= get_block_values(grid, br * size, bc * size)

			if 0 not in values:
				possible_val_block = []

				# Запись возможных значений в каждую ячейку блока
				for r in range(size):
					for c in range(size):
						row, col = br * size + r, bc * size + c
						if not grid[row][col]:
							possible_val_block.append(((row, col), possible_grid[row][col]))

				naked_pairs(possible_val_block)


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


def one_choice(grid):
	change = True
	while change:
		change = False
		possible_grid = make_possible_grid(grid)
		for r, row in enumerate(possible_grid):
			for c, val in enumerate(row):
				if val:
					if len(val) == 1:
						grid[r][c] = val.pop()
						change = True

	return filled(grid)


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


def algorithm_with_block(grid):
	size = int(pow(len(grid), 0.5))
	possible_grid = make_possible_grid(grid)

	# Перебор блоков на возможные значения в них
	for br in range(size):
		for bc in range(size):
			values = {v for v in range(len(grid) + 1)}
			values -= get_block_values(grid, br * size, bc * size)

			if 0 not in values:
				possible_val_block = []

				# Запись возможных значений в каждую ячейку блока
				for r in range(size):
					for c in range(size):
						row, col = br * size + r, bc * size + c
						if not grid[row][col]:
							possible_val_block.append(((row, col), possible_grid[row][col]))

				# Просмотр для каждой пустой ячейки, есть ли значение которое существует в единственном экземпляре
				if last_hero(grid, possible_val_block):
					one_choice(grid)

	return filled(grid)


def algorithm_with_row(grid):
	size = len(grid)
	possible_grid = make_possible_grid(grid)

	# Перебор блоков на возможные значения в них
	for r in range(size):
		values = {v for v in range(len(grid) + 1)}
		values -= get_row_values(grid, r)

		if 0 not in values:
			possible_val_row = []

			# Запись возможных значений в каждую ячейку строки
			for c in range(size):
				if not grid[r][c]:
					possible_val_row.append(((r, c), possible_grid[r][c]))

			# Просмотр для каждой пустой ячейки, есть ли значение которое существует в единственном экземпляре
			if last_hero(grid, possible_val_row):
					possible_grid = make_possible_grid(grid)

	return filled(grid)


def algorithm_with_column(grid):
	size = len(grid)
	possible_grid = make_possible_grid(grid)

	# Перебор блоков на возможные значения в них
	for c in range(size):
		values = {v for v in range(len(grid) + 1)}
		values -= get_column_values(grid, c)

		if 0 not in values:
			possible_val_col = []

			# Запись возможных значений в каждую ячейку строки
			for r in range(size):
				if not grid[r][c]:
					possible_val_col.append(((r, c), possible_grid[r][c]))

			# Просмотр для каждой пустой ячейки, есть ли значение которое существует в единственном экземпляре
			if last_hero(grid, possible_val_col):
					possible_grid = make_possible_grid(grid)

	return filled(grid)



