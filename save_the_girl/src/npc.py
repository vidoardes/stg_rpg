"""Define NPC's and their stats"""

import random

import src.items as items
import src.weapons as weapons


class NonPlayableCharacter():
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects")

    def __str__(self):
        return self.name


class Trader(NonPlayableCharacter):
    def __init__(self):
        self.name = "Trader"
        self.gold = random.randint(70, 150)

        self.inventory = {"Weapons": {}, "Items": {}}

        crusty_bread_qty = random.randint(1, 4)
        potion_qty = random.randint(1, 3)
        hi_potion_qty = random.randint(1, 2)

        self.inventory["Items"]["Crusty Bread"] = {}
        self.inventory["Items"]["Crusty Bread"]["obj"] = items.CrustyBread()
        self.inventory["Items"]["Crusty Bread"]["qty"] = crusty_bread_qty

        item_picker = random.randint(1, 10)

        if item_picker > 3:
            self.inventory["Items"]["Potion"] = {}
            self.inventory["Items"]["Potion"]["obj"] = items.Potion()
            self.inventory["Items"]["Potion"]["qty"] = potion_qty

        if item_picker > 5:
            self.inventory["Items"]["Hi-Potion"] = {}
            self.inventory["Items"]["Hi-Potion"]["obj"] = items.HiPotion()
            self.inventory["Items"]["Hi-Potion"]["qty"] = hi_potion_qty

        if item_picker > 8:
            self.inventory["Items"]["X-Potion"] = {}
            self.inventory["Items"]["X-Potion"]["obj"] = items.XPotion()
            self.inventory["Items"]["X-Potion"]["qty"] = 1

        if item_picker == 10:
            self.inventory["Weapons"]["Rusty sword"] = {}
            self.inventory["Weapons"]["Rusty sword"]["obj"] = weapons.RustySword()
            self.inventory["Weapons"]["Rusty sword"]["qty"] = 1
