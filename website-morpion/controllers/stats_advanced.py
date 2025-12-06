"""
Contrôleur pour la page de statistiques avancées.
Récupère des analyses complètes des données de jeu.
"""

from models.advanced_stats_repository import get_advanced_stats_all

REQUEST_VARS.setdefault('message', None)
REQUEST_VARS.setdefault('message_class', None)

# Récupérer toutes les statistiques avancées
stats = get_advanced_stats_all(SESSION["CONNEXION"])

# Calculs auxiliaires para los templates
# Normalizar valores para gráficos de barras (0-100%)
if stats["team_performance"]:
    max_games = max((t["total_games"] for t in stats["team_performance"]), default=1)
    for team in stats["team_performance"]:
        team["games_percentage"] = round((team["total_games"] / max_games * 100), 1) if max_games > 0 else 0

if stats["morpion_usage"]:
    max_usage = max((m["teams_count"] for m in stats["morpion_usage"]), default=1)
    for morpion in stats["morpion_usage"]:
        morpion["usage_percentage"] = round((morpion["teams_count"] / max_usage * 100), 1) if max_usage > 0 else 0

if stats["duration_distribution"]:
    max_count = max((d["game_count"] for d in stats["duration_distribution"]), default=1)
    for duration in stats["duration_distribution"]:
        duration["percentage"] = round((duration["game_count"] / max_count * 100), 1) if max_count > 0 else 0

if stats["top_killers"]:
    max_kills = max((k["kill_count"] for k in stats["top_killers"]), default=1)
    for killer in stats["top_killers"]:
        killer["percentage"] = round((killer["kill_count"] / max_kills * 100), 1) if max_kills > 0 else 0

if stats["win_methods"]:
    total_wins = sum(w["count"] for w in stats["win_methods"])
    for method in stats["win_methods"]:
        method["percentage"] = round((method["count"] / total_wins * 100), 1) if total_wins > 0 else 0

if stats["spell_usage"]:
    total_spells = sum(s["usage_count"] for s in stats["spell_usage"] if s["spell_type"] != "Autre")
    if total_spells > 0:
        for spell in stats["spell_usage"]:
            spell["percentage"] = round((spell["usage_count"] / total_spells * 100), 1) if total_spells > 0 else 0

if stats["grid_preferences"]:
    total_games = sum(g["games_count"] for g in stats["grid_preferences"])
    for grid in stats["grid_preferences"]:
        grid["percentage"] = round((grid["games_count"] / total_games * 100), 1) if total_games > 0 else 0

if stats["monthly_activity"]:
    max_activity = max((m["games_count"] for m in stats["monthly_activity"]), default=1)
    for month in stats["monthly_activity"]:
        month["activity_percentage"] = round((month["games_count"] / max_activity * 100), 1) if max_activity > 0 else 0

# Pasar todo a REQUEST_VARS
REQUEST_VARS["stats"] = stats
