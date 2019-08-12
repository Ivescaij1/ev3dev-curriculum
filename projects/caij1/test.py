import turtle_warrior as tw
import rosegraphics as rg
import robot_controller as robo
import tkinter as tk
import math


canvas = tk.Canvas(width=960, height=400)
canvas.pack()

warrior = tw.Warrior()
warrior.lv = 100

tt = tw.VisualTurtle(canvas, warrior)

tt.visual_generate_map()

for _ in range(10):
    tw.Monster(warrior, canvas)

canvas.wait_window()