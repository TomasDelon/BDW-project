import unittest

from models import game_logic_avancee as gla


class GameLogicAvanceeTests(unittest.TestCase):
    def test_victory_line(self):
        grid = {
            (0, 0): {"team_id": 1, "morpion_id": 101},
            (1, 1): {"team_id": 1, "morpion_id": 102},
            (2, 2): {"team_id": 1, "morpion_id": 103},
        }
        morpions_state = {
            101: {"hp": 5},
            102: {"hp": 5},
            103: {"hp": 5},
        }
        team1 = [{"id_morpion": 101}, {"id_morpion": 102}, {"id_morpion": 103}]
        team2 = [{"id_morpion": 201}, {"id_morpion": 202}, {"id_morpion": 203}]

        result = gla.check_game_end_conditions_avancee(
            grid,
            grid_size=3,
            current_turn=5,
            max_turns=20,
            team1_id=1,
            team2_id=2,
            morpions_state=morpions_state,
            destroyed_cells=[],
            team1_morpions=team1,
            team2_morpions=team2,
            used_morpions=[101, 102, 103],
        )

        self.assertTrue(result["game_over"])
        self.assertEqual(result["winner_team_id"], 1)
        self.assertEqual(result["reason"], "victory")

    def test_all_morpions_dead_after_all_used(self):
        # Team 1 has played all its morpions and they are dead
        morpions_state = {
            1: {"hp": 0},
            2: {"hp": 0},
        }
        grid = {}  # cleaned up after deaths
        team1 = [{"id_morpion": 1}, {"id_morpion": 2}]
        team2 = [{"id_morpion": 3}, {"id_morpion": 4}]

        result = gla.check_game_end_conditions_avancee(
            grid,
            grid_size=4,
            current_turn=10,
            max_turns=30,
            team1_id=1,
            team2_id=2,
            morpions_state=morpions_state,
            destroyed_cells=[],
            team1_morpions=team1,
            team2_morpions=team2,
            used_morpions=[1, 2, 3],  # team1 fully used, team2 still has one available
        )

        self.assertTrue(result["game_over"])
        self.assertEqual(result["winner_team_id"], 2)
        self.assertEqual(result["reason"], "all_morpions_dead")

    def test_stalemate_no_actions_possible(self):
        # Both rosters exhausted, no mana, not adjacent => stalemate
        grid = {
            (0, 0): {"team_id": 1, "morpion_id": 1},
            (3, 3): {"team_id": 2, "morpion_id": 3},
        }
        morpions_state = {
            1: {"hp": 5, "mana": 0},
            3: {"hp": 5, "mana": 0},
        }
        team1 = [{"id_morpion": 1}, {"id_morpion": 2}]
        team2 = [{"id_morpion": 3}, {"id_morpion": 4}]

        result = gla.check_game_end_conditions_avancee(
            grid,
            grid_size=4,
            current_turn=15,
            max_turns=30,
            team1_id=1,
            team2_id=2,
            morpions_state=morpions_state,
            destroyed_cells=[],
            team1_morpions=team1,
            team2_morpions=team2,
            used_morpions=[1, 2, 3, 4],  # todos los morpions ya usados
        )

        self.assertTrue(result["game_over"])
        self.assertIsNone(result["winner_team_id"])
        self.assertEqual(result["reason"], "stalemate")

    def test_no_stalemate_when_reserves_exist(self):
        # Team 2 still has a morpion not yet placed -> no stalemate
        grid = {
            (0, 0): {"team_id": 1, "morpion_id": 1},
            (3, 3): {"team_id": 2, "morpion_id": 3},
        }
        morpions_state = {
            1: {"hp": 5, "mana": 0},
            3: {"hp": 5, "mana": 0},
        }
        team1 = [{"id_morpion": 1}, {"id_morpion": 2}]
        team2 = [{"id_morpion": 3}, {"id_morpion": 4}]

        result = gla.check_game_end_conditions_avancee(
            grid,
            grid_size=4,
            current_turn=15,
            max_turns=30,
            team1_id=1,
            team2_id=2,
            morpions_state=morpions_state,
            destroyed_cells=[],
            team1_morpions=team1,
            team2_morpions=team2,
            used_morpions=[1, 2, 3],  # team2 todavía tiene el 4 sin usar
        )

        self.assertFalse(result["game_over"])
        self.assertIsNone(result["winner_team_id"])
        self.assertIsNone(result["reason"])

    def test_calculate_success_probability_clamps(self):
        self.assertAlmostEqual(gla.calculate_success_probability(5), 90.0, places=3)
        self.assertAlmostEqual(gla.calculate_success_probability(20), 42.0, places=3)
        self.assertEqual(gla.calculate_success_probability(-5), 0.0)


if __name__ == "__main__":
    unittest.main()
