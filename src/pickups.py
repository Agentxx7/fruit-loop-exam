
class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=20, symbol="?", kind="fruit"):
        self.name = name
        self.value = value
        self.symbol = symbol
        self.kind = kind

    def __str__(self):
        return self.symbol


placed_items = [
    (21, 1, Item("carrot")),
    (8, 2, Item("apple")),
    (32, 3, Item("strawberry")),
    (9, 4, Item("cherry")),
    (6, 6, Item("watermelon")),
    (12, 6, Item("radish")),
    (7, 9, Item("cucumber")),
    (22, 10, Item("meatball")),
    (19, 5, Item("trap", value=-10, symbol="T", kind="trap")),
    (20, 6, Item("shovel", value=0, symbol="S", kind="shovel")),
    (16, 6, Item("key", value=0, symbol="K", kind="key")),
    (22, 6, Item("chest", value=100, symbol="C", kind="chest")),
    (33, 10, Item("exit", value=0, symbol="E", kind="exit")),
]


def randomize(grid):
    for x, y, item in placed_items:
        if grid.is_empty(x, y) and not grid.is_player_position(x, y):
            grid.set(x, y, item)


def count_required_collectibles():
    total = 0
    for x, y, item in placed_items:
        if item.kind not in ["trap", "exit"]:
            total += 1
    return total
