import os
import tkinter as tk
from tkinter import ttk
from ttkthemes
from PIL import ImageTk


class App():
	def __init__(self, parent) -> None:
		self.parent = parent
		self.cwd = imageDirectory = os.getcwd() + "/samples/20220517/1652784219.0/"
		self.mainWindow()

	def mainWindow(self):
		tk.Button(text="add image", command=self.addImage).grid(row=1,column=1)

	def addImage(self):
		img = ImageTk.PhotoImage(file=self.cwd + "kalium_cropped.png")
		panel = tk.Label(root, image=img).grid(row=2, column=1)


if __name__ == '__main__':
	root = tk.Tk()
	root.title("merge")
	root.geometry('1024x768')
	root.style = ttkthemes.ThemedStyle()

	app = App(root)
	root.mainloop()
