import time
import sys

from test_generate_sudoku import generate_field, print_grid, solver, filled


def convert_array(array):
	if isinstance(array, list):
		s = ''
		for row in array:
			for num in row:
				s += str(num)
		return s
	else:
		size = int(len(array) ** 0.5)
		l = [[0 for i in range(size)]for j in range(size)]
		for row in range(size):
			for col in range(size):
				l[row][col] = array[row * 9 + col]
		return l


def same_row(i, j):
	return int(i / 9) == int(j / 9)


def same_col(i, j):
	return (i - j) % 9 == 0


def same_block(i, j):
	return int(i / 27) == int(j / 27) and int(i % 9 / 3) == int(j % 9 / 3)


def r(a):
	i = a.find('0')
	if i == -1:
		table = convert_array(a)
		if filled(table):
			return table
		print("No correct field")
		return

	excluded_numbers = set()
	for j in range(81):
		if same_row(i, j) or same_col(i, j) or same_block(i, j):
			excluded_numbers.add(a[j])

	for m in '123456789':
		if m not in excluded_numbers:
			grid = r(a[:i] + m + a[i + 1:])
			if grid is not None:
				return grid


size_grid = 9
complications = {
	'easy': ((33, 40), 72),
	'medium': ((26, 33), 102),
	'hard': ((20, 26), 175)
}

tm_enum = 0
tm_smart = 0

tm = time.time()
main_grid = generate_field(int(pow(size_grid, 0.5)), complications['hard'])
print_grid(main_grid)
print('Generate field ' + str(time.time() - tm) + ' sec.\n')

# test_str = convert_array(main_grid)
#
# tm = time.time()
# result = r(test_str)
# print_grid(result)
# tm_enum += time.time() - tm
# print('Solver field ' + str(tm_enum) + ' sec.\n')

tm = time.time()
solver(main_grid)
print_grid(main_grid)
tm_smart += time.time() - tm
print('Solver field ' + str(tm_smart) + ' sec.\n')

print('Ratio:\n\tenum/algorithm ' + str(tm_enum / tm_smart))
