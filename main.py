from sudoku import Sudoku
from pygame.locals import *
from functions import *
from menu import Menu
import time


def display():
	display_footer(screen, keyboard, size_ceil)
	s.drawField(s.table)


def display_footer(screen, panel, size):
	for i in range(SIZE ** 2):
		drawCenterText(screen, str(i + 1), (panel.x + i * size, panel.y, size, panel.h))


def display_timer(screen, panel, time):
	pygame.draw.rect(screen, BACKGROUND, panel)
	if time < 600:
		minute = '0' + str(int(time // 60))
	else:
		minute = str(int(time // 60))

	if time % 60 < 10:
		second = '0' + str(int(time % 60))
	else:
		second = str(int(time % 60))

	font = pygame.font.SysFont('Arial', 15)
	tm = font.render(minute + ':' + second, True, BLACK)
	pos_x = WIDTH - START_POINT[0] - tm.get_width()
	pos_y = panel.y + (panel.h - tm.get_height()) / 2
	screen.blit(tm, (pos_x, pos_y))


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
panel = pygame.Rect(START_POINT[0], 0, WIDTH - START_POINT[0], START_POINT[1] * 2 / 3)

# Таймер, показывающий время с начала игры
timer = pygame.Rect(WIDTH * 2 / 3, START_POINT[1] * 2 / 3, WIDTH / 3, START_POINT[1] * 1 / 3)

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

m.display()
display()
pygame.display.update()

tm = time.time()
stop_timer = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit(1)

		elif event.type == KEYDOWN:
			if 0 < event.key - 48 < 10:
				number = event.key - 48
				stop_timer = s.activateCeil(s.active_ceil, number)

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
			elif keyboard.collidepoint(mouse_pos) and event.button == 1:
				# prints current location of mouse
				number = int((mouse_pos[0] - START_POINT[0]) / size_ceil) + 1
				stop_timer = s.activateCeil(s.active_ceil, number)
			elif panel.collidepoint(mouse_pos) and event.button == 1:
				if m.collide(mouse_pos, s) == 'new game':
					tm = time.time()
				display()

			pygame.display.update()

	if not stop_timer:
		curr_time = time.time() - tm
		display_timer(screen, timer, curr_time)
	pygame.display.update()
	clock.tick(FPS)
