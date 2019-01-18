from sudoku import Sudoku

import pygame 
import sys
import copy
import random as r

# Colors
BACKGROUND = (255, 255, 255)
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
FPS = 24
display_width = 500
display_height = 500
name_app = 'Sudoku'
START_POSX_FIELD = 12
START_POSY_FIELD = 12
CEIL_SIZE = 48
BLOCK_SIZE = CEIL_SIZE * 3
DIFFICULTY_LIST = {
	'easy': 40,
	'medium': 31,
	'hard': 22
}
font_name = 'Comic San'
font_size = 30
difficulty = 'medium'

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
		self.size = size
		self.border = border
		self.height = size_ceil * size ** 2
		self.width = size_ceil * size ** 2
		self.active_ceil = None
		self.table = [[None for i in range(9)] for j in range(9)]
		self.empty_ceils = [[False for i in range(9)] for j in range(9)]
		self.cycle_generate = 10
		self.generate()
		self.drawField()
	
	# Generate
	def generate(self):
		self.table = copy.deepcopy(self.base_table)

		mix_func = ['self.SwapBigRow',
					'self.SwapBigColumn',
					'self.SwapSmallRow',
					'self.SwapSmallColumn']

		for i in xrange(1, self.cycle_generate):
			id_func = r.randrange(0,len(mix_func),1)
			eval(mix_func[id_func])

	def SwapBigRow(self):
		row1 = r.randrange(0, 3)
		row2 = r.randrange(0, 3)

		while row1 == row2:
			row2 = r.randrange(0, 3)

		for i in range(3):
			self.table[row1 * 3 + i], self.table[row2 * 3 + i] = \
				self.table[row2 * 3 + i], self.table[row1 * 3 + i]

	def SwapBigColumn(self):
		col1 = r.randrange(0, 3)
		col2 = r.randrange(0, 3)

		while col1 == col2:
			col2 = r.randrange(0, 3)

		for c in range(3):
			for i in range(9):
				self.table[i][col1 * 3 + c], self.table[i][col2 * 3 + c] = \
					self.table[i][col2 * 3 + c], self.table[i][col1 * 3 + c]

	def SwapSmallRow(self):
		row = r.randrange(0, 3)
		smallRow1 = r.randrange(0, 3)
		smallRow2 = r.randrange(0, 3)

		while smallRow1 == smallRow2:
			smallRow2 = r.randrange(0, 3)

		self.table[row * 3 + smallRow1], self.table[row * 3 + smallRow2] = \
			self.table[row * 3 + smallRow2], self.table[row * 3 + smallRow1]

	def SwapSmallColumn(self):
		col = r.randrange(0, 3)
		smallCol1 = r.randrange(0, 3)
		smallCol2 = r.randrange(0, 3)

		while smallCol1 == smallCol2:
			smallCol2 = r.randrange(0, 3)

		for i in range(9):
			self.table[i][col * 3 + smallCol1], self.table[i][col * 3 + smallCol2] = \
				self.table[i][col * 3 + smallCol2], self.table[i][col * 3 + smallCol1]

	def ChangeDifficult(self):
		

	# Display
	def drawField(self):
		self.screen.fill(BACKGROUND)
		pygame.font.init()
		pygame.draw.rect(self.screen, [200, 200, 200], self.field) # draw field

		for row in range(3):
			for col in range(3):
				size_block = self.size_ceil * 3
				start_point = (self.start_point[0] + col * size_block, 
					self.start_point[1] + row * size_block)
				self.drawBlock(start_point, row, col, size_block)

	def drawBlock(self, start_point, block_row, block_col, size, border=2):
		self.drawCeil(start_point, size, self.border['block'])

		for row in range(3):
			for col in range(3):
				pos = (start_point[0] + col * self.size_ceil,
					start_point[1] + row * self.size_ceil)
				ceil = [block_row*3 + row, block_col*3 + col]

				if self.active_ceil == ceil:
					self.drawCeil(pos,self.size_ceil, None)
				
				number = self.table[ceil[0]][ceil[1]]

				self.drawCeil(pos, self.size_ceil, self.border['ceil'],
				 number)

	def drawCeil(self, start_point, size, border=1, text=None):
		font = pygame.font.SysFont(font_name, font_size)
		if border is None:
			pygame.draw.rect(self.screen, BLUE,
			 (start_point[0], start_point[1],
			  size, size))
		else:
			pygame.draw.rect(self.screen, self.border['color'],
			 (start_point[0], start_point[1],
			  size, size),
			 border)

		if text is not None:
			number = font.render(str(text), True, BLACK)
			pos_num_x = start_point[0] + (size - number.get_width()) / 2
			pos_num_y = start_point[1] + (size - number.get_height()) / 2
			self.screen.blit(number, (pos_num_x, pos_num_y))

	# Test
	def solve(self, solution):
		countValues = 1
		changeCountValues = True

		while True:
			if changeCountValues == False:
				countValues += 1

			changeCountValues = False
			for row in range(self.size ** 2):
				for col in range(self.size ** 2):
					possibleValues = findPossibleValues(solution, row, col)
					countPossibleValues = len(possibleValues)
					if countPossibleValues == countValues:
						solution[row][col] = possibleValues.pop()
						changeCountValues = True
					elif countPossibleValues == 0:
						


    def findPossibleValues(self, puzzle, rowIndex, columnIndex):
        values = {v for v in range(1, 10)}
        values -= self.getRowValues(puzzle, rowIndex)
        values -= self.getColumnValues(puzzle, columnIndex)
        values -= self.getBlockValues(puzzle, rowIndex, columnIndex)
        return values

    @staticmethod
    def getRowValues(puzzle, rowIndex):
        return set(puzzle[rowIndex][:])

    @staticmethod
    def getColumnValues(puzzle, columnIndex):
        return {puzzle[r][columnIndex] for r in range(9)}

    @staticmethod
    def getBlockValues(puzzle, rowIndex, columnIndex):
        blockRowStart = 3 * (rowIndex // 3)
        blockColumnStart = 3 * (columnIndex // 3)
        return {
            puzzle[blockRowStart + r][blockColumnStart + c]
            for r in range(3)
            for c in range(3)
        }

def main(): 
	pygame.init() 
	clock = pygame.time.Clock() 
	fps = 30
	start_point = (10, 80)
	height = 500
	width = height - start_point[1] * 2 + start_point[0] * 2
	size = [width, height]

	# Установка размера ячейки в зависимости от ширины экрана
	if width - start_point[0] >= height - start_point[1]:
		size_ceil = int((height - start_point[1] * 2) / 9)
		font_size = size_ceil
	else:
		size_ceil = int((width - start_point[0] * 2) / 9)
		font_size = size_ceil

	screen = pygame.display.set_mode(size)

	size_field = size_ceil * 9
	field = pygame.Rect(start_point[0], start_point[1],
		 size_field, size_field)
	border = {
		'block': 2,
		'ceil': 1,
		'color': BLACK
	}

	s = Sudoku(screen, field, start_point, size_ceil, border)

	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = event.pos # gets mouse position 

				# checks if mouse position is over the button 

				if field.collidepoint(mouse_pos):
					# prints current location of mouse 
					ceil = [int((mouse_pos[1] - start_point[1]) / size_ceil),
					 int((mouse_pos[0] - start_point[0]) / size_ceil)]

					s.active_ceil = ceil
					s.drawField()
					print(s.table[ceil[0]][ceil[1]])

					pygame.display.update()

		clock.tick(fps) 

main()

pygame.quit()