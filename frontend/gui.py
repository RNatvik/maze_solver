from tkinter import *
from frontend.scene import MainScene


root = Tk(className="Maze Solver 2000 TM")
frame = MainScene()
frame.main_frame.pack(side=LEFT)
root.mainloop()
