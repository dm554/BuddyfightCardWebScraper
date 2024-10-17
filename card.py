class Card:
    card_type = ""

    def __init__(self, name, world, attribute, effect="No effect"):
        self.name = name
        self.effect = effect
        self.world = world
        self.attribute = attribute



class Monster(Card):
    def __init__(self, name, world, size, power, critical, defense, effect, attribute):
        super().__init__(name, world, attribute, effect)
        self.size = size
        self.power = power
        self.defense = defense
        self.critical = critical
        self.card_type = "Monster"


    def __str__(self) -> str:
        return "Name: " + self.name + "\nCard Type: " + self.card_type + "\nWorld: " + self.world + "\nSize: " + self.size + "\nPower: " + self.power + "\nCritical: " + self.critical + "\nDefense: " + self.defense + "\nEffect: " + self.effect


class Spell(Card):
    def __init__(self, name, world, effect, attribute):
        super().__init__(name, world, attribute, effect)
        self.card_type = "Spell"

    def __str__(self) -> str:
        return "Name: " + self.name + "\nCard Type: " + self.card_type + "\nWorld: " + self.world + "\nEffect: " + self.effect


class Impact(Card):
    def __init__(self, name, world, effect, attribute):
        super().__init__(name, world, attribute, effect)
        self.card_type = "Impact"

    def __str__(self) -> str:
        return "Name: " + self.name + "\nCard Type: " + self.card_type + "\nWorld: " + self.world + "\nEffect: " + self.effect


class Item(Card):
    def __init__(self, name, world, power, critical, effect, attribute):
        super().__init__(name, world, attribute, effect)
        self.power = power
        self.critical = critical
        self.card_type = "Item"

    def __str__(self) -> str:
        return "Name: " + self.name + "\nCard Type: " + self.card_type + "\nWorld: " + self.world + "\nPower: " + self.power + "\nCritical: " + self.critical + "\nEffect: " + self.effect



class Flag(Card):
    def __init__(self, name, world, effect):
        super().__init__(name, world, effect)
        self.card_type = "Flag"

    def __str__(self) -> str:
        return "Name: " + self.name + "\nCard Type: " + self.card_type + "\nWorld: " + self.world + "\nEffect: " + self.effect
