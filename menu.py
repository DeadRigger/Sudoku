from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class Menu(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.dd = DropDown()

		self.dd.dismiss()

		new = Button(
			text="New",
			background_normal='',
    		background_down='',
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
