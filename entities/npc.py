"""Define NPC's and their stats"""

import random

import entities.items as items
import entities.weapons as weapons


class NonPlayableCharacter():
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects")

    def __str__(self):
        return self.name


class Trader(NonPlayableCharacter):
    def __init__(self):
        self.name = "Trader"
        self.gold = random.randint(70, 150)

        self.inventory = []

        crusty_bread_qty = random.randint(1, 4)
        potion_qty = random.randint(1, 3)
        hi_potion_qty = random.randint(1, 2)

        for i in range(crusty_bread_qty):
            self.inventory.append(items.CrustyBread())

        item_picker = random.randint(1, 10)

        if item_picker > 3:
            for i in range(potion_qty):
                self.inventory.append(items.Potion())

        if item_picker > 5:
            for i in range(hi_potion_qty):
                self.inventory.append(items.HiPotion())

        if item_picker > 8:
            self.inventory.append(items.XPotion())

        if item_picker == 10:
            self.inventory.append(weapons.RustySword())
