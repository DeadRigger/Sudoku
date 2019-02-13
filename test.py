from kivy.app import App
from kivy.graphics.vertex_instructions import Line

from constants import *

from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.properties import ListProperty
from kivy.properties import NumericProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from random import random
from test_generate_sudoku import generate_field, find_possible_values

from kivy.config import Config

Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 320)
Config.set("graphics", "height", 640)
Config.set("graphics", "maxfps", 30)


class Cell(ToggleButton):
	coords = ListProperty()


class Grid(GridLayout):
	def __init__(self, size, **kwargs):
		super().__init__(**kwargs)

		# Field
		self.active_ceil = None
		self.field = generate_field(size, DIFFICULTY_LIST[DIFFICULTY])
		count_number = self.cols

		for r in range(count_number):
			for c in range(count_number):
				if self.field[r][c]:
					text = str(self.field[r][c])
				else:
					text = ""

				cell = Cell(
					coords=(r, c),
					text=text,
					group='field',
					background_normal='',
					background_color=[1, 1, 1, 1],
					color=[0, 0, 0, 1],
					on_press=self.click
				)

				self.add_widget(cell)

		# Keyboard
		for i in range(count_number):
			self.add_widget(Widget())

		for i in range(count_number):
			self.add_widget(Button(text=str(i + 1), on_press=self.entry))

	def generate(self, difficult):
		self.clear_widgets()
		self.active_ceil = None
		self.field = generate_field(int(self.cols ** 0.5), DIFFICULTY_LIST[difficult])
		count_number = self.cols

		for r in range(count_number):
			for c in range(count_number):
				if self.field[r][c]:
					text = str(self.field[r][c])
				else:
					text = ""

				self.add_widget(Cell(
					coords=(r, c),
					text=text,
					group='field',
					background_normal='',
					background_color=[1, 1, 1, 1],
					color=[0, 0, 0, 1],
					on_press=self.click
				))

		for i in range(count_number):
			self.add_widget(Widget())

		for i in range(count_number):
			self.add_widget(Button(text=str(i + 1), on_press=self.entry))

	def click(self, instance):
		self.active_ceil = instance
		print(find_possible_values(self.field, self.active_ceil.coords[0], self.active_ceil.coords[1]))

	def entry(self, instance):
		if self.active_ceil is not None:
			if self.active_ceil.text == instance.text:
				self.active_ceil.text = ''
				self.field[self.active_ceil.coords[0]][self.active_ceil.coords[1]] = 0
			else:
				self.active_ceil.text = instance.text
				self.field[self.active_ceil.coords[0]][self.active_ceil.coords[1]] = int(instance.text)
		print(instance.text)


class TestApp(App):
	def build(self):
		size_field = 3
		bl = BoxLayout(orientation="vertical", padding=25)

		# Menu
		dd = DropDown()
		easy = Button(text="Easy", size_hint=(0.25, None), height=44)
		easy.bind(on_release=lambda text: dd.select(easy.text))
		dd.add_widget(easy)
		medium = Button(text="Medium", size_hint=(0.25, None), height=44)
		medium.bind(on_release=lambda text: dd.select(medium.text))
		dd.add_widget(medium)
		hard = Button(text="Hard", size_hint=(0.25, None), height=44)
		hard.bind(on_release=lambda text: dd.select(hard.text))
		dd.add_widget(hard)

		menu = Button(text="New game", on_release=dd.open, padding=(0, 15), size_hint=(0.25, None), height=44)

		menu.add_widget(dd)

		self.gl = Grid(size=size_field, cols=size_field ** 2, size_hint=(1, 0.8))

		bl.add_widget(menu)
		bl.add_widget(self.gl)

		dd.bind(on_select=self.new_game)
		return bl

	def new_game(self, instance, text):
		print(text.lower())
		self.gl.generate(text.lower())


if __name__ == "__main__":
	TestApp().run()
