from sudoku import Sudoku
from pygame.locals import *
from functions import *
from threading import Thread


def display():
	m.display()
	display_footer(screen, keyboard, size_ceil)
	s.drawField(s.table)


class Menu:
	def __init__(self, screen, panel):
		self.open = False
		self.screen = screen
		self.panel = panel
		self.width_block = panel.w / 5
		self.margin_left = panel.w / 4
		self.height_block = 60
		self.menu = {
			'new': {
				'rect': (panel.x, panel.y, self.width_block, self.height_block),
				'draw': 'drawCenterText(screen, "NEW", self.menu["new"]["rect"])',
				'show_submenu': False,
				'submenu': {
					'easy': {
						'rect': (panel.x + self.margin_left, panel.y, self.width_block, self.height_block),
						'draw': 'drawCenterText(screen, "EASY", self.menu["new"]["submenu"]["easy"]["rect"])',
					},
					'medium': {
						'rect': (panel.x + self.margin_left * 2, panel.y, self.width_block, self.height_block),
						'draw': 'drawCenterText(screen, "MEDIUM", self.menu["new"]["submenu"]["medium"]["rect"])',
					},
					'hard': {
						'rect': (panel.x + self.margin_left * 3, panel.y, self.width_block, self.height_block),
						'draw': 'drawCenterText(screen, "HARD", self.menu["new"]["submenu"]["hard"]["rect"])',
					},
				}
			},
		}

	def display(self, point=None):
		pygame.draw.rect(self.screen, BACKGROUND, self.panel)
		pygame.font.init()

		for pnt in self.menu.keys():
			eval(self.menu[pnt]['draw'])

		if point is not None:
			if not self.menu[point]['show_submenu']:
				self.menu[point]['show_submenu'] = True
				for subpoint in self.menu[point]['submenu'].keys():
					eval(self.menu[point]['submenu'][subpoint]['draw'])
			else:
				self.menu[point]['show_submenu'] = False

	def show(self, point):
		if self.open:
			self.open = False
		else:
			self.open = True

		self.display(point)

	def changeLevel(self, difficult):
		s.generate_field(s.min_size, DIFFICULTY_LIST[difficult])
		for point in self.menu.keys():
			self.menu[point]['show_submenu'] = False
		display()

	def collide(self, mouse_pos):
		for point in self.menu.keys():
			rect = self.menu[point]['rect']
			if rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and rect[1] <= mouse_pos[1] <= rect[1] + rect[3]:
				self.show(point)
				return
			for subpoint in self.menu[point]['submenu'].keys():
				rect = self.menu[point]['submenu'][subpoint]['rect']
				if rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and rect[1] <= mouse_pos[1] <= rect[1] + rect[3]:
					self.changeLevel(subpoint)
					return


def display_footer(screen, panel, size):
	for i in range(SIZE ** 2):
		drawCenterText(screen, str(i + 1), (panel.x + i * size, panel.y, size, panel.h))


# Initialization objects pygame
pygame.init()
clock = pygame.time.Clock()
size = [WIDTH, HEIGHT]

# Установка размера ячейки в зависимости от ширины экрана
size_ceil = int((WIDTH - START_POINT[0] * 2) / 9)

# Размер текста соответствует размеру ячейки
font_size = size_ceil

screen = pygame.display.set_mode(size)
pygame.display.set_caption(NAME_APP)

size_field = size_ceil * 9

# Меню, в котором можно выбрать сложность уровня и начать его
panel = pygame.Rect(START_POINT[0], 0, WIDTH - START_POINT[0], START_POINT[1])

# Rect, на котором будет располагаться сетка судоку
grid = pygame.Rect(START_POINT[0], START_POINT[1], size_field, size_field)

# Клавиатура при нажатии, на которую активная ячейка будет заполнена тем числом, на которое нажали
pos_x = START_POINT[0]
pos_y = START_POINT[1] + size_field
keyboard = pygame.Rect(pos_x, pos_y, WIDTH - pos_x, HEIGHT - pos_y)

border = {
	'block': 2,
	'ceil': 1,
	'color': BORDER_COLOR
}

screen.fill(BACKGROUND)
pygame.font.init()

s = Sudoku(screen, grid, START_POINT, size_ceil, border, size=SIZE)
m = Menu(screen, panel)

display()
pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit(1)

		elif event.type == KEYDOWN:
			if 0 < event.key - 48 < 10:
				number = event.key - 48
				s.activateCeil(s.active_ceil, number)
				pygame.display.update()

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = event.pos  # gets mouse position

			# checks if mouse position is over the button

			if grid.collidepoint(mouse_pos) and event.button == 1:
				# prints current location of mouse
				ceil = [int((mouse_pos[1] - START_POINT[1]) / size_ceil),
						int((mouse_pos[0] - START_POINT[0]) / size_ceil)]

				s.activateCeil(ceil)
				possVal = s.find_possible_values(s.table, ceil[0], ceil[1])
				if possVal:
					print(possVal)
				pygame.display.update()
			elif keyboard.collidepoint(mouse_pos) and event.button == 1:
				# prints current location of mouse
				number = int((mouse_pos[0] - START_POINT[0]) / size_ceil) + 1
				s.activateCeil(s.active_ceil, number)
				pygame.display.update()
			elif panel.collidepoint(mouse_pos) and event.button == 1:
				m.collide(mouse_pos)
				pygame.display.update()

	clock.tick(FPS)
	pygame.display.update()
