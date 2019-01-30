import time

from test_generate_sudoku import generate_field, print_grid, solver

size_grid = 9
complications = {
	'easy': ((33, 40), 72),
	'medium': ((26, 33), 102),
	'hard': ((20, 26), 175)
}


tm = time.time()
main_grid = generate_field(int(pow(size_grid, 0.5)), complications['easy'])
print_grid(main_grid)
print('Generate field ' + str(time.time()-tm) + ' sec.\n')

tm = time.time()
solver(main_grid)
print_grid(main_grid)
print('Solver field ' + str(time.time()-tm) + ' sec.')

