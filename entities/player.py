from entities.entity import Entity


class Player(Entity):
    def __init__(self, name):
        super().__init__(name)