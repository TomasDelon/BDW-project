from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from models import team_repository as trepo
from models import game_repository as grepo
from models import advanced_stats_repository as arepo


def make_connection_and_cursor():
    connexion = MagicMock()
    cursor = MagicMock()
    context_manager = MagicMock()
    context_manager.__enter__.return_value = cursor
    context_manager.__exit__.return_value = False
    connexion.cursor.return_value = context_manager
    return connexion, cursor


class TeamRepositoryTests(unittest.TestCase):
    def test_create_team_success_commits_and_returns_id(self):
        connexion, cursor = make_connection_and_cursor()
        cursor.fetchone.return_value = (123,)

        team_id = trepo.create_team(connexion, "Alpha", "#112233")

        self.assertEqual(team_id, 123)
        cursor.execute.assert_called_once()
        connexion.commit.assert_called_once()
        connexion.rollback.assert_not_called()

    def test_create_team_failure_rolls_back(self):
        connexion, cursor = make_connection_and_cursor()
        cursor.execute.side_effect = trepo.psycopg.Error("duplicate key")

        team_id = trepo.create_team(connexion, "Alpha", "#112233")

        self.assertIsNone(team_id)
        connexion.commit.assert_not_called()
        connexion.rollback.assert_called_once()

    def test_add_morpions_to_team_returns_insert_count(self):
        connexion, cursor = make_connection_and_cursor()
        cursor.rowcount = 3

        inserted = trepo.add_morpions_to_team(connexion, 10, [1, 2, 3])

        self.assertEqual(inserted, 3)
        cursor.executemany.assert_called_once()
        connexion.commit.assert_called_once()

    def test_add_morpions_to_team_handles_errors(self):
        connexion, cursor = make_connection_and_cursor()
        cursor.executemany.side_effect = trepo.psycopg.Error("boom")

        inserted = trepo.add_morpions_to_team(connexion, 10, [1, 2])

        self.assertIsNone(inserted)
        connexion.rollback.assert_called_once()


class GameRepositoryTests(unittest.TestCase):
    def test_add_log_entry_increments_log_num(self):
        connexion, cursor = make_connection_and_cursor()
        cursor.fetchone.return_value = (4,)

        ok = grepo.add_log_entry(connexion, game_id=7, message="Test log")

        self.assertTrue(ok)
        self.assertEqual(cursor.execute.call_count, 2)
        insert_call = cursor.execute.call_args_list[1]
        params = insert_call.args[1]
        self.assertEqual(params[1], 5)  # log_num should increment to 5
        connexion.commit.assert_called_once()

    def test_add_log_entry_handles_database_error(self):
        connexion, cursor = make_connection_and_cursor()
        cursor.execute.side_effect = grepo.psycopg.Error("deadlock")

        ok = grepo.add_log_entry(connexion, game_id=1, message="boom")

        self.assertFalse(ok)
        connexion.rollback.assert_called_once()


class AdvancedStatsRepositoryTests(unittest.TestCase):
    def test_duration_distribution_returns_empty_when_no_games(self):
        with patch.object(arepo, "execute_select_query_dict", return_value=None) as mock_query:
            data = arepo.get_game_duration_distribution(MagicMock())
        self.assertEqual(data, [])
        mock_query.assert_called_once()

    def test_team_win_rate_ranking_fallbacks_to_min_games_zero(self):
        fake_result = [{"id_team": 1, "name": "Alpha", "total_games": 1, "wins": 1, "win_rate": 100.0}]
        with patch.object(
            arepo, "execute_select_query_dict", side_effect=[[], fake_result]
        ) as mock_query:
            data = arepo.get_team_win_rate_ranking(MagicMock(), min_games=5)
        self.assertEqual(data, fake_result)
        self.assertEqual(mock_query.call_count, 2)
        first_params = mock_query.call_args_list[0].args[2]
        second_params = mock_query.call_args_list[1].args[2]
        self.assertEqual(first_params[0], 5)
        self.assertEqual(second_params[0], 0)


if __name__ == "__main__":
    unittest.main()
