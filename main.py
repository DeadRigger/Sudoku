from kivy.app import App
from kivy.config import Config

Config.set("graphics", "width", 480)
Config.set("graphics", "height", 720)
Config.set("graphics", "resizable", 0)

from constants import DIFFICULTY
from menu import Menu
from sudoku import Grid

from kivy.uix.boxlayout import BoxLayout


class MainLayout(BoxLayout):
	pass


class SudokuApp(App):
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
	SudokuApp().run()
