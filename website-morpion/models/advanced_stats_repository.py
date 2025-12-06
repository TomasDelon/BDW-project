"""
Fonctions pour les statistiques avancées (página extra).
Queries SQL complejas para análisis profundo de datos.
"""

from .db_utils import execute_select_query_dict

__all__ = [
    "get_team_performance_stats",
    "get_morpion_usage_stats",
    "get_spell_usage_stats",
    "get_game_duration_distribution",
    "get_win_methods_distribution",
    "get_team_win_rate_ranking",
    "get_most_deadly_morpions",
    "get_top_killers_from_logs",
    "get_grid_size_preferences",
    "get_monthly_activity",
    "get_advanced_stats_all",
]


def get_team_performance_stats(connexion, limit=10):
    """
    Estadísticas de rendimiento de equipos: victorias, derrotas, tasa de victoria.
    Muestra todos los equipos, incluso sin partidas jugadas.
    """
    query = """
        WITH team_games AS (
            SELECT
                t.id_team,
                t.name,
                t.color,
                COUNT(DISTINCT CASE WHEN g.id_winner = t.id_team THEN g.id_game END) AS wins,
                COUNT(DISTINCT CASE WHEN (g.id_team1 = t.id_team OR g.id_team2 = t.id_team) 
                                   AND g.id_winner IS NOT NULL 
                                   AND g.id_winner != t.id_team THEN g.id_game END) AS losses,
                COUNT(DISTINCT CASE WHEN (g.id_team1 = t.id_team OR g.id_team2 = t.id_team) 
                                   AND g.id_winner IS NULL THEN g.id_game END) AS draws,
                COUNT(DISTINCT CASE WHEN g.id_team1 = t.id_team OR g.id_team2 = t.id_team 
                                   THEN g.id_game END) AS total_games
            FROM team t
            LEFT JOIN game g ON g.id_team1 = t.id_team OR g.id_team2 = t.id_team
            GROUP BY t.id_team, t.name, t.color
        )
        SELECT
            id_team,
            name,
            color,
            wins,
            losses,
            draws,
            total_games,
            CASE WHEN total_games > 0 
                 THEN CAST(ROUND(CAST(wins AS NUMERIC) / CAST(total_games AS NUMERIC) * 100, 1) AS FLOAT)
                 ELSE 0 
            END AS win_rate
        FROM team_games
        ORDER BY total_games DESC, win_rate DESC, wins DESC, name ASC
        LIMIT %s
    """
    return execute_select_query_dict(connexion, query, [limit]) or []


def get_morpion_usage_stats(connexion, limit=10):
    """
    Morpions más usados en equipos.
    Muestra todos los morpions, incluso si no están en equipos.
    """
    query = """
        SELECT
            m.id_morpion,
            m.name,
            m.hp,
            m.attack,
            m.mana,
            m.accuracy,
            m.image_url,
            COUNT(DISTINCT tm.team_id) AS teams_count,
            ROUND(AVG(m.hp + m.attack + m.mana + m.accuracy), 1) AS avg_stats
        FROM morpion m
        LEFT JOIN team_morpion tm ON tm.morpion_id = m.id_morpion
        GROUP BY m.id_morpion, m.name, m.hp, m.attack, m.mana, m.accuracy, m.image_url
        ORDER BY teams_count DESC, m.name ASC
        LIMIT %s
    """
    return execute_select_query_dict(connexion, query, [limit]) or []


def get_spell_usage_stats(connexion):
    """
    Análisis de uso de sorts en logs (busca keywords en mensajes).
    """
    query = """
        SELECT
            CASE
                WHEN LOWER(message) LIKE '%%boule de feu%%' OR LOWER(message) LIKE '%%fireball%%' THEN 'Boule de feu'
                WHEN LOWER(message) LIKE '%%soin%%' OR LOWER(message) LIKE '%%heal%%' THEN 'Soin'
                WHEN LOWER(message) LIKE '%%armageddon%%' THEN 'Armageddon'
                ELSE 'Autre'
            END AS spell_type,
            COUNT(*) AS usage_count
        FROM game_log
        WHERE LOWER(message) LIKE '%%sort%%' 
           OR LOWER(message) LIKE '%%spell%%'
           OR LOWER(message) LIKE '%%boule%%'
           OR LOWER(message) LIKE '%%soin%%'
           OR LOWER(message) LIKE '%%armageddon%%'
        GROUP BY spell_type
        ORDER BY usage_count DESC
    """
    return execute_select_query_dict(connexion, query) or []


def get_game_duration_distribution(connexion):
    """
    Distribución de duraciones de partidas en rangos.
    """
    query = """
        WITH durations AS (
            SELECT
                id_game,
                EXTRACT(EPOCH FROM (ended_at - started_at)) AS duration_seconds
            FROM game
            WHERE ended_at IS NOT NULL AND started_at IS NOT NULL
        ),
        ranges AS (
            SELECT
                id_game,
                duration_seconds,
                CASE
                    WHEN duration_seconds < 60 THEN 1
                    WHEN duration_seconds < 300 THEN 2
                    WHEN duration_seconds < 900 THEN 3
                    WHEN duration_seconds < 1800 THEN 4
                    WHEN duration_seconds < 3600 THEN 5
                    ELSE 6
                END AS range_order,
                CASE
                    WHEN duration_seconds < 60 THEN '< 1 min'
                    WHEN duration_seconds < 300 THEN '1-5 min'
                    WHEN duration_seconds < 900 THEN '5-15 min'
                    WHEN duration_seconds < 1800 THEN '15-30 min'
                    WHEN duration_seconds < 3600 THEN '30-60 min'
                    ELSE '> 1 hora'
                END AS duration_range
            FROM durations
        )
        SELECT
            duration_range,
            COUNT(*) AS game_count,
            CAST(ROUND(AVG(duration_seconds), 0) AS INTEGER) AS avg_seconds
        FROM ranges
        GROUP BY duration_range, range_order
        ORDER BY range_order
    """
    results = execute_select_query_dict(connexion, query) or []
    
    # Si no hay partidas finalizadas, devolver estructura vacía
    if not results:
        return []
    
    return results


def get_win_methods_distribution(connexion):
    """
    Métodos de victoria inferidos de los logs.
    """
    query = """
        WITH last_logs AS (
            SELECT DISTINCT ON (gl.id_game)
                gl.id_game,
                gl.message,
                g.id_winner
            FROM game_log gl
            JOIN game g ON g.id_game = gl.id_game
            WHERE g.id_winner IS NOT NULL
            ORDER BY gl.id_game, gl.log_num DESC
        )
        SELECT
            CASE
                WHEN LOWER(message) LIKE '%%ligne%%' OR LOWER(message) LIKE '%%alignement%%' 
                     OR LOWER(message) LIKE '%%alignment%%' OR LOWER(message) LIKE '%%victoire%%' THEN 'Ligne complète'
                WHEN LOWER(message) LIKE '%%éliminé%%' OR LOWER(message) LIKE '%%tous les morpions%%'
                     OR LOWER(message) LIKE '%%mort%%' OR LOWER(message) LIKE '%%élimin%%' THEN 'Élimination totale'
                WHEN LOWER(message) LIKE '%%tours%%' OR LOWER(message) LIKE '%%maximum%%' THEN 'Max tours atteint'
                WHEN LOWER(message) LIKE '%%abandon%%' OR LOWER(message) LIKE '%%stalemate%%' THEN 'Impasse'
                ELSE 'Autre'
            END AS win_method,
            COUNT(*) AS count
        FROM last_logs
        GROUP BY win_method
        ORDER BY count DESC
    """
    results = execute_select_query_dict(connexion, query) or []
    
    # Si no hay partidas con winner, devolver lista vacía
    if not results:
        return []
    
    return results


def get_team_win_rate_ranking(connexion, min_games=1):
    """
    Ranking de equipos por tasa de victoria (mínimo de partidas jugadas).
    Si min_games=1, muestra equipos con al menos 1 partida.
    Si min_games=0, muestra todos los equipos.
    """
    query = """
        WITH team_stats AS (
            SELECT
                t.id_team,
                t.name,
                t.color,
                COUNT(DISTINCT g.id_game) AS total_games,
                COUNT(DISTINCT CASE WHEN g.id_winner = t.id_team THEN g.id_game END) AS wins
            FROM team t
            LEFT JOIN game g ON (g.id_team1 = t.id_team OR g.id_team2 = t.id_team)
                AND g.ended_at IS NOT NULL
            GROUP BY t.id_team, t.name, t.color
            HAVING COUNT(DISTINCT g.id_game) >= %s
        )
        SELECT
            id_team,
            name,
            color,
            total_games,
            wins,
            CAST(ROUND(CAST(wins AS NUMERIC) / NULLIF(CAST(total_games AS NUMERIC), 0) * 100, 1) AS FLOAT) AS win_rate
        FROM team_stats
        ORDER BY win_rate DESC, wins DESC
        LIMIT 10
    """
    results = execute_select_query_dict(connexion, query, [min_games])
    
    # Si no hay resultados con min_games, intentar con 0
    if not results and min_games > 0:
        return get_team_win_rate_ranking(connexion, min_games=0)
    
    return results or []


def get_most_deadly_morpions(connexion, limit=10):
    """
    Morpions con mayor ataque o características destacadas.
    """
    query = """
        SELECT
            m.id_morpion,
            m.name,
            m.hp,
            m.attack,
            m.mana,
            m.accuracy,
            m.image_url,
            (m.attack * 2 + m.hp + m.mana * 1.5)::int AS power_score
        FROM morpion m
        ORDER BY power_score DESC, m.attack DESC
        LIMIT %s
    """
    return execute_select_query_dict(connexion, query, [limit]) or []


def get_top_killers_from_logs(connexion, limit=5):
    """
    Analyse les logs pour dresser un classement des morpions qui éliminent le plus d'ennemis.
    """
    query = """
        WITH killer_logs AS (
            SELECT
                regexp_match(
                    message,
                    '^Joueur [0-9]+ \\(([^)]+)\\) - ([^:]+?)(?: a |:)'
                ) AS parts
            FROM game_log
            WHERE message ILIKE '%%a été éliminé%%'
        )
        SELECT
            TRIM(parts[2]) AS killer_name,
            TRIM(parts[1]) AS team_name,
            COUNT(*) AS kill_count
        FROM killer_logs
        WHERE parts IS NOT NULL
        GROUP BY killer_name, team_name
        ORDER BY kill_count DESC, killer_name ASC
        LIMIT %s
    """
    return execute_select_query_dict(connexion, query, [limit]) or []


def get_grid_size_preferences(connexion):
    """
    Preferencias de tamaño de grille.
    """
    query = """
        SELECT
            gc.grid_size,
            COUNT(DISTINCT g.id_game) AS games_count,
            ROUND(AVG(gc.max_turns), 1) AS avg_max_turns
        FROM game g
        JOIN game_config gc ON gc.id_config = g.id_config
        GROUP BY gc.grid_size
        ORDER BY gc.grid_size
    """
    return execute_select_query_dict(connexion, query) or []


def get_monthly_activity(connexion):
    """
    Actividad mensual: número de partidas creadas por mes.
    """
    query = """
        SELECT
            EXTRACT(YEAR FROM started_at)::int AS year,
            EXTRACT(MONTH FROM started_at)::int AS month,
            COUNT(*) AS games_count,
            COUNT(CASE WHEN ended_at IS NOT NULL THEN 1 END) AS completed_games
        FROM game
        GROUP BY year, month
        ORDER BY year DESC, month DESC
        LIMIT 12
    """
    return execute_select_query_dict(connexion, query) or []


def get_advanced_stats_all(connexion):
    """
    Recopila todas las estadísticas avanzadas en un solo diccionario.
    """
    return {
        "team_performance": get_team_performance_stats(connexion, limit=10),
        "morpion_usage": get_morpion_usage_stats(connexion, limit=10),
        "spell_usage": get_spell_usage_stats(connexion),
        "duration_distribution": get_game_duration_distribution(connexion),
        "win_methods": get_win_methods_distribution(connexion),
        "team_ranking": get_team_win_rate_ranking(connexion, min_games=1),
        "deadly_morpions": get_most_deadly_morpions(connexion, limit=8),
        "top_killers": get_top_killers_from_logs(connexion, limit=6),
        "grid_preferences": get_grid_size_preferences(connexion),
        "monthly_activity": get_monthly_activity(connexion),
    }
