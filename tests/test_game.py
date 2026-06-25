import contextlib
import io
import unittest

from src.game import GameState, move_player
from src.pickups import Item, spawn_fruit


def quiet_move(state, dx, dy):
    with contextlib.redirect_stdout(io.StringIO()):
        move_player(state, dx, dy)


class GameTest(unittest.TestCase):
    def test_player_cannot_move_into_wall_without_shovel(self):
        state = GameState()
        state.player.pos_x = 23
        state.player.pos_y = 6

        quiet_move(state, 1, 0)

        self.assertEqual((23, 6), (state.player.pos_x, state.player.pos_y))
        self.assertEqual(0, state.score)
        self.assertEqual(0, state.successful_moves)

    def test_trap_remains_after_triggering(self):
        state = GameState()
        state.player.pos_x = 18
        state.player.pos_y = 5

        quiet_move(state, 1, 0)

        self.assertEqual(-11, state.score)
        self.assertEqual("trap", state.g.get(19, 5).kind)

    def test_key_opens_chest_and_adds_treasure(self):
        state = GameState()
        state.player.pos_x = 15
        state.player.pos_y = 6

        quiet_move(state, 1, 0)
        state.player.pos_x = 21
        state.player.pos_y = 6
        quiet_move(state, 1, 0)

        self.assertNotIn("key", state.inventory)
        self.assertIn("treasure", state.inventory)
        self.assertEqual(98, state.score)
        self.assertEqual(state.g.empty, state.g.get(22, 6))

    def test_spawn_fruit_uses_empty_tile(self):
        state = GameState()
        state.g.set(1, 1, Item("blocking fruit"))
        state.player.pos_x = 2
        state.player.pos_y = 1

        did_spawn = spawn_fruit(state.g)

        self.assertTrue(did_spawn)
        self.assertEqual("blocking fruit", state.g.get(1, 1).name)
        self.assertNotIsInstance(state.g.get(2, 1), Item)
        self.assertEqual("fertile fruit", state.g.get(3, 1).name)
        self.assertFalse(state.g.get(3, 1).required)

    def test_fertile_soil_spawns_after_25_successful_moves(self):
        state = GameState()
        state.g.clear(1, 1)

        for _ in range(12):
            quiet_move(state, 1, 0)
            quiet_move(state, -1, 0)
        quiet_move(state, 1, 0)

        self.assertEqual("fertile fruit", state.g.get(1, 1).name)
        self.assertEqual(25, state.successful_moves)


if __name__ == "__main__":
    unittest.main()
