"""
Fonctions liées aux statistiques (fonctionnalité 1).
Séparées pour alléger model_pg et faciliter leur réutilisation.
"""

from .db_utils import count_instances, execute_select_query_dict

__all__ = [
    "get_counts_for_tables",
    "get_top_teams_by_wins",
    "get_fastest_and_longest_games",
    "get_avg_logs_per_month_year",
    "get_functionality_one_stats",
]


def get_counts_for_tables(connexion, table_names):
    results = []
    for name in table_names:
        results.append({"table": name, "count": count_instances(connexion, name)})
    return results


def get_top_teams_by_wins(connexion, limit=3):
    query = """
        SELECT
            t.id_team,
            t.name,
            COUNT(*) AS wins
        FROM team t
        JOIN game g
          ON g.id_winner = t.id_team
        GROUP BY t.id_team, t.name
        ORDER BY wins DESC, t.name ASC
        LIMIT %s
    """
    return execute_select_query_dict(connexion, query, [limit]) or []


def get_fastest_and_longest_games(connexion):
    base_query = """
        SELECT
            g.id_game,
            g.started_at,
            g.ended_at,
            g.ended_at - g.started_at AS duration,
            t1.id_team AS team1_id,
            t1.name    AS team1_name,
            t1.color   AS team1_color,
            t2.id_team AS team2_id,
            t2.name    AS team2_name,
            t2.color   AS team2_color,
            tw.id_team AS winner_id,
            tw.name    AS winner_name,
            tw.color   AS winner_color
        FROM game AS g
        JOIN team AS t1 ON t1.id_team = g.id_team1
        JOIN team AS t2 ON t2.id_team = g.id_team2
        LEFT JOIN team AS tw ON tw.id_team = g.id_winner
        WHERE g.ended_at IS NOT NULL
        ORDER BY duration {direction}
        LIMIT 1
    """

    fastest_rows = execute_select_query_dict(
        connexion,
        base_query.format(direction="ASC"),
    ) or []
    longest_rows = execute_select_query_dict(
        connexion,
        base_query.format(direction="DESC"),
    ) or []

    return (_normalize_duration_row(fastest_rows[0]) if fastest_rows else None,
            _normalize_duration_row(longest_rows[0]) if longest_rows else None)


def _normalize_duration_row(row):
    """
    Ajoute des champs exploitables côté template :
      - duration_seconds : nombre de secondes (pour les ratios)
      - duration_display : texte formaté HH:MM:SS
    """
    if row is None:
        return None

    duration = row.get("duration")
    seconds = 0

    if duration is not None:
        try:
            seconds = duration.total_seconds()
        except AttributeError:
            # psycopg peut retourner un float ou Decimal si l'interval est converti
            seconds = float(duration)

    row = row.copy()
    row["duration_seconds"] = max(0, float(seconds))
    row["duration_display"] = _format_duration_text(row["duration_seconds"])
    return row


def _format_duration_text(seconds):
    seconds = int(round(seconds))
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def get_avg_logs_per_month_year(connexion):
    query = """
        WITH per_game_month AS (
            SELECT
                id_game,
                DATE_TRUNC('month', created_at) AS month_start,
                COUNT(*) AS nb_logs
            FROM game_log
            GROUP BY id_game, DATE_TRUNC('month', created_at)
        )
        SELECT
            EXTRACT(YEAR FROM month_start)::int   AS year,
            EXTRACT(MONTH FROM month_start)::int  AS month,
            AVG(nb_logs)::float                   AS avg_logs
        FROM per_game_month
        GROUP BY year, month
        ORDER BY year, month
    """
    return execute_select_query_dict(connexion, query) or []


def get_functionality_one_stats(connexion, table_names=None, top_limit=3):
    if table_names is None:
        table_names = ["team", "morpion", "game"]

    counts = get_counts_for_tables(connexion, table_names)
    top_teams = get_top_teams_by_wins(connexion, limit=top_limit)
    fastest, longest = get_fastest_and_longest_games(connexion)
    avg_logs = get_avg_logs_per_month_year(connexion)

    return {
        "counts": counts,
        "top_teams": top_teams,
        "fastest_game": fastest,
        "longest_game": longest,
        "avg_logs": avg_logs,
    }
