"""Create enemy entity and define stats"""

import random
import decimal


class Enemy:
    def __init__(self):
        self.name = ""
        self.hp = 0
        self.damage = 0
        self.loot = 0
        raise NotImplementedError("Do not create raw Enemy objects.")

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0

    def randomise_stats(self, stat):
        hp_modifier = random.randrange(-50, 50) / 100
        return decimal.Decimal(round(hp_modifier * stat, 0) + stat)


class GiantSpider(Enemy):
    def __init__(self):
        self.name = "Giant Spider"
        self.hp = 10
        self.damage = 2
        self.loot = 2


class Ogre(Enemy):
    def __init__(self):
        self.name = "Ogre"
        self.hp = 30
        self.damage = 10
        self.loot = 8


class BatColony(Enemy):
    def __init__(self):
        self.name = "Colony of bats"
        self.hp = 100
        self.damage = 4
        self.loot = 10


class RockMonster(Enemy):
    def __init__(self):
        self.name = "Rock Monster"
        self.hp = 80
        self.damage = 15
        self.loot = 20
