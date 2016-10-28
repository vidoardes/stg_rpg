class Weapon:
    def __init__(self):
        raise NotImplementedError("Not a real Weapon!")
        
    def __str__(self):
        return self.name


class Rock(Weapon):
    def __init__(self):
        self.name = "Rock"
        self.description = "A fist-sized rock, suitable for bludgeoning."
        self.damage = 5
        self.value = 1


class Dagger(Weapon):
    def __init__(self):
        self.name = "Dagger"
        self.description = "A small dagger with some rust. " \
            "Somewhat more dangerous than a rock."
        self.damage = 10
        self.value= 20


class RustySword(Weapon):
    def __init__(self):
        self.name = "Rusty sword"
        self.description = "This sword is showing its age, " \
            "but still has some fight in it."
        self.damage = 20
        value = 100
