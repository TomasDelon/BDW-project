"""
Module façade conservé pour compatibilité.

L'ancien fichier `model_pg.py` a été découpé en sous-modules :
  - db_utils : fonctions génériques d'accès aux données
  - stats_repository : statistiques (fonctionnalité 1)
  - team_repository : gestion des équipes / morpions (fonctionnalité 2)

Ce fichier ré-exporte les symboles principaux afin d'éviter de modifier
immédiatement tous les contrôleurs existants.
"""

from .db_utils import (
    execute_select_query,
    execute_other_query,
    get_instances,
    count_instances,
    execute_select_query_dict,
)
from .stats_repository import (
    get_counts_for_tables,
    get_top_teams_by_wins,
    get_fastest_and_longest_games,
    get_avg_logs_per_month_year,
    get_functionality_one_stats,
)
from .advanced_stats_repository import (
    get_team_performance_stats,
    get_morpion_usage_stats,
    get_spell_usage_stats,
    get_game_duration_distribution,
    get_win_methods_distribution,
    get_team_win_rate_ranking,
    get_most_deadly_morpions,
    get_grid_size_preferences,
    get_monthly_activity,
    get_advanced_stats_all,
)
from .team_repository import (
    get_all_morpions,
    check_team_name_color_exists,
    check_team_color_exists,
    create_team,
    add_morpions_to_team,
    get_all_teams_with_morpions,
    get_teams_for_game_selection,
    get_games_for_team,
    get_games_for_teams,
    delete_team,
)
from .custom_morpion_repository import (
    create_custom_morpion,
    get_next_morpion_id,
    check_morpion_name_exists,
)
from .game_repository import (
    create_config,
    create_game,
    get_game_with_details,
    get_team_morpions_for_game,
    add_log_entry,
    get_game_logs,
    update_game_end,
)
from .game_logic_normale import (
    check_victory_normale,
    is_grid_full_normale,
    check_game_end_conditions,
)
from .game_logic_avancee import (
    calculate_success_probability,
    roll_action_success,
    can_attack,
    execute_attack,
    can_cast_spell,
    execute_boule_de_feu,
    execute_soin,
    execute_armageddon,
    validate_attack_action,
    validate_spell_action,
    check_all_morpions_dead,
    check_game_end_conditions_avancee,
)

__all__ = [
    # db utils
    "execute_select_query",
    "execute_other_query",
    "get_instances",
    "count_instances",
    "execute_select_query_dict",
    # stats
    "get_counts_for_tables",
    "get_top_teams_by_wins",
    "get_fastest_and_longest_games",
    "get_avg_logs_per_month_year",
    "get_functionality_one_stats",
    # team / morpion
    "get_all_morpions",
    "check_team_name_color_exists",
    "check_team_color_exists",
    "create_team",
    "add_morpions_to_team",
    "get_all_teams_with_morpions",
    "get_teams_for_game_selection",
    "get_games_for_team",
    "get_games_for_teams",
    "delete_team",
    # custom morpion
    "create_custom_morpion",
    "get_next_morpion_id",
    "check_morpion_name_exists",
    # game (repository - shared)
    "create_config",
    "create_game",
    "get_game_with_details",
    "get_team_morpions_for_game",
    "add_log_entry",
    "get_game_logs",
    "update_game_end",
    # game logic (normale)
    "check_victory_normale",
    "is_grid_full_normale",
    "check_game_end_conditions",
    # game logic (avancée)
    "calculate_success_probability",
    "roll_action_success",
    "can_attack",
    "execute_attack",
    "can_cast_spell",
    "execute_boule_de_feu",
    "execute_soin",
    "execute_armageddon",
    "validate_attack_action",
    "validate_spell_action",
    "check_all_morpions_dead",
    "check_game_end_conditions_avancee",
]
