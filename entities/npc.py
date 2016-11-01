"""Define NPC's and their stats"""

import random
import entities.items as items


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

        crusty_bread_qty = random.randint(0, 5)
        potion_qty = random.randint(0, 4)
        hi_potion_qty = random.randint(0, 3)
        x_potion_qty = random.randint(0, 2)

        for i in range(crusty_bread_qty):
            self.inventory.append(items.CrustyBread())

        item_picker = random.randint(0, 10)

        if item_picker > 3:
            for i in range(potion_qty):
                self.inventory.append(items.Potion())

        if item_picker > 6:
            for i in range(hi_potion_qty):
                self.inventory.append(items.HiPotion())

        if item_picker > 9:
            for i in range(x_potion_qty):
                self.inventory.append(items.XPotion())
