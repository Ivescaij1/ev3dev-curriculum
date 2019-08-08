import tkinter as tk
from tkinter import ttk
import sys


def main():

    root = tk.Tk()
    root.title("Game Control")

    # grid(0, 1-3) & (1-3, 0): Empty frame that holds left and right buttons frame always in same size
    top_bar_left = tk.Frame(root, width=280, height=0)
    top_bar_left.grid(row=0, column=1)
    top_bar_right = ttk.Frame(root, width=1080, height=0)
    top_bar_right.grid(row=0, column=2)
    top_bar_right = ttk.Frame(root, width=280, height=0)
    top_bar_right.grid(row=0, column=3)

    side_bar_top = tk.Frame(root, width=0, height=75)
    side_bar_top.grid(row=1, column=0)
    side_bar_middle = tk.Frame(root, width=0, height=480)
    side_bar_middle.grid(row=2, column=0)
    side_bar_middle = tk.Frame(root, width=0, height=240)
    side_bar_middle.grid(row=3, column=0)

    # grid(1,1): TOP left frame that contain the position label and entry box
    # 3 column, 2 row used, with one free column/row for sticky room
    position_frame = tk.Frame(root, bg='orange red')
    position_frame.grid(row=1, column=1, sticky="nsew")
    position_frame.grid_rowconfigure([0, 3], weight=1)
    position_frame.grid_columnconfigure([0, 4], weight=1)

    position_label = tk.Label(position_frame, text="Position", bg='orange red')
    position_label.grid(row=2, column=2)
    x_entry = ttk.Entry(position_frame, width=8, justify=tk.CENTER)
    x_entry.grid(row=1, column=1)
    y_entry = ttk.Entry(position_frame, width=8, justify=tk.CENTER)
    y_entry.grid(row=1, column=3)

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
    direction_label.grid(row=2, column=1)
    direction_entry = ttk.Entry(direction_frame, width=8, justify=tk.CENTER)
    direction_entry.grid(row=1, column=1)

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

    # grid(2, 1) left move control, free grid around perimeter and between 'move' and direction button
    # * have row0 reserved even if not expandable
    move_frame = tk.Frame(root, bg='orange red')
    move_frame.grid(row=2, column=1, sticky='nsew')
    move_frame.grid_rowconfigure([2, 6], weight=1)
    move_frame.grid_columnconfigure([0, 4], weight=1)

    move_button = tk.Button(move_frame, text="Move", height=2, width=8)
    move_button.grid(row=1, column=2)
    move_button['command'] = lambda: print("Move button")

    w_button = tk.Button(move_frame, text="W", height=4, width=8)
    w_button.grid(row=3, column=2)
    w_button['command'] = lambda: print("Forward button")
    root.bind('<w>', lambda event: print("Forward key"))

    a_button = tk.Button(move_frame, text="A", height=4, width=8)
    a_button.grid(row=4, column=1)
    a_button['command'] = lambda: print("Left button")
    root.bind('<a>', lambda event: print("Left key"))

    stop_button = tk.Button(move_frame, text="Stop", height=4, width=8)
    stop_button.grid(row=4, column=2)
    stop_button['command'] = lambda: print("Stop button")
    root.bind('<space>', lambda event: print("Stop key"))

    d_button = tk.Button(move_frame, text="D", height=4, width=8)
    d_button.grid(row=4, column=3)
    d_button['command'] = lambda: print("Right button")
    root.bind('<d>', lambda event: print("Right key"))

    s_button = tk.Button(move_frame, text="S", height=4, width=8)
    s_button.grid(row=5, column=2)
    s_button['command'] = lambda: print("Back button")
    root.bind('<s>', lambda event: print("Back key"))

    # grid(2, 3) Right action control

    action_frame = tk.Frame(root, bg='dodger blue')
    action_frame.grid(row=2, column=3, sticky='nsew')
    action_frame.grid_rowconfigure([2, 4, 6, 8], weight=1)
    action_frame.grid_columnconfigure([0, 4], weight=1)

    turn_button = tk.Button(action_frame, text="Turn", height=2, width=8)
    turn_button.grid(row=1, column=2)
    turn_button['command'] = lambda: print("Turn button")

    att_button = tk.Button(action_frame, text="Attack \n<J>", height=4, width=8)
    att_button.grid(row=3, column=2)
    att_button['command'] = lambda: print("Att button")
    root.bind('<j>', lambda event: print("Att key"))

    skill_button = tk.Button(action_frame, text="Fire Ball \n<K>", height=4, width=8)
    skill_button.grid(row=5, column=2)
    skill_button['command'] = lambda: print("d Att button")
    root.bind('<k>', lambda event: print("d Att key"))

    rest_button = tk.Button(action_frame, text="Rest \n<L>", height=4, width=8)
    rest_button.grid(row=7, column=2)
    rest_button['command'] = lambda: print("rest button")
    root.bind('<l>', lambda event: print("rest key"))

    # grid (3, 1) hp/mp & exit display frame
    exit_frame = tk.Frame(root, bg='orange red')
    exit_frame.grid(row=3, column=1, sticky='nsew')
    exit_frame.grid_rowconfigure([0, 2, 4], weight=1)
    exit_frame.grid_columnconfigure([1, 4], weight=1)

    hp_label = tk.Label(exit_frame, text="HP", bg='orange red')
    hp_label.grid(row=1, column=2)
    hp = ttk.Entry(exit_frame, width=8, justify=tk.CENTER)
    hp.grid(row=1, column=3)

    mp_label = tk.Label(exit_frame, text="MP", bg='orange red')
    mp_label.grid(row=3, column=2)
    mp = ttk.Entry(exit_frame, width=8, justify=tk.CENTER)
    mp.grid(row=3, column=3)

    exit_button = ttk.Button(exit_frame, text="Exit <X>")
    exit_button.grid(row=5, column=0)
    exit_button['command'] = lambda: exit()
    root.bind('x', lambda event: exit())

    # grid (3, 3) action control frame
    turn_frame = tk.Frame(root, bg='dodger blue')
    turn_frame.grid(row=3, column=3, sticky='nsew')
    turn_frame.grid_rowconfigure([0, 4], weight=1)
    turn_frame.grid_columnconfigure([0, 4], weight=1)

    left_button = tk.Button(turn_frame, text="Left <Q>", height=4, width=8)
    left_button.grid(row=2, column=1)
    left_button['command'] = lambda: print("left button")
    root.bind('<q>', lambda event: print("left key"))

    right_button = tk.Button(turn_frame, text="Right <E>", height=4, width=8)
    right_button.grid(row=2, column=3)
    right_button['command'] = lambda: print("right button")
    root.bind('<e>', lambda event: print("right key"))

    up_button = tk.Button(turn_frame, text="Up", height=4, width=8)
    up_button.grid(row=1, column=2)
    up_button['command'] = lambda: print("Up button")
    root.bind('<u>', lambda event: print("Up key"))

    down_button = tk.Button(turn_frame, text="Down", height=4, width=8)
    down_button.grid(row=3, column=2)
    down_button['command'] = lambda: print("Down button")
    root.bind('<j>', lambda event: print("Down key"))

    def text_director(inputs):
        textbox.insert('1.0', inputs, 'center')

    sys.stdout.write = text_director  # whenever sys.stdout.write is called, redirector is called.
    root.grid_rowconfigure([1, 2, 3], weight=1)
    root.grid_columnconfigure([1, 2, 3], weight=1)

    root.mainloop()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()