"""
Battery of regression tests derived from the manual simulator that existed
in ``tests/simulate_cases.py``.  Converting it to real unit tests gives us
 deterministic assertions and surfaces failures automatically in CI.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple
import unittest

from models import game_logic_avancee as gla


Params = Dict[str, Any]


@dataclass
class GameCase:
    name: str
    description: str
    builder: Callable[[], Tuple[Params, Dict[str, Any]]]


def _base_params() -> Params:
    return {
        "grid_size": 4,
        "current_turn": 5,
        "max_turns": 20,
        "team1_id": 1,
        "team2_id": 2,
    }


def case_victory_team1_line() -> Tuple[Params, Dict[str, Any]]:
    params = _base_params()
    grid = {
        (0, 0): {"team_id": 1, "morpion_id": 101},
        (0, 1): {"team_id": 1, "morpion_id": 102},
        (0, 2): {"team_id": 1, "morpion_id": 103},
        (0, 3): {"team_id": 1, "morpion_id": 104},
    }
    params.update(
        grid=grid,
        morpions_state={mid: {"hp": 5, "mana": 5} for mid in [101, 102, 103, 104]},
        destroyed_cells=[],
        team1_morpions=[{"id_morpion": mid} for mid in [101, 102, 103, 104]],
        team2_morpions=[{"id_morpion": mid} for mid in [201, 202, 203, 204]],
        used_morpions=[101, 102, 103, 104],
    )
    expected = {"game_over": True, "winner_team_id": 1, "reason": "victory"}
    return params, expected


def case_victory_team2_line() -> Tuple[Params, Dict[str, Any]]:
    params = _base_params()
    params.update(team1_id=10, team2_id=20)
    grid = {
        (0, 0): {"team_id": 20, "morpion_id": 301},
        (1, 1): {"team_id": 20, "morpion_id": 302},
        (2, 2): {"team_id": 20, "morpion_id": 303},
        (3, 3): {"team_id": 20, "morpion_id": 304},
    }
    params.update(
        grid=grid,
        morpions_state={mid: {"hp": 5, "mana": 5} for mid in [301, 302, 303, 304]},
        destroyed_cells=[],
        team1_morpions=[{"id_morpion": mid} for mid in [101, 102, 103, 104]],
        team2_morpions=[{"id_morpion": mid} for mid in [301, 302, 303, 304]],
        used_morpions=[101, 102, 103, 104, 301, 302, 303, 304],
    )
    expected = {"game_over": True, "winner_team_id": 20, "reason": "victory"}
    return params, expected


def case_elimination_team1_dead() -> Tuple[Params, Dict[str, Any]]:
    params = _base_params()
    params.update(current_turn=12)
    team1_roster = [1, 2, 3]
    team2_roster = [4, 5, 6]
    params.update(
        grid={
            (0, 0): {"team_id": 2, "morpion_id": 4},
        },
        morpions_state={
            1: {"hp": 0, "mana": 0},
            2: {"hp": 0, "mana": 0},
            3: {"hp": 0, "mana": 0},
            4: {"hp": 5, "mana": 5},
        },
        destroyed_cells=[],
        team1_morpions=[{"id_morpion": mid} for mid in team1_roster],
        team2_morpions=[{"id_morpion": mid} for mid in team2_roster],
        used_morpions=team1_roster + [4],
    )
    expected = {"game_over": True, "winner_team_id": 2, "reason": "all_morpions_dead"}
    return params, expected


def case_elimination_team2_dead() -> Tuple[Params, Dict[str, Any]]:
    params = _base_params()
    team1_roster = [10, 11, 12]
    team2_roster = [20, 21, 22]
    params.update(
        grid={
            (0, 0): {"team_id": 1, "morpion_id": 10},
        },
        morpions_state={
            10: {"hp": 5, "mana": 5},
            20: {"hp": 0, "mana": 0},
            21: {"hp": 0, "mana": 0},
            22: {"hp": 0, "mana": 0},
        },
        destroyed_cells=[],
        team1_morpions=[{"id_morpion": mid} for mid in team1_roster],
        team2_morpions=[{"id_morpion": mid} for mid in team2_roster],
        used_morpions=[10] + team2_roster,
    )
    expected = {"game_over": True, "winner_team_id": 1, "reason": "all_morpions_dead"}
    return params, expected


def case_grid_full_draw() -> Tuple[Params, Dict[str, Any]]:
    params = _base_params()
    params.update(grid_size=3)
    grid = {
        (0, 0): {"team_id": 1, "morpion_id": 500},
        (0, 1): {"team_id": 2, "morpion_id": 501},
        (0, 2): {"team_id": 1, "morpion_id": 502},
        (1, 0): {"team_id": 2, "morpion_id": 503},
        (1, 1): {"team_id": 1, "morpion_id": 504},
        (1, 2): {"team_id": 2, "morpion_id": 505},
        (2, 0): {"team_id": 2, "morpion_id": 506},
        (2, 1): {"team_id": 1, "morpion_id": 507},
        (2, 2): {"team_id": 2, "morpion_id": 508},
    }
    morpions_state = {mid: {"hp": 5, "mana": 5} for mid in range(500, 509)}
    used = list(range(500, 509))
    team1 = [{"id_morpion": mid} for mid in [500, 502, 504, 506]]
    team2 = [{"id_morpion": mid} for mid in [501, 503, 505, 507, 508]]
    params.update(
        grid=grid,
        morpions_state=morpions_state,
        destroyed_cells=[],
        team1_morpions=team1,
        team2_morpions=team2,
        used_morpions=used,
        current_turn=30,
        max_turns=40,
    )
    expected = {"game_over": False, "winner_team_id": None, "reason": None}
    return params, expected


def case_max_turns_draw() -> Tuple[Params, Dict[str, Any]]:
    params = _base_params()
    params.update(current_turn=55, max_turns=50)
    params.update(
        grid={},
        morpions_state={},
        destroyed_cells=[],
        team1_morpions=[{"id_morpion": 1}],
        team2_morpions=[{"id_morpion": 2}],
        used_morpions=[],
    )
    expected = {"game_over": True, "winner_team_id": None, "reason": "max_turns"}
    return params, expected


def case_stalemate() -> Tuple[Params, Dict[str, Any]]:
    params = _base_params()
    params.update(current_turn=10)
    grid = {
        (0, 0): {"team_id": 1, "morpion_id": 1},
        (3, 3): {"team_id": 2, "morpion_id": 2},
    }
    params.update(
        grid=grid,
        morpions_state={1: {"hp": 5, "mana": 0}, 2: {"hp": 5, "mana": 0}},
        destroyed_cells=[],
        team1_morpions=[{"id_morpion": 1}],
        team2_morpions=[{"id_morpion": 2}],
        used_morpions=[1, 2],
    )
    expected = {"game_over": True, "winner_team_id": None, "reason": "stalemate"}
    return params, expected


def case_ongoing_with_reserves() -> Tuple[Params, Dict[str, Any]]:
    params = _base_params()
    grid = {
        (0, 0): {"team_id": 1, "morpion_id": 1},
        (0, 1): {"team_id": 2, "morpion_id": 2},
    }
    params.update(
        grid=grid,
        morpions_state={1: {"hp": 5, "mana": 0}, 2: {"hp": 5, "mana": 0}},
        destroyed_cells=[],
        team1_morpions=[{"id_morpion": 1}, {"id_morpion": 3}],
        team2_morpions=[{"id_morpion": 2}, {"id_morpion": 4}],
        used_morpions=[1, 2],
    )
    expected = {"game_over": False, "winner_team_id": None, "reason": None}
    return params, expected


def case_no_valid_actions_even_with_mana() -> Tuple[Params, Dict[str, Any]]:
    """Todos los morpions en grilla están aislados y sin mana, confirmando empate."""
    params = _base_params()
    params.update(current_turn=18)
    grid = {
        (0, 0): {"team_id": 1, "morpion_id": 11},
        (0, 3): {"team_id": 2, "morpion_id": 21},
        (3, 0): {"team_id": 1, "morpion_id": 12},
        (3, 3): {"team_id": 2, "morpion_id": 22},
    }
    morpions_state = {
        11: {"hp": 5, "mana": 0},
        12: {"hp": 5, "mana": 0},
        21: {"hp": 5, "mana": 0},
        22: {"hp": 5, "mana": 0},
    }
    params.update(
        grid=grid,
        morpions_state=morpions_state,
        destroyed_cells=[],
        team1_morpions=[{"id_morpion": 11}, {"id_morpion": 12}],
        team2_morpions=[{"id_morpion": 21}, {"id_morpion": 22}],
        used_morpions=[11, 12, 21, 22],
    )
    expected = {"game_over": True, "winner_team_id": None, "reason": "stalemate"}
    return params, expected


CASES: List[GameCase] = [
    GameCase("victory_team1_line", "Equipo 1 completa una fila.", case_victory_team1_line),
    GameCase("victory_team2_diagonal", "Equipo 2 completa una diagonal.", case_victory_team2_line),
    GameCase("all_dead_team1", "Equipo 1 usó todo su roster y murió.", case_elimination_team1_dead),
    GameCase("all_dead_team2", "Equipo 2 usó todo su roster y murió.", case_elimination_team2_dead),
    GameCase("grid_full_draw", "Grille completa sin línea.", case_grid_full_draw),
    GameCase("max_turns_draw", "Se alcanzó el límite de tours.", case_max_turns_draw),
    GameCase("stalemate", "Ambos equipos sin acciones posibles.", case_stalemate),
    GameCase("stalemate_spread", "Sin mana ni acciones incluso separados.", case_no_valid_actions_even_with_mana),
    GameCase("ongoing", "La partida continúa al quedar reservas.", case_ongoing_with_reserves),
]


class GameLogicAvanceeCaseTests(unittest.TestCase):
    def test_simulated_cases(self):
        for game_case in CASES:
            params, expected = game_case.builder()
            with self.subTest(name=game_case.name):
                result = gla.check_game_end_conditions_avancee(**params)
                for key, value in expected.items():
                    self.assertEqual(
                        value,
                        result.get(key),
                        msg=f"{game_case.name} → {game_case.description}",
                    )


class SpellValidationEdgeCaseTests(unittest.TestCase):
    def setUp(self):
        self.grid = {
            (0, 0): {"team_id": 1, "morpion_id": 1},
            (1, 0): {"team_id": 1, "morpion_id": 2},
            (0, 1): {"team_id": 2, "morpion_id": 3},
        }

    def test_armageddon_rejects_destroyed_cell(self):
        destroyed_cells = [(1, 1)]
        is_valid, message = gla.validate_spell_action(
            self.grid,
            caster_pos=(0, 0),
            target_pos=(1, 1),
            spell_type="armageddon",
            current_player=1,
            team1_id=1,
            team2_id=2,
            destroyed_cells=destroyed_cells,
        )
        self.assertFalse(is_valid)
        self.assertIn("déjà détruite", message)

    def test_insufficient_mana_for_spell(self):
        caster_state = {"mana": 0}
        self.assertFalse(gla.can_cast_spell(caster_state, "boule_de_feu", cost=2))
        caster_state["mana"] = 5
        self.assertTrue(gla.can_cast_spell(caster_state, "boule_de_feu", cost=2))


if __name__ == "__main__":
    unittest.main()
