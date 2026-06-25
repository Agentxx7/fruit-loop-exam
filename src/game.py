from src.grid import Grid
from src.player import Player
from src import pickups


# TODO: flytta denna till en annan fil
class GameState:
    """Samla spelets variabler i en klass."""
    def __init__(self):
        self.player = Player(18, 6)
        self.score = 0
        self.inventory = []

        self.g = Grid()
        self.g.set_player(self.player)
        self.g.make_walls()
        pickups.randomize(self.g)


MOVES = {
    "w": (0, -1),
    "a": (-1, 0),
    "s": (0, 1),
    "d": (1, 0),
}


# TODO: flytta denna till en annan fil
def print_status(game_grid, state):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {state.score} points.")
    print(game_grid)


def print_inventory(state):
    """Visa alla saker som spelaren har plockat upp."""
    if len(state.inventory) == 0:
        print("Inventory is empty.")
    else:
        print("Inventory:")
        for item_name in state.inventory:
            print(f"- {item_name}")


def move_player(state, dx, dy):
    """Flytta spelaren om rutan inte är en vägg."""
    if not state.player.can_move(dx, dy, state.g):
        print("You cannot walk through walls.")
        return

    state.player.move(dx, dy)
    state.score -= 1

    item = state.g.get(state.player.pos_x, state.player.pos_y)
    if isinstance(item, pickups.Item):
        state.score += item.value
        state.inventory.append(item.name)
        print(f"You found a {item.name}, +{item.value} points.")
        state.g.clear(state.player.pos_x, state.player.pos_y)


def start(state):
    command = "a"
    # Loopa tills användaren trycker Q eller X.
    while not command.casefold() in ["q", "x"]:
        print_status(state.g, state)

        command = input("Use WASD to move, I for inventory, Q/X to quit. ")
        command = command.casefold()[:1]

        if command in MOVES:
            dx, dy = MOVES[command]
            move_player(state, dx, dy)
        elif command == "i":
            print_inventory(state)


    # Hit kommer vi när while-loopen slutar
    print("Thank you for playing!")


# __name__ skapas av Python och sätts till "__main__" om man startar game.py
# direkt. Detta är för att undvika att start-funktionen körs om man importerar
# saker från game.py i en annan fil, till exempel vid testning.
if __name__ == "__main__":
    game_state = GameState()
    start(game_state)
