from __future__ import annotations

import unittest
from unittest.mock import patch

from models.ai_engine import MorpionAI


class MorpionAITests(unittest.TestCase):
    def setUp(self):
        self.ai_team_id = 2
        self.player_team_id = 1
        self.available_morpions = [
            {"id_morpion": 1, "name": "Test1", "hp": 5, "attack": 5, "mana": 3, "accuracy": 2},
            {"id_morpion": 2, "name": "Test2", "hp": 4, "attack": 4, "mana": 4, "accuracy": 3},
        ]

    @patch("models.ai_engine.random.choice", side_effect=lambda seq: seq[0])
    def test_choose_move_empty_grid_valid_coordinates(self, _):
        ai = MorpionAI(difficulty="medium")
        morpion_id, position = ai.choose_move(
            grid={},
            grid_size=3,
            ai_team_id=self.ai_team_id,
            player_team_id=self.player_team_id,
            available_morpions=self.available_morpions,
        )
        self.assertIn(morpion_id, {1, 2})
        self.assertTrue(all(0 <= coord < 3 for coord in position))
        self.assertEqual(len(position), 2)

    @patch("models.ai_engine.random.choice", side_effect=lambda seq: seq[0])
    def test_choose_move_wins_when_possible(self, _):
        ai = MorpionAI(difficulty="hard")
        grid = {
            (1, 0): {"team_id": self.ai_team_id, "morpion_id": 10},
            (1, 1): {"team_id": self.ai_team_id, "morpion_id": 11},
            (0, 0): {"team_id": self.player_team_id, "morpion_id": 20},
        }
        _, position = ai.choose_move(
            grid=grid,
            grid_size=3,
            ai_team_id=self.ai_team_id,
            player_team_id=self.player_team_id,
            available_morpions=self.available_morpions,
        )
        self.assertEqual(position, (1, 2))

    @patch("models.ai_engine.random.choice", side_effect=lambda seq: seq[0])
    def test_choose_move_four_by_four_returns_free_cell(self, _):
        ai = MorpionAI(difficulty="medium")
        grid = {
            (0, 0): {"team_id": self.player_team_id, "morpion_id": 5},
            (1, 1): {"team_id": self.ai_team_id, "morpion_id": 6},
            (2, 2): {"team_id": self.player_team_id, "morpion_id": 7},
        }
        _, position = ai.choose_move(
            grid=grid,
            grid_size=4,
            ai_team_id=self.ai_team_id,
            player_team_id=self.player_team_id,
            available_morpions=self.available_morpions,
        )
        self.assertNotIn(position, grid)
        self.assertTrue(all(0 <= coord < 4 for coord in position))

    def test_choose_move_raises_without_morpions(self):
        ai = MorpionAI(difficulty="medium")
        with self.assertRaises(ValueError):
            ai.choose_move(
                grid={},
                grid_size=3,
                ai_team_id=self.ai_team_id,
                player_team_id=self.player_team_id,
                available_morpions=[],
            )

    def test_choose_move_raises_when_grid_full(self):
        ai = MorpionAI(difficulty="medium")
        full_grid = {(r, c): {"team_id": 1, "morpion_id": r * 4 + c} for r in range(3) for c in range(3)}
        with self.assertRaises(ValueError):
            ai.choose_move(
                grid=full_grid,
                grid_size=3,
                ai_team_id=self.ai_team_id,
                player_team_id=self.player_team_id,
                available_morpions=self.available_morpions,
            )

    @patch("models.ai_engine.random.random", return_value=0.1)
    @patch("models.ai_engine.random.choice", side_effect=lambda seq: seq[0])
    def test_easy_difficulty_can_use_random_move(self, mock_choice, _):
        ai = MorpionAI(difficulty="easy")
        # Force random branch via random.random() < 0.6
        _, position = ai.choose_move(
            grid={(0, 0): {"team_id": self.player_team_id, "morpion_id": 9}},
            grid_size=3,
            ai_team_id=self.ai_team_id,
            player_team_id=self.player_team_id,
            available_morpions=self.available_morpions,
        )
        # random.choice is called twice: first for morpion, then for position.
        self.assertGreaterEqual(mock_choice.call_count, 2)
        self.assertIn(position, [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])


if __name__ == "__main__":
    unittest.main()
