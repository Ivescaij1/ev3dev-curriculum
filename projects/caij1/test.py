import turtle_warrior as tw
import rosegraphics as rg
import robot_controller as robo
import tkinter as tk
import math


canvas = tk.Canvas(width=960, height=400)
canvas.pack()

warrior = tw.Warrior()

tt = tw.VisualTurtle(canvas, warrior)

tt.visual_generate_map()

canvas.wait_window()