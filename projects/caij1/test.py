import turtle_warrior as tw
import rosegraphics as rg
import robot_controller as robo
import tkinter as tk
import math


canvas = tk.Canvas(width=960, height=400)
canvas.pack()
#
# warrior = tw.Warrior()
#
# tt = tw.VisualTurtle(canvas, warrior)
#
# tt.visual_generate_map()

# canvas.create_rectangle(10,10,300,50)


def shape(x, y, deg, canva):
    pc_x = x
    pc_y = y
    pa_x = x + math.cos(deg) * 100
    pa_y = y - math.sin(deg) * 100
    pu_x = x - math.cos(deg - 45) * 100
    pu_y = y - math.sin(deg - 45) * 100
    pd_x = x - math.cos(deg - 45) * 100
    pd_y = y + math.sin(deg - 45) * 100

    canva.create_polygon(pc_x, pc_y, pu_x, pu_y, pa_x, pa_y, pd_x, pd_y, fill='', outline='black')

shape(100, 100, 0, canvas)

canvas.wait_window()