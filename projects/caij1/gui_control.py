import tkinter as tk
from tkinter import ttk
import sys


def main():

    root = tk.Tk()
    root.title("Game Control")

    # grid(0, 1-3) & (1-3, 0): Empty frame that holds left and right buttons frame always in same size
    # TODO: check width after button is done
    top_bar_left = tk.Frame(root, width=300, height=0)
    top_bar_left.grid(row=0, column=1)
    top_bar_right = ttk.Frame(root, width=1080, height=0)
    top_bar_right.grid(row=0, column=2)
    top_bar_right = ttk.Frame(root, width=300, height=0)
    top_bar_right.grid(row=0, column=3)

    side_bar_top = tk.Frame(root, width=0, height=75)
    side_bar_top.grid(row=1, column=0)

    # grid(1,1): TOP left frame that contain the position label and entry box
    # 3 column, 2 row used, with one free column/row for stikcy room
    position_frame = tk.Frame(root, bg='orange red')
    position_frame.grid(row=1, column=1, sticky="nsew")
    position_frame.grid_rowconfigure([0, 3], weight=1)
    position_frame.grid_columnconfigure([0, 4], weight=1)

    position_label = tk.Label(position_frame, text="Position", bg='orange red')
    position_label.grid(row=1, column=2)
    x_entry = ttk.Entry(position_frame, width=8, justify=tk.CENTER)
    x_entry.grid(row=2, column=1)
    y_entry = ttk.Entry(position_frame, width=8, justify=tk.CENTER)
    y_entry.grid(row=2, column=3)

    # grid(1,2): character button, map button, start button
    # 3 column, 1 row used, with space between buttons and perimeter [row 0 & 2, column 0 & 2 & 4 & 6] expandable.
    start_frame = tk.Frame(root, bg='black')
    start_frame.grid(row=1, column=2, sticky='nsew')
    start_frame.grid_rowconfigure([0, 2], weight=1)
    start_frame.grid_columnconfigure([0, 2, 4, 6], weight=1)

    map_button = ttk.Button(start_frame, text="Map <M>", width=12)
    map_button.grid(row=1, column=1)
    map_button['command'] = lambda: print("Map button")
    root.bind('<m>', lambda event: print("Map key"))

    start_button = ttk.Button(start_frame, text="Start <Enter>", width=12)
    start_button.grid(row=1, column=3)
    start_button['command'] = lambda: print("Start button")
    root.bind('<Return>', lambda event: print("Start key"))

    character_button = ttk.Button(start_frame, text="Character <P>", width=12)
    character_button.grid(row=1, column=5)
    character_button['command'] = lambda: print("Start button")
    root.bind('<p>', lambda event: print("Start key"))

    # grid(1,3) TOP right frame that contain the direction label and entry box
    # 1 column, 2 row used, with one free column/row for sticky room
    direction_frame = tk.Frame(root, bg='dodger blue')
    direction_frame.grid(row=1, column=3, sticky='nsew')
    direction_frame.grid_rowconfigure([0, 3], weight=1)
    direction_frame.grid_columnconfigure([0, 2], weight=1)

    direction_label = tk.Label(direction_frame, text="Direction", bg='dodger blue')
    direction_label.grid(row=1, column=1)
    direction_entry = ttk.Entry(direction_frame, width=8, justify=tk.CENTER)
    direction_entry.grid(row=2, column=1)

    # grid(2, 2) Canvas display frame with tkinter canvas, free grid around perimeter.
    canvas_frame = tk.Frame(root, bg='black')
    canvas_frame.grid(row=2, column=2, sticky='nsew')
    canvas_frame.grid_rowconfigure([0, 2], weight=1)
    canvas_frame.grid_columnconfigure([0, 2], weight=1)

    canvas = tk.Canvas(canvas_frame, width=960, height=400)
    canvas.grid(row=1, column=1)

    # grid(3,2): Text display frame with tkinter text widget, free grid around perimeter.
    # 1 character width = 15 pixel with 24 font
    text_frame = tk.Frame(root, bg='black')
    text_frame.grid(row=3, column=2, sticky='nsew')
    text_frame.grid_rowconfigure([0, 2], weight=1)
    text_frame.grid_columnconfigure([0, 2], weight=1)

    textbox = tk.Text(text_frame, width=64, height=5, font=('Comic Sans MS', 24, 'bold'), background='lightgray')
    textbox.grid(row=1, column=1)
    textbox.tag_configure("center", justify='center')










    main_frame = ttk.Frame(root, padding=50)
    main_frame.grid(row=4, column=2, sticky='nswe')
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)






    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: print("Forward button")
    root.bind('<w>', lambda event: print("Forward key"))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: print("Left button")
    root.bind('<a>', lambda event: print("Left key"))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: print("Stop button")
    root.bind('<space>', lambda event: print("Stop key"))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: print("Right button")
    root.bind('<d>', lambda event: print("Right key"))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: print("Back button")
    root.bind('<s>', lambda event: print("Back key"))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: print("Up button")
    root.bind('<u>', lambda event: print("Up key"))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: print("Down button")
    root.bind('<j>', lambda event: print("Down key"))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = lambda: print("Quit button")
    root.bind('c', lambda event: print("Quit key"))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = lambda: exit()

    def text_director(inputs):
        textbox.insert('0.1', inputs, 'center')

    sys.stdout.write = text_director  # whenever sys.stdout.write is called, redirector is called.
    root.grid_rowconfigure([1, 2, 3], weight=1)
    root.grid_columnconfigure([1, 2, 3], weight=1)

    root.mainloop()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()