
import random
import rosegraphics as rg
import time
import robot_controller as robo
import turtle


class Warrior(object):
    def __init__(self):
        self.lv = 1
        self.exp = 0
        self.str = 9 + self.lv
        self.vit = 9 + self.lv
        self.agi = 9 + self.lv
        self.int = 9 + self.lv
        self.max_hp = self.vit * 10
        self.max_mp = self.int * 2

        self.hp = self.max_hp
        self.mp = self.max_mp
        self.skill_point = 0

        self.x = 10
        self.y = 10
        self.towards = 0
        self.x_range = 0
        self.y_range = 0

    def obtain_exp(self, exp):
        self.exp = self.exp + exp
        print('You get exp: ', exp, 'points!')
        while self.exp > self.lv:
            self.exp = self.exp - self.lv
            self.lv = self.lv + 1
            self.skill_point = self.skill_point + 2
            print('You get upgrade! You get two skill points!')

    def rest(self):
        if self.hp < self.max_hp:
            print('you restore some health!')
            if self.hp + 5 < self.max_hp:
                self.hp = self.hp + 5
            else:
                self.hp = self.max_hp

        if self.mp < self.max_mp:
            print('you restore some mana!')
            if self.hp + 5 < self.max_mp:
                self.mp = self.mp + 5
            else:
                self.mp = self.max_mp

    def get_hurt(self, damage):
        ram = random.randint(0, 100)
        if self.agi - ram < 0:
            if self.agi - ram < 100:
                percent_avoid = (self.agi - ram) / 100
            else:
                percent_avoid = 1
            print('You avoid', percent_avoid * 100, 'percent damage by agi')
        else:
            percent_avoid = 0

        self.hp = self.hp - damage * (1 - percent_avoid)
        if self.hp <= 0:
            print('You are Dead')

    def attack(self):
        damage = self.str
        print('You make', damage, 'points damage')
        return damage

    def distance_attack(self):
        damage = self.int
        self.mp = self.mp - 2
        print('You make', damage, 'points damage by 2 points mp')
        return damage

    def move(self, delta_x, delta_y):
        self.x = self.x + delta_x
        self.y = self.y + delta_y

    def turn(self, degree):
        self.towards = self.towards + degree


class VisualTurtle(object):
    def __init__(self, canvas, turtle_warrior):
        self.running = True
        self.turtle = turtle.RawTurtle(canvas, shape='turtle')
        self.canvas = canvas
        self.warrior = turtle_warrior
        self.x_range = 0
        self.y_range = 0

        self.turtle.speed(self.warrior.agi/2)
        self.turtle.pencolor('black')
        self.turtle.pensize(width=5)
        self.turtle.penup()

    def visual_move(self, distance):
        while self.warrior.x < self.x_range \
                and self.warrior.y < self.y_range:
            if distance > 0:
                self.turtle.forward(distance)
            if distance < 0:
                self.turtle.backward(distance)

    def visual_turn(self, degrees):
        if degrees > 0:
            self.turtle.left(degrees)
        if degrees < 0:
            self.turtle.right(degrees)

    def visual_draw_map(self, robot):
        self.turtle.goto(-470, 190)
        self.turtle.pendown()

        start_x = time.clock()
        while robot.left_motor.state == 'running':
            self.turtle.forward(self.warrior.agi)
            self.x_range = self.x_range + 10
            time.sleep(0.99)
        self.warrior.x_range = (time.clock() - start_x) * self.warrior.agi
        self.turtle.right(90)

        start_y = time.clock()
        while robot.right_motor.state == 'running':
            self.turtle.forward(self.warrior.agi)
            self.y_range = self.y_range + 10
            time.sleep(0.99)
        self.turtle.penup()
        self.warrior.y_range = (time.clock() - start_y) * self.warrior.agi

    def visual_generate_map(self):
        self.x_range = random.randint(47, 94) * 10
        self.y_range = random.randint(19, 38) * 10
        self.canvas.create_rectangle(-470, -190, -470 + self.x_range, -190 + self.y_range)

        self.warrior.x_range = self.x_range
        self.warrior.y_range = self.y_range
        self.turtle.goto(-469.9, 189.9)


class Monster(object):
    def __init__(self, warrior, canvas):
        self.x = random.randint(-470, -470 + warrior.x_range)
        self.y = random.randint(-190, -190 + warrior.y_range)
        self.lv = random.randint(0, 5) + warrior.lv

        random_bonus = random.randint(0, 10)
        self.str = 9 + self.lv + random_bonus
        self.exp = self.lv + random_bonus
        self.hp = self.lv * 6 + random_bonus * 3

        canvas.create_oval(self.x + 2 - random_bonus, self.y + 2 - random_bonus,
                           self.x + 2 + random_bonus, self.y + 2 + random_bonus, fill='black')

    def attack(self):
        damage = self.str
        print('Monster make', damage, 'points damage to you')
        return damage

    def get_hurt(self, damage):
        self.hp = self.hp - damage
        if self.hp <= 0:
            return self.exp
        else:
            print('Monster still have', self.hp, 'points hp')









