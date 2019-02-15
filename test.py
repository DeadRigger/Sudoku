from kivy.app import App
from kivy.config import Config

Config.set("graphics", "width", 480)
Config.set("graphics", "height", 720)
Config.set("graphics", "resizable", 0)

from constants import *

from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label

from kivy.properties import ListProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from test_generate_sudoku import generate_field, make_possible_grid, filled, find_possible_values


class MainLayout(BoxLayout):
	pass


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

	def generate(self, difficult):
		self.clear_widgets()

		# Field
		size = self.cols ** 2
		size_block = self.cols
		self.active_ceil = None
		self.field = generate_field(size_block, DIFFICULTY_LIST[difficult])
		self.possible_grid = make_possible_grid(self.field)
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
					on_press=self.entry))
			self.add_widget(bl)

		if DISABLE_KEY_NUMBER: self.disabled_numbers()

	# Called when touch on a grid cell
	def click(self, instance):
		self.active_ceil = instance
		self.possible_grid = make_possible_grid(self.field)

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
			if filled(self.field):
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


class Menu(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.dd = DropDown()

		self.dd.dismiss()

		new = Button(
			text="New",
			background_normal='',
			background_color=[1, 1, 1, 1],
			color=[0, 0, 0, 1],
			on_release=self.dd.open
		)

		easy = Button(
			text="easy", size_hint=(0.25, None), height=44,
			background_normal='',
			background_color=[1, 1, 1, 1],
			color=[0, 0, 0, 1],
			on_release=lambda text: self.dd.select(easy.text)
		)
		self.dd.add_widget(easy)

		medium = Button(
			text="medium", size_hint=(0.25, None), height=44,
			background_normal='',
			background_color=[1, 1, 1, 1],
			color=[0, 0, 0, 1],
			on_release=lambda text: self.dd.select(medium.text)
		)
		self.dd.add_widget(medium)

		hard = Button(
			text="hard", size_hint=(0.25, None), height=44,
			background_normal='',
			background_color=[1, 1, 1, 1],
			color=[0, 0, 0, 1],
			on_release=lambda text: self.dd.select(hard.text)
		)
		self.dd.add_widget(hard)

		new.add_widget(self.dd)
		self.add_widget(new)


class TestApp(App):
	def build(self):
		self.title = "Sudoku"
		self.size_field = 3
		bl = MainLayout(orientation="vertical", padding=25)

		self.menu = Menu(padding=(0, 0, 0, 15), size_hint=(0.25, 0.1))
		self.grid = Grid(cols=self.size_field, spacing=4, size_hint=(1, 0.9))
		self.grid.generate(DIFFICULTY)

		bl.add_widget(self.menu)
		bl.add_widget(self.grid)

		self.menu.dd.bind(on_select=lambda instance, text: self.grid.generate(text))

		return bl


if __name__ == "__main__":
	TestApp().run()
