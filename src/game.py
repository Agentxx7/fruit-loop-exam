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
        self.remaining_collectibles = pickups.count_required_collectibles()
        self.successful_moves = 0
        self.is_running = True

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
    target_x = state.player.pos_x + dx
    target_y = state.player.pos_y + dy

    if not state.player.can_move(dx, dy, state.g):
        if "shovel" in state.inventory and not state.g.is_border_position(target_x, target_y):
            state.inventory.remove("shovel")
            state.g.clear(target_x, target_y)
            print("You used a shovel to dig through the wall.")
        else:
            print("You cannot walk through walls.")
            return

    state.player.move(dx, dy)
    state.score -= 1
    handle_tile(state)
    count_successful_move(state)


def collect_item(state, item):
    state.score += item.value
    state.inventory.append(item.name)
    if item.required:
        state.remaining_collectibles -= 1
    print(f"You found a {item.name}, +{item.value} points.")
    state.g.clear(state.player.pos_x, state.player.pos_y)


def count_successful_move(state):
    state.successful_moves += 1
    if state.is_running and state.successful_moves % 25 == 0:
        if pickups.spawn_fruit(state.g):
            print("A new fruit grows from the fertile soil.")


def handle_tile(state):
    """Hantera det som finns på spelarens ruta."""
    item = state.g.get(state.player.pos_x, state.player.pos_y)
    if not isinstance(item, pickups.Item):
        return

    if item.kind == "trap":
        state.score += item.value
        print("You stepped on a trap, -10 points.")
    elif item.kind == "key":
        state.inventory.append("key")
        state.remaining_collectibles -= 1
        print("You found a key.")
        state.g.clear(state.player.pos_x, state.player.pos_y)
    elif item.kind == "shovel":
        state.inventory.append("shovel")
        state.remaining_collectibles -= 1
        print("You found a shovel.")
        state.g.clear(state.player.pos_x, state.player.pos_y)
    elif item.kind == "chest":
        if "key" in state.inventory:
            state.inventory.remove("key")
            state.inventory.append("treasure")
            state.score += item.value
            state.remaining_collectibles -= 1
            print("You opened the chest and found treasure, +100 points.")
            state.g.clear(state.player.pos_x, state.player.pos_y)
        else:
            print("The chest is locked. You need a key.")
    elif item.kind == "exit":
        if state.remaining_collectibles == 0:
            print("You collected everything and escaped. You win!")
            state.is_running = False
        else:
            print("You need to collect everything before leaving.")
    else:
        collect_item(state, item)


def start(state):
    command = "a"
    # Loopa tills användaren trycker Q eller X.
    while state.is_running and not command.casefold() in ["q", "x"]:
        print_status(state.g, state)

        command = input("Use WASD to move, I for inventory, Q/X to quit. ")
        command = command.casefold()[:1]

        if command in MOVES:
            dx, dy = MOVES[command]
            move_player(state, dx, dy)
        elif command == "i":
            print_inventory(state)


    # Hit kommer vi när while-loopen slutar
    if command.casefold() in ["q", "x"]:
        print("Thank you for playing!")
    else:
        print("Game over.")


# __name__ skapas av Python och sätts till "__main__" om man startar game.py
# direkt. Detta är för att undvika att start-funktionen körs om man importerar
# saker från game.py i en annan fil, till exempel vid testning.
if __name__ == "__main__":
    game_state = GameState()
    start(game_state)
