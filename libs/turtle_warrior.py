
import random


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

        self.x = 0
        self.y = 0
        self.towards = 0

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


class Monster(object):
    def __init__(self, x, y, lv):
        self.x = x
        self.y = y
        self.lv = lv

        random_bonus = random.randint(0, self.lv)
        self.str = 10 + random_bonus
        self.exp = self.lv + random_bonus
        self.hp = self.lv * 6 + random_bonus * 3

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