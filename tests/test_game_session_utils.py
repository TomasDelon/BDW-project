from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from controllers import game_session_utils as gsu


class GameSessionUtilsTests(unittest.TestCase):
    def test_build_session_key(self):
        self.assertEqual(gsu.build_session_key("game", 42), "game_42")

    def test_get_or_init_game_state_applies_defaults(self):
        defaults = {"turn": lambda: 1, "logs_cache": list}
        loader_calls = []

        def loader():
            loader_calls.append(True)
            return {"cells": {}}

        session_store = {}
        state = gsu.get_or_init_game_state(session_store, "game_1", loader, defaults)
        self.assertEqual(state["turn"], 1)
        self.assertEqual(state["logs_cache"], [])
        self.assertEqual(loader_calls.count(True), 1)
        # Calling again should reuse cached state without invoking loader.
        state2 = gsu.get_or_init_game_state(session_store, "game_1", loader, defaults)
        self.assertIs(state2, state)
        self.assertEqual(loader_calls.count(True), 1)

    def test_mark_logs_dirty_flags_cache(self):
        game_state = {"logs_dirty": False}
        session_store = {}
        gsu.mark_logs_dirty(game_state, session_store, "game_1")
        self.assertTrue(game_state["logs_dirty"])
        self.assertIs(session_store["game_1"], game_state)

    def test_get_logs_with_cache_fetches_once(self):
        game_state = {"logs_dirty": True}
        session_store = {}
        fetcher = MagicMock(return_value=["log1"])
        logs = gsu.get_logs_with_cache(game_state, session_store, "game_1", fetcher)
        self.assertEqual(logs, ["log1"])
        fetcher.assert_called_once()
        # Second call should reuse cache and not call fetcher again.
        fetcher.reset_mock()
        logs = gsu.get_logs_with_cache(game_state, session_store, "game_1", fetcher)
        self.assertEqual(logs, ["log1"])
        fetcher.assert_not_called()

    def test_setup_request_defaults_populates_keys(self):
        request_vars = {}
        gsu.setup_request_defaults(request_vars, allowed_grid_sizes=[3, 4])
        expected_keys = {"message", "page_mode", "allowed_grid_sizes", "ai_just_played"}
        self.assertTrue(expected_keys.issubset(request_vars.keys()))
        self.assertFalse(request_vars["game_over"])

    def test_get_requested_game_id_priority(self):
        GET = {"game_id": ["10"]}
        POST = {"game_id": ["11"]}
        self.assertEqual(gsu.get_requested_game_id("12", GET, POST), "10")
        self.assertEqual(gsu.get_requested_game_id(None, {}, POST), "11")
        self.assertEqual(gsu.get_requested_game_id("15", {}, {}), "15")
        self.assertEqual(gsu.get_requested_game_id(None, {}, {}), "")

    def test_sync_game_state_copies_core_fields(self):
        game_state = {}
        session_store = {}
        request_vars = {
            "grid": {(0, 0): "X"},
            "morpions_state": {1: {"hp": 5}},
            "current_turn": 5,
            "current_player": 2,
        }
        gsu.sync_game_state(game_state, request_vars, session_store, "game_1")
        self.assertEqual(game_state["cells"], {(0, 0): "X"})
        self.assertEqual(session_store["game_1"]["turn"], 5)
        self.assertEqual(session_store["game_1"]["current_player"], 2)

    def test_display_game_end_message_updates_session_and_logs(self):
        game_state = {"team1_id": 1, "team2_id": 2, "game_details": {}}
        game = {"team1_name": "Alpha", "team2_name": "Beta"}
        request_vars = {"game_over": False}
        session_store = {}
        session_key = "game_9"
        connexion = MagicMock()
        add_log_entry = MagicMock()
        update_game_end = MagicMock()
        refreshed_game = {"team1_name": "Alpha", "team2_name": "Beta", "id_winner": 1}

        with patch.object(gsu, "mark_logs_dirty") as mock_dirty:
            result = gsu.display_game_end_message(
                end_conditions={"game_over": True, "winner_team_id": 1, "reason": "victory"},
                game_state=game_state,
                game=game,
                REQUEST_VARS=request_vars,
                connexion=connexion,
                game_id=9,
                session_key=session_key,
                session_store=session_store,
                add_log_entry_fn=add_log_entry,
                update_game_end_fn=update_game_end,
                get_game_with_details_fn=MagicMock(return_value=refreshed_game),
            )

        self.assertEqual(result, refreshed_game)
        self.assertTrue(request_vars["game_over"])
        self.assertIn("🎉", request_vars["message"])
        update_game_end.assert_called_once_with(connexion, 9, 1)
        add_log_entry.assert_called_once()
        mock_dirty.assert_called_once_with(game_state, session_store, session_key)
        self.assertIs(session_store[session_key], game_state)


if __name__ == "__main__":
    unittest.main()
