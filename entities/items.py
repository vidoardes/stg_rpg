class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")

    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)


class CrustyBread(Consumable):
    def __init__(self):
        self.name = "Crusty Bread"
        self.healing_value = 10
        self.value = 12


class Potion(Consumable):
    def __init__(self):
        self.name = "Potion"
        self.healing_value = 25
        self.value = 20


class HiPotion(Consumable):
    def __init__(self):
        self.name = "Hi-Potion"
        self.healing_value = 50
        self.value = 30


class XPotion(Consumable):
    def __init__(self):
        self.name = "X-Potion"
        self.healing_value = 75
        self.value = 50
