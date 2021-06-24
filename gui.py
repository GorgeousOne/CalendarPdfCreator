import os
import tkinter as tk
from tkinter import filedialog as fd

import datetime
import CalenderPdfCreator


class Window:

	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Calendar PDF Creator")

		self.header = tk.Label(self.root, text="Year to create calendar of:")

		self.year_text = tk.StringVar()
		self.year_text.trace_add("write", self.check_numbers)
		self.year_text.set(datetime.date.today().year)

		self.directory_text = tk.StringVar()
		self.directory_text.trace_add("write", self.check_directory)
		self.directory_input = tk.Entry(self.root, textvariable=self.directory_text, width=70)

		self.create_button = tk.Button(self.root, text='Create PDF', command=self.create_calendar)
		self.browse_button = tk.Button(self.root, text='Open...', command=lambda: self.browse_file_system(self.last_path))

		self.year_input = tk.Entry(self.root, textvariable=self.year_text)
		self.last_path = os.path.dirname(os.path.realpath(__file__))
		self.directory_text.set(self.last_path)

		self.header.pack(pady=10)
		self.year_input.pack(pady=10)
		self.create_button.pack(pady=10)
		self.directory_input.pack(padx=10, pady=10)
		self.browse_button.pack(pady=(10, 20))

		self.root.minsize(500, 250)
		self.root.mainloop()

	def check_numbers(self, *args):
		digits = []
		for char in self.year_text.get():
			if char.isdigit():
				digits.append(char)
		self.year_text.set(''.join(digits)[0:4])

	def check_directory(self, *args):
		directory = self.directory_text.get()
		if os.path.isdir(directory):
			self.directory_input.config(fg='black')
			self.create_button.config(state="active")
			self.last_path = directory
		else:
			self.directory_input.config(fg='red')
			self.create_button.config(state="disabled")

	def create_calendar(self):
		self.create_button.config(state="disabled", text="Processing...")
		CalenderPdfCreator.print_year(int(self.year_text.get()))
		self.create_button.config(state="active", text="Done!")
		self.create_button.after(2000, lambda: self.create_button.config(state="active", text="Create PDF"))

	def browse_file_system(self, directory):
		new_dir = fd.askdirectory(initialdir=directory, title="Select a folder...")
		if new_dir:
			self.last_path = new_dir
			self.directory_text.set(self.last_path)


if __name__ == "__main__":
	CalenderPdfCreator.init()
	Window()
