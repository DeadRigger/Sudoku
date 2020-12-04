from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.clock import Clock


class Menu(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.popmenu = ModalView(size_hint=(0.5, 0.5))
		self.popmenu.dismiss()

		layout = GridLayout(cols=2)
		layout_menu = GridLayout(cols=1, size_hint=(.5, .5))

		self.time = Label(text="00:00", color=[0, 0, 0, 1], size_hint_x=None, halign="right")

		self.new = Button(
			text="New",
			size_hint_x=None,
			background_normal='',
			background_down='',
			background_color=[1, 1, 1, 1],
			color=[0, 0, 0, 1],
			on_release=self.popmenu.open
		)

		layout.add_widget(self.new)
		layout.add_widget(self.time)

		self.easy = Button(
			text="EASY", size_hint=(0.25, None), height=44,
			background_normal='',
			background_color=[0.2, 0.2, 0.2, 0],
			color=[1, 1, 1, 1]
		)

		self.medium = Button(
			text="MEDIUM", size_hint=(0.25, None), height=44,
			background_normal='',
			background_color=[0.2, 0.2, 0.2, 0],
			color=[1, 1, 1, 1]
		)

		self.hard = Button(
			text="HARD", size_hint=(0.25, None), height=44,
			background_normal='',
			background_color=[0.2, 0.2, 0.2, 0],
			color=[1, 1, 1, 1]
		)

		layout_menu.add_widget(self.easy)
		layout_menu.add_widget(self.medium)
		layout_menu.add_widget(self.hard)

		self.popmenu.add_widget(layout_menu)
		self.add_widget(layout)

		Clock.schedule_interval(self.increase_time, 1)

	def increase_time(self, dt):
		t = self.time.text.split(":")
		if 0 < int(t[1]) + 1 <= 59:
			sec = int(t[1]) + 1
			if sec < 10:
				sec = "0" + str(sec)
			else:
				sec = str(sec)
			self.time.text = t[0] + ":" + sec
		elif int(t[1]) + 1 == 60:
			minute = int(t[1]) + 1
			if minute < 10:
				minute = "0" + str(minute)
			else:
				minute = str(minute)
			self.time.text = minute + ":00"
