import unittest

from models import game_logic_normale as gln


class GameLogicNormaleTests(unittest.TestCase):
    def test_victory_team1_row(self):
        grid = {
            (0, 0): {"team_id": 1, "morpion_id": 10},
            (0, 1): {"team_id": 1, "morpion_id": 11},
            (0, 2): {"team_id": 1, "morpion_id": 12},
        }
        result = gln.check_game_end_conditions(
            grid=grid,
            grid_size=3,
            current_turn=5,
            max_turns=20,
            team1_id=1,
            team2_id=2,
        )
        self.assertTrue(result["game_over"])
        self.assertEqual(result["winner_team_id"], 1)
        self.assertEqual(result["reason"], "victory")

    def test_victory_team2_diagonal_on_four_by_four(self):
        grid = {
            (0, 3): {"team_id": 20, "morpion_id": 101},
            (1, 2): {"team_id": 20, "morpion_id": 102},
            (2, 1): {"team_id": 20, "morpion_id": 103},
            (3, 0): {"team_id": 20, "morpion_id": 104},
        }
        result = gln.check_game_end_conditions(
            grid=grid,
            grid_size=4,
            current_turn=9,
            max_turns=30,
            team1_id=10,
            team2_id=20,
        )
        self.assertTrue(result["game_over"])
        self.assertEqual(result["winner_team_id"], 20)
        self.assertEqual(result["reason"], "victory")

    def test_victory_team1_column_on_four_by_four(self):
        grid = {
            (0, 1): {"team_id": 7, "morpion_id": 1},
            (1, 1): {"team_id": 7, "morpion_id": 2},
            (2, 1): {"team_id": 7, "morpion_id": 3},
            (3, 1): {"team_id": 7, "morpion_id": 4},
        }
        result = gln.check_game_end_conditions(
            grid=grid,
            grid_size=4,
            current_turn=9,
            max_turns=25,
            team1_id=7,
            team2_id=8,
        )
        self.assertTrue(result["game_over"])
        self.assertEqual(result["winner_team_id"], 7)
        self.assertEqual(result["reason"], "victory")

    def test_grid_full_draw(self):
        pattern = [
            [1, 2, 1],
            [2, 1, 2],
            [2, 1, 2],
        ]
        grid = {}
        idx = 0
        for row in range(3):
            for col in range(3):
                grid[(row, col)] = {"team_id": pattern[row][col], "morpion_id": idx}
                idx += 1

        result = gln.check_game_end_conditions(
            grid=grid,
            grid_size=3,
            current_turn=15,
            max_turns=20,
            team1_id=1,
            team2_id=2,
        )
        self.assertTrue(result["game_over"])
        self.assertIsNone(result["winner_team_id"])
        self.assertEqual(result["reason"], "grid_full")

    def test_max_turns_trigger(self):
        result = gln.check_game_end_conditions(
            grid={},
            grid_size=3,
            current_turn=51,
            max_turns=50,
            team1_id=1,
            team2_id=2,
        )
        self.assertTrue(result["game_over"])
        self.assertIsNone(result["winner_team_id"])
        self.assertEqual(result["reason"], "max_turns")

    def test_exact_max_turns_does_not_trigger_draw(self):
        result = gln.check_game_end_conditions(
            grid={(0, 0): {"team_id": 1, "morpion_id": 1}},
            grid_size=3,
            current_turn=30,
            max_turns=30,
            team1_id=1,
            team2_id=2,
        )
        self.assertFalse(result["game_over"])
        self.assertIsNone(result["winner_team_id"])
        self.assertIsNone(result["reason"])

    def test_no_morpions_available_for_both_teams(self):
        team1 = [{"id_morpion": mid} for mid in (1, 2)]
        team2 = [{"id_morpion": mid} for mid in (3, 4)]
        used = [1, 2, 3, 4]
        result = gln.check_game_end_conditions(
            grid={},
            grid_size=4,
            current_turn=12,
            max_turns=30,
            team1_id=1,
            team2_id=2,
            team1_morpions=team1,
            team2_morpions=team2,
            used_morpions=used,
        )
        self.assertTrue(result["game_over"])
        self.assertIsNone(result["winner_team_id"])
        self.assertEqual(result["reason"], "no_morpions")

    def test_game_continues_when_reserves_exist(self):
        team1 = [{"id_morpion": 1}, {"id_morpion": 2}]
        team2 = [{"id_morpion": 3}, {"id_morpion": 4}]
        used = [1, 3]  # ambos equipos aún tienen piezas disponibles
        result = gln.check_game_end_conditions(
            grid={(0, 0): {"team_id": 1, "morpion_id": 1}},
            grid_size=3,
            current_turn=4,
            max_turns=20,
            team1_id=1,
            team2_id=2,
            team1_morpions=team1,
            team2_morpions=team2,
            used_morpions=used,
        )
        self.assertFalse(result["game_over"])
        self.assertIsNone(result["winner_team_id"])
        self.assertIsNone(result["reason"])

    def test_is_grid_full_normale(self):
        grid = {(r, c): {"team_id": 1, "morpion_id": r * 4 + c} for r in range(4) for c in range(4)}
        self.assertTrue(gln.is_grid_full_normale(grid, grid_size=4))
        grid.pop((3, 3))
        self.assertFalse(gln.is_grid_full_normale(grid, grid_size=4))


if __name__ == "__main__":
    unittest.main()
