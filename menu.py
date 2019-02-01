from functions import *


class Menu:
	def __init__(self, screen, panel):
		self.open = False
		self.screen = screen
		self.panel = panel
		self.width_block = panel.w / 5
		self.margin_left = panel.w / 4
		self.height_block = panel.h * 2/3
		self.menu = {
			'new': {
				'rect': (panel.x, panel.y, self.width_block, self.height_block),
				'draw': 'Button(self.screen, self.menu["new"]["rect"], "NEW").draw()',
				'show_submenu': False,
				'submenu': {
					'easy': {
						'rect': (panel.x + self.margin_left, panel.y, self.width_block, self.height_block),
						'draw': 'Button(self.screen, self.menu["new"]["submenu"]["easy"]["rect"], "EASY").draw()',
					},
					'medium': {
						'rect': (panel.x + self.margin_left * 2, panel.y, self.width_block, self.height_block),
						'draw': 'Button(self.screen, self.menu["new"]["submenu"]["medium"]["rect"], "MEDIUM").draw()',
					},
					'hard': {
						'rect': (panel.x + self.margin_left * 3, panel.y, self.width_block, self.height_block),
						'draw': 'Button(self.screen, self.menu["new"]["submenu"]["hard"]["rect"], "HARD").draw()',
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

		self.display(point=point)

	def changeLevel(self, difficult, sudoku):
		sudoku.generate_field(sudoku.min_size, DIFFICULTY_LIST[difficult])
		for point in self.menu.keys():
			self.menu[point]['show_submenu'] = False
		self.open = False
		self.display()

	def collide(self, mouse_pos, sudoku):
		for point in self.menu.keys():
			rect = self.menu[point]['rect']
			if rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and rect[1] <= mouse_pos[1] <= rect[1] + rect[3]:
				self.show(point)
				return
			if self.open:
				for subpoint in self.menu[point]['submenu'].keys():
					rect = self.menu[point]['submenu'][subpoint]['rect']
					if rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and rect[1] <= mouse_pos[1] <= rect[1] + rect[3]:
						self.changeLevel(subpoint, sudoku)
						return 'new game'
