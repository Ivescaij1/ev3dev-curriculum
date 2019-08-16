import tkinter as tk
from tkinter import ttk
import sys
import math
from multiprocessing import Process
import turtle_warrior as tw
import robot_controller as robo
import ev3dev.ev3 as ev3
import mqtt_remote_method_calls as com
import delegates
import time


class DataContainer(object):
    def __init__(self):
        self.running = False
        self.warrior = None
        self.turtle = None
        self.robot = None
        # self.mqtt = MqttConnect()

        self.save = tw.Warrior()
        self.save.state = False

        self.monster = []
        self.monster_attacks = []


class EntryBoxes(object):
    def __init__(self):
        self.x = None
        self.y = None
        self.direction = None
        self.hp = None
        self.mp = None

    def refresh(self, warrior_in_data):
        self.x.delete(0, 'end')
        self.y.delete(0, 'end')
        self.direction.delete(0, 'end')
        self.hp.delete(0, 'end')
        self.mp.delete(0, 'end')
        self.x.insert(0, str(warrior_in_data.x))
        self.y.insert(0, str(warrior_in_data.y))
        self.direction.insert(0, str(warrior_in_data.towards))
        self.hp.insert(0, str(warrior_in_data.hp))
        self.mp.insert(0, str(warrior_in_data.mp))


class MqttConnect(object):
    def __init__(self):
        ev3_delegate = delegates.Ev3Delegate()
        mqtt_client = com.MqttClient(ev3_delegate)
        mqtt_client.connect_to_pc()
        ev3_delegate.loop_forever()
        print("Shutdown complete.")


def main():

    root = tk.Tk()
    root.title("Game Control")

    dc = DataContainer()
    eb = EntryBoxes()
    # dc.robot = robo.Snatch3r()
    main_gui(root, dc, eb)
    menu_bar(root, dc)

    root.mainloop()


def main_gui(root, dc, eb):
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
    eb.x = x_entry
    y_entry = ttk.Entry(position_frame, width=8, justify=tk.CENTER)
    y_entry.grid(row=1, column=3)
    eb.y = y_entry

    # grid(1,2): character button, map button, start button
    # 3 column, 1 row used, with space between buttons and perimeter [row 0 & 2, column 0 & 2 & 4 & 6] expandable.
    start_frame = tk.Frame(root, bg='black')
    start_frame.grid(row=1, column=2, sticky='nsew')
    start_frame.grid_rowconfigure([0, 2], weight=1)
    start_frame.grid_columnconfigure([0, 2, 4, 6], weight=1)

    map_button = ttk.Button(start_frame, text="Map <M>", width=12)
    map_button.grid(row=1, column=1)
    map_button['command'] = lambda: handle_map_button(dc)
    root.bind('<m>', lambda event: handle_map_button(dc))

    start_button = ttk.Button(start_frame, text="Start <Enter>", width=12)
    start_button.grid(row=1, column=3)
    start_button['command'] = lambda: handle_start_button(canvas, dc)
    root.bind('<Return>', lambda event: handle_start_button(canvas, dc))

    character_button = ttk.Button(start_frame, text="Character <P>", width=12)
    character_button.grid(row=1, column=5)
    character_button['command'] = lambda: pop_up(dc)
    root.bind('<p>', lambda event: pop_up(dc))

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
    eb.direction = direction_entry

    # grid(2, 1) left move control, free grid around perimeter and between 'move' and direction button
    # * have row0 reserved even if not expandable
    move_frame = tk.Frame(root, bg='orange red')
    move_frame.grid(row=2, column=1, sticky='nsew')
    move_frame.grid_rowconfigure([2, 6], weight=1)
    move_frame.grid_columnconfigure([0, 4], weight=1)

    move_button = tk.Button(move_frame, text="Move", height=2, width=8)
    move_button.grid(row=1, column=2)
    move_button['command'] = lambda: handle_move_button(dc, eb)

    w_button = tk.Button(move_frame, text="W", height=4, width=8)
    w_button.grid(row=3, column=2)
    w_button['command'] = lambda: handle_forward_button(dc)
    root.bind('<w>', lambda event: handle_forward_button(dc))

    a_button = tk.Button(move_frame, text="A", height=4, width=8)
    a_button.grid(row=4, column=1)
    a_button['command'] = lambda: handle_left_button(dc)
    root.bind('<a>', lambda event: handle_left_button(dc))

    stop_button = tk.Button(move_frame, text="Stop", height=4, width=8)
    stop_button.grid(row=4, column=2)
    stop_button['command'] = lambda: handle_stop_button(dc)
    root.bind('<space>', lambda event: handle_stop_button(dc))

    d_button = tk.Button(move_frame, text="D", height=4, width=8)
    d_button.grid(row=4, column=3)
    d_button['command'] = lambda: handle_right_button(dc)
    root.bind('<d>', lambda event: handle_right_button(dc))

    s_button = tk.Button(move_frame, text="S", height=4, width=8)
    s_button.grid(row=5, column=2)
    s_button['command'] = lambda: handle_backward_button(dc)
    root.bind('<s>', lambda event: handle_backward_button(dc))

    # grid(2, 3) Right action control

    action_frame = tk.Frame(root, bg='dodger blue')
    action_frame.grid(row=2, column=3, sticky='nsew')
    action_frame.grid_rowconfigure([2, 4, 6, 8], weight=1)
    action_frame.grid_columnconfigure([0, 4], weight=1)

    turn_button = tk.Button(action_frame, text="Turn", height=2, width=8)
    turn_button.grid(row=1, column=2)
    turn_button['command'] = lambda: handle_turn_button(dc, eb)

    att_button = tk.Button(action_frame, text="Attack \n<J>", height=4, width=8)
    att_button.grid(row=3, column=2)
    att_button['command'] = lambda: handle_attack_button(dc)
    root.bind('<j>', lambda event: handle_attack_button(dc))

    skill_button = tk.Button(action_frame, text="Fire Ball \n<K>", height=4, width=8)
    skill_button.grid(row=5, column=2)
    skill_button['command'] = lambda: handle_d_attack_button(dc)
    root.bind('<k>', lambda event: handle_d_attack_button(dc))

    rest_button = tk.Button(action_frame, text="Rest \n<L>", height=4, width=8)
    rest_button.grid(row=7, column=2)
    rest_button['command'] = lambda: handle_rest_button(dc)
    root.bind('<l>', lambda event: handle_rest_button(dc))

    # grid (3, 1) hp/mp & exit display frame
    exit_frame = tk.Frame(root, bg='orange red')
    exit_frame.grid(row=3, column=1, sticky='nsew')
    exit_frame.grid_rowconfigure([0, 2, 4], weight=1)
    exit_frame.grid_columnconfigure([1, 4], weight=1)

    hp_label = tk.Label(exit_frame, text="HP", bg='orange red')
    hp_label.grid(row=1, column=2)
    hp_box = ttk.Entry(exit_frame, width=8, justify=tk.CENTER)
    hp_box.grid(row=1, column=3)
    eb.hp = hp_box

    mp_label = tk.Label(exit_frame, text="MP", bg='orange red')
    mp_label.grid(row=3, column=2)
    mp_box = ttk.Entry(exit_frame, width=8, justify=tk.CENTER)
    mp_box.grid(row=3, column=3)
    eb.mp = mp_box

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
    left_button['command'] = lambda: handle_left_turn(dc)
    root.bind('<q>', lambda event: handle_left_turn(dc))

    right_button = tk.Button(turn_frame, text="Right <E>", height=4, width=8)
    right_button.grid(row=2, column=3)
    right_button['command'] = lambda: handle_right_turn(dc)
    root.bind('<e>', lambda event: handle_right_turn(dc))

    up_button = tk.Button(turn_frame, text="Up", height=4, width=8)
    up_button.grid(row=1, column=2)
    up_button['command'] = lambda: print("Up button")
    root.bind('<u>', lambda event: print("Up key"))

    down_button = tk.Button(turn_frame, text="Down", height=4, width=8)
    down_button.grid(row=3, column=2)
    down_button['command'] = lambda: print("Down button")
    root.bind('<i>', lambda event: print("Down key"))

    # grid(3,2): Text display frame with tkinter text widget, free grid around perimeter.
    # 1 character width = 15 pixel with 24 font
    text_frame = tk.Frame(root, bg='black')
    text_frame.grid(row=3, column=2, sticky='nsew')
    text_frame.grid_rowconfigure([0, 2], weight=1)
    text_frame.grid_columnconfigure([0, 2], weight=1)

    textbox = tk.Text(text_frame, width=64, height=7, font=('Comic Sans MS', 24, 'bold'), background='lightgray')
    textbox.grid(row=1, column=1)
    textbox.tag_configure("center", justify='center')

    # grid(2, 2) Canvas display frame with tkinter canvas, free grid around perimeter.
    canvas_frame = tk.Frame(root, bg='black')
    canvas_frame.grid(row=2, column=2, sticky='nsew')
    canvas_frame.grid_rowconfigure([0, 2], weight=1)
    canvas_frame.grid_columnconfigure([0, 2], weight=1)

    canvas = tk.Canvas(canvas_frame, width=960, height=400)
    canvas.grid(row=1, column=1)

    # root configuation below
    def text_director(inputs):
        textbox.insert('1.0', inputs, 'center')

    root.grid_rowconfigure([1, 2, 3], weight=1)
    root.grid_columnconfigure([1, 2, 3], weight=1)
    sys.stdout.write = text_director

    # button functions below this point
    def handle_start_button(window, data):
        print("Start")
        if not data.running:
            data.warrior = tw.Warrior()
            data.turtle = tw.VisualTurtle(window, data.warrior)
            data.running = True
        else:
            if not ev3.LargeMotor(ev3.OUTPUT_B).connected:
                if len(dc.monster) < 50:
                    for _ in range(5):
                        new_monster = tw.Monster(data.warrior, window)
                        new_monster.draw()
                        data.monster.append(new_monster)
                        print(str(new_monster.x)+' , '+str(new_monster.y))
                else:
                    print('You have TOO MANY monsters')

            else:
                color = data.robot.send_color()
                if color != "White":
                    new_monster = tw.Monster(data.warrior, window)
                    new_monster.x = data.warrior.x + 10 * math.cos(data.warrior.towards)
                    new_monster.y = data.warrior.y + 10 * math.sin(data.warrior.towards)
                    new_monster.draw()
                    data.Monster = data.Monster + [new_monster]
            print('Notice: Bigger == Stronger')

    def handle_map_button(data):
        print("Map")
        if data.running:
            if data.mqtt:
                data.turtle.draw_map()

                data.mqtt.send_message('draw_map')
                data.robot.left_motor.waitwhile(state='running')
                data.mqtt.send_message('turn_degrees', [90, 900])
                data.mqtt.send_message('draw_map')
                data.robot.left_motor.waitwhile(state='running')

            elif ev3.LargeMotor(ev3.OUTPUT_B).connected:
                data.turtle.draw_map(data.robot)
            else:
                data.turtle.generate_map()
        else:
            print('Press Start to start,\n'
                  'Then press map to generate map, \n'
                  'Press Start again to generate monsters')

    def handle_move_button(data, entry_boxes):
        print("Button Move")
        x = int(entry_boxes.x.get())
        y = int(entry_boxes.y.get())
        data.warrior.x = x
        data.warrior.y = y
        data.turtle.move_to(x, y)

    def handle_forward_button(data):
        print("Forward button")
        data.turtle.move(data.warrior.agi)
        data.warrior.x = data.warrior.x + data.warrior.agi * math.cos(data.warrior.towards * math.pi / 180)
        data.warrior.y = data.warrior.y - data.warrior.agi * math.sin(data.warrior.towards * math.pi / 180)
        eb.refresh(data.warrior)
        # check_distance(data)

    def handle_backward_button(data):
        print("Back button")
        data.turtle.move(-data.warrior.agi)
        data.warrior.x = data.warrior.x - data.warrior.agi * math.cos(data.warrior.towards * math.pi / 180)
        data.warrior.y = data.warrior.y + data.warrior.agi * math.sin(data.warrior.towards * math.pi / 180)
        eb.refresh(data.warrior)
        # check_distance(data)

    def handle_left_button(data):
        print("Left button")
        data.warrior.x = data.warrior.x - data.warrior.agi * math.sin(data.warrior.towards * math.pi / 180)
        data.warrior.y = data.warrior.y - data.warrior.agi * math.cos(data.warrior.towards * math.pi / 180)
        data.turtle.move_to(data.warrior.x, data.warrior.y)
        eb.refresh(data.warrior)
        # check_distance(data)

    def handle_right_button(data):
        print("Right button")
        data.warrior.x = data.warrior.x + data.warrior.agi * math.sin(data.warrior.towards * math.pi / 180)
        data.warrior.y = data.warrior.y + data.warrior.agi * math.cos(data.warrior.towards * math.pi / 180)
        data.turtle.move_to(data.warrior.x, data.warrior.y)
        eb.refresh(data.warrior)
        # check_distance(data)

    def handle_stop_button(data):
        print('Space')
        data.turtle.move_to(data.warrior.x, data.warrior.y)
        eb.refresh(data.warrior)
        # check_distance(data)

    def handle_turn_button(data, entry_boxes):
        print("Turn button")
        degree = int(entry_boxes.direction.get())
        data.warrior.towards = degree % 360
        data.turtle.turn(degree)

    def handle_left_turn(data):
        print('Turn left')
        data.turtle.turn(10)
        data.warrior.towards = (data.warrior.towards + 10) % 360
        eb.refresh(data.warrior)

    def handle_right_turn(data):
        print('Turn left')
        data.turtle.turn(-10)
        data.warrior.towards = (data.warrior.towards - 10) % 360
        eb.refresh(data.warrior)

    def handle_attack_button(data):
        print('Attack')
        for i in range(len(data.monster)):
            distance = math.sqrt((data.warrior.x - data.monster[i].x) ** 2 +
                                 (data.warrior.y - data.monster[i].y) ** 2)
            if distance <= 50:
                monster_attack = data.monster[i].attack()
                data.warrior.get_hurt(monster_attack)
        for j in range(len(data.monster)):
            distance = math.sqrt((data.warrior.x - data.monster[j].x) ** 2 +
                                 (data.warrior.y - data.monster[j].y) ** 2)
            angle = data.warrior.towards - math.atan((data.monster[j].y - data.warrior.y)/(data.monster[j].x - data.warrior.x)) / math.pi * 180
            if distance <= 20:
                if -60 <= angle <= 60:
                    damage = data.warrior.attack()
                    exp = data.monster[j].get_hurt(damage)
                    data.warrior.obtain_exp(exp)
                    if exp > 0:
                        data.monster.remove(data.monster[j])
                        break
        eb.refresh(data.warrior)

    def handle_d_attack_button(data):
        print('D_Attack')
        for i in range(len(data.monster)):
            distance = math.sqrt((data.warrior.x - data.monster[i].x) ** 2 +
                                 (data.warrior.y - data.monster[i].y) ** 2)
            if distance <= 50:
                monster_attack = data.monster[i].attack() * 0.5
                data.warrior.get_hurt(monster_attack)
        for j in range(len(data.monster)):
            distance = math.sqrt((data.warrior.x - data.monster[j].x) ** 2 +
                                 (data.warrior.y - data.monster[j].y) ** 2)
            angle = data.warrior.towards - math.atan((data.monster[j].y - data.warrior.y)/(data.monster[j].x - data.warrior.x)) / math.pi * 180
            if distance <= 50:
                if -30 <= angle <= 30:
                    damage = data.warrior.distance_attack()
                    exp = data.monster[j].get_hurt(damage)
                    data.warrior.obtain_exp(exp)
                    if exp > 0:
                        data.monster.remove(data.monster[j])
                        break
        eb.refresh(data.warrior)

    def handle_rest_button(data):
        print("rest")
        data.warrior.rest()
        eb.refresh(data.warrior)


def menu_bar(root, dc):
    root.option_add('*tearOff', False)
    menubar = tk.Menu(root)
    root['menu'] = menubar

    main_menu = tk.Menu(menubar)
    menubar.add_cascade(menu=main_menu, label='Menu')

    main_menu.add_command(label='Save',
                          command=lambda: save())
    main_menu.add_command(label='Load',
                          command=lambda: load())
    main_menu.add_command(label='Exit',
                          command=lambda: exit())

    game_menu = tk.Menu(menubar)
    menubar.add_cascade(menu=game_menu, label='Game')
    game_menu.add_command(label='Character',
                          command=lambda: pop_up(dc))

    def save():
        print('MenuSave')
        dc.save.lv = dc.warrior.lv
        dc.save.exp = dc.warrior.exp
        dc.save.str = dc.warrior.exp
        dc.save.vit = dc.warrior.vit
        dc.save.agi = dc.warrior.agi
        dc.save.int = dc.warrior.int
        dc.save.max_hp = dc.warrior.max_hp
        dc.save.max_mp = dc.warrior.max_mp

        dc.save.hp = dc.warrior.hp
        dc.save.mp = dc.warrior.mp
        dc.save.skill_point = dc.warrior.skill_point

        dc.save.x = dc.warrior.x
        dc.save.y = dc.warrior.y
        dc.save.towards = dc.warrior.towards
        dc.save.x_range = dc.warrior.x_range
        dc.save.y_range = dc.warrior.y_range

        dc.save.state = True

    def load():
        print('MenuLoad')
        if dc.save.state:
            dc.warrior.lv = dc.save.lv
            dc.warrior.exp = dc.save.exp
            dc.warrior.str = dc.save.str
            dc.warrior.vit = dc.save.vit
            dc.warrior.agi = dc.save.agi
            dc.warrior.int = dc.save.int
            dc.warrior.max_hp = dc.save.max_hp
            dc.warrior.max_mp = dc.save.max_mp

            dc.warrior.hp = dc.save.hp
            dc.warrior.mp = dc.save.mp
            dc.warrior.skill_point = dc.save.skill_point

            dc.warrior.x = dc.save.x
            dc.warrior.y = dc.save.y
            dc.warrior.towards = dc.save.towards
            dc.warrior.x_range = dc.save.x_range
            dc.warrior.y_range = dc.save.y_range
        else:
            print('No Record Found')


def pop_up(data):
    window = tk.Toplevel()
    window.grid_rowconfigure([0, 4, 6, 8, 10], weight=1)
    window.grid_columnconfigure([0, 4, 6, 10], weight=1)
    new_nums = [data.warrior.skill_point,
                data.warrior.max_hp, data.warrior.str, data.warrior.vit,
                data.warrior.max_mp, data.warrior.int, data.warrior.agi]

    sp_box = tk.Entry(window, width=4, justify=tk.CENTER)
    sp_box.grid(row=2, column=5)
    sp_box.insert(0, new_nums[0])
    sp_label = tk.Label(window, text='Available skill points')
    sp_label.grid(row=1, column=5)

    hp_label = tk.Label(window, text='HP')
    hp_label.grid(row=3, column=1)
    hp_box = tk.Entry(window, width=4, justify=tk.CENTER)
    hp_box.grid(row=3, column=2)
    hp_box.insert(0, new_nums[1])
    hp_button = tk.Button(window, text="+hp", height=1, width=4)
    hp_button.grid(row=3, column=3)
    hp_button['command'] = lambda: handle_hp_button()

    str_label = tk.Label(window, text='Strength')
    str_label.grid(row=5, column=1)
    str_box = tk.Entry(window, width=4, justify=tk.CENTER)
    str_box.grid(row=5, column=2)
    str_box.insert(0, new_nums[2])
    str_button = tk.Button(window, text="+str", height=1, width=4)
    str_button.grid(row=5, column=3)
    str_button['command'] = lambda: handle_str_button()

    vit_label = tk.Label(window, text='Vitality')
    vit_label.grid(row=7, column=1)
    vit_box = tk.Entry(window, width=4, justify=tk.CENTER)
    vit_box.grid(row=7, column=2)
    vit_box.insert(0, new_nums[3])
    vit_button = tk.Button(window, text="+vit", height=1, width=4)
    vit_button.grid(row=7, column=3)
    vit_button['command'] = lambda: handle_vit_button()

    mp_label = tk.Label(window, text='MP')
    mp_label.grid(row=3, column=7)
    mp_box = tk.Entry(window, width=4, justify=tk.CENTER)
    mp_box.grid(row=3, column=8)
    mp_box.insert(0, new_nums[4])
    mp_button = tk.Button(window, text="+mp", height=1, width=4)
    mp_button.grid(row=3, column=9)
    mp_button['command'] = lambda: handle_mp_button()

    int_label = tk.Label(window, text='Intelligence')
    int_label.grid(row=5, column=7)
    int_box = tk.Entry(window, width=4, justify=tk.CENTER)
    int_box.grid(row=5, column=8)
    int_box.insert(0, new_nums[5])
    int_button = tk.Button(window, text="+int", height=1, width=4)
    int_button.grid(row=5, column=9)
    int_button['command'] = lambda: handle_int_button()

    agi_label = tk.Label(window, text='Agility')
    agi_label.grid(row=7, column=7)
    agi_box = tk.Entry(window, width=4, justify=tk.CENTER)
    agi_box.grid(row=7, column=8)
    agi_box.insert(0, new_nums[6])
    agi_button = tk.Button(window, text="+agi", height=1, width=4)
    agi_button.grid(row=7, column=9)
    agi_button['command'] = lambda: handle_agi_button()

    confirm = tk.Button(window, text="Confirm\n<Enter>", height=2, width=8)
    confirm.grid(row=9, column=4)
    confirm['command'] = lambda: handle_confirm_button()
    window.bind('<Return>', lambda event: handle_confirm_button())

    window_destroy = tk.Button(window, text="Exit\n<P>", height=2, width=8)
    window_destroy.grid(row=9, column=6)
    window_destroy['command'] = lambda: window.destroy()
    window.bind('<p>', lambda event: window.destroy())

    def handle_confirm_button():
        data.warrior.skill_point = new_nums[0]
        data.warrior.max_hp = new_nums[1]
        data.warrior.str = new_nums[2]
        data.warrior.vit = new_nums[3]
        data.warrior.max_mp = new_nums[4]
        data.warrior.int = new_nums[5]
        data.warrior.agi = new_nums[6]

        data.warrior.hp = data.warrior.max_hp
        data.warrior.mp = data.warrior.max_mp

    def handle_hp_button():
        if new_nums[0] > 0:
            new_nums[0] = new_nums[0] - 1
            sp_box.delete(0, 'end')
            sp_box.insert(0, new_nums[0])
            new_nums[1] = new_nums[1] + 10
            hp_box.delete(0, 'end')
            hp_box.insert(0, new_nums[1])

    def handle_str_button():
        if new_nums[0] > 0:
            new_nums[0] = new_nums[0] - 1
            sp_box.delete(0, 'end')
            sp_box.insert(0, new_nums[0])
            new_nums[2] = new_nums[2] + 1
            str_box.delete(0, 'end')
            str_box.insert(0, new_nums[2])

    def handle_vit_button():
        if new_nums[0] > 0:
            new_nums[0] = new_nums[0] - 1
            sp_box.delete(0, 'end')
            sp_box.insert(0, new_nums[0])
            new_nums[3] = new_nums[3] + 1
            vit_box.delete(0, 'end')
            vit_box.insert(0, new_nums[3])

    def handle_mp_button():
        if new_nums[0] > 0:
            new_nums[0] = new_nums[0] - 1
            sp_box.delete(0, 'end')
            sp_box.insert(0, new_nums[0])
            new_nums[4] = new_nums[4] + 10
            mp_box.delete(0, 'end')
            mp_box.insert(0, new_nums[4])

    def handle_int_button():
        if new_nums[0] > 0:
            new_nums[0] = new_nums[0] - 1
            sp_box.delete(0, 'end')
            sp_box.insert(0, new_nums[0])
            new_nums[5] = new_nums[5] + 1
            int_box.delete(0, 'end')
            int_box.insert(0, new_nums[5])

    def handle_agi_button():
        if new_nums[0] > 0:
            new_nums[0] = new_nums[0] - 1
            sp_box.delete(0, 'end')
            sp_box.insert(0, new_nums[0])
            new_nums[6] = new_nums[6] + 1
            agi_box.delete(0, 'end')
            agi_box.insert(0, new_nums[6])





# def check_distance(data_container):
#     for i in range(len(data_container.monster_attacks)):
#         data_container.monster_attacks[i].terminate()
#         data_container.monster_attacks[i].join()
#     for j in range(len(data_container.monster)):
#         distance = math.sqrt((data_container.warrior.x - data_container.monster[j].x) ** 2 +
#                              (data_container.warrior.y - data_container.monster[j].y) ** 2)
#         if distance <= 20:
#             attack_process = tw.MonsterAttack(data_container.monster[j], data_container.warrior)
#             attack_process.start()
#             data_container.monster_attacks.append(attack_process)

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()