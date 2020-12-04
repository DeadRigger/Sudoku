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
		main_layout = MainLayout(orientation="vertical", padding=25)

		self.title = "Sudoku"
		self.size_field = 3
		self.menu = Menu(padding=(0, 0, 0, 15), size_hint=(1, 0.1))
		self.grid = Grid(cols=self.size_field, spacing=4, size_hint=(1, 0.9))
		self.grid.generate(DIFFICULTY)

		# Add widgets on the main layout
		main_layout.add_widget(self.menu)
		main_layout.add_widget(self.grid)

		# Binds
		self.menu.easy.bind(on_release=lambda button: self.menu_button(button.text))
		self.menu.medium.bind(on_release=lambda button: self.menu_button(button.text))
		self.menu.hard.bind(on_release=lambda button: self.menu_button(button.text))

		return main_layout

	def menu_button(self, text):
		self.grid.generate(text.lower())
		self.menu.popmenu.dismiss()


if __name__ == "__main__":
	SudokuApp().run()
