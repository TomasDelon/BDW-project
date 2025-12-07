"""
Fonctions liées à la gestion des équipes, morpions et parties.
"""

import psycopg
from logzero import logger

from .db_utils import execute_select_query_dict
from constants import MIN_MORPIONS_PER_TEAM, TEAM_GAMES_HISTORY_LIMIT

__all__ = [
    "get_all_morpions",
    "check_team_name_color_exists",
    "check_team_color_exists",
    "create_team",
    "add_morpions_to_team",
    "get_all_teams_with_morpions",
    "get_teams_for_game_selection",
    "get_games_for_team",
    "get_games_for_teams",
    "delete_games_for_team",
    "delete_team",
]


def get_all_morpions(connexion):
    """
    Récupère tous les morpions disponibles dans la base de données.
    
    Args:
        connexion: Connexion à la base de données
    
    Returns:
        list: Liste de dictionnaires contenant les informations des morpions
    """
    query = """
        SELECT
            id_morpion,
            name,
            image_url,
            hp,
            attack,
            mana,
            accuracy
        FROM morpion
        ORDER BY name ASC
    """
    return execute_select_query_dict(connexion, query) or []


def count_teams(connexion, filters):
    """
    Compte les équipes répondant à un ensemble de filtres {colonne: valeur}.
    """
    where_clauses = []
    params = []
    for column, value in filters.items():
        where_clauses.append(f"{column} = %s")
        params.append(value)
    where_sql = " AND ".join(where_clauses) if where_clauses else "TRUE"

    query = f"""
        SELECT COUNT(*) AS count
        FROM team
        WHERE {where_sql}
    """
    result = execute_select_query_dict(connexion, query, params)
    return result[0]["count"] if result else 0


def check_team_name_color_exists(connexion, name, color):
    """
    Vérifie si une équipe existe déjà avec le nom et la couleur spécifiés.
    
    Args:
        connexion: Connexion à la base de données
        name: Nom de l'équipe à vérifier
        color: Couleur de l'équipe à vérifier
    
    Returns:
        bool: True si une équipe existe déjà avec ces critères, False sinon
    """
    return count_teams(connexion, {"name": name, "color": color}) > 0


def check_team_color_exists(connexion, color):
    """
    Vérifie si une équipe existe déjà avec la couleur spécifiée.
    
    Args:
        connexion: Connexion à la base de données
        color: Couleur de l'équipe à vérifier
    
    Returns:
        bool: True si une équipe existe déjà avec cette couleur, False sinon
    """
    return count_teams(connexion, {"color": color}) > 0


def create_team(connexion, name, color):
    """
    Crée une nouvelle équipe avec le nom et la couleur spécifiés.
    
    Args:
        connexion: Connexion à la base de données
        name: Nom de la nouvelle équipe
        color: Couleur de la nouvelle équipe
    
    Returns:
        int | None: ID de la nouvelle équipe créée, ou None en cas d'erreur
    """
    query = """
        INSERT INTO team (name, color)
        VALUES (%s, %s)
        RETURNING id_team
    """
    try:
        with connexion.cursor() as cursor:
            cursor.execute(query, [name, color])
            result = cursor.fetchone()
        connexion.commit()
        return result[0] if result else None
    except psycopg.Error as err:
        logger.error(f"Erreur lors de la création de l'équipe: {err}")
        connexion.rollback()
        return None


def add_morpions_to_team(connexion, team_id, morpion_ids):
    """
    Ajoute une liste de morpions à une équipe.
    
    Args:
        connexion: Connexion à la base de données
        team_id: ID de l'équipe
        morpion_ids: Liste des IDs des morpions à ajouter
    
    Returns:
        int | None: Nombre de morpions ajoutés, ou None en cas d'erreur
    """
    if not morpion_ids:
        return 0

    query = """
        INSERT INTO team_morpion (team_id, morpion_id)
        VALUES (%s, %s)
        ON CONFLICT (team_id, morpion_id) DO NOTHING
    """
    values = [(team_id, morpion_id) for morpion_id in morpion_ids]
    try:
        with connexion.cursor() as cursor:
            cursor.executemany(query, values)
            inserted = cursor.rowcount
        connexion.commit()
        return inserted
    except psycopg.Error as err:
        logger.error(f"Erreur lors de l'ajout des morpions à l'équipe: {err}")
        connexion.rollback()
        return None


def get_all_teams_with_morpions(connexion):
    """
    Récupère toutes les équipes avec leurs morpions associés.
    
    Args:
        connexion: Connexion à la base de données
    
    Returns:
        list: Liste d'équipes avec leurs morpions détaillés
    """
    query = """
        SELECT
            t.id_team,
            t.name,
            t.color,
            t.created_at,
            tm.morpion_id,
            m.name AS morpion_name,
            m.image_url,
            m.hp,
            m.attack,
            m.mana,
            m.accuracy
        FROM team t
        LEFT JOIN team_morpion tm ON t.id_team = tm.team_id
        LEFT JOIN morpion m ON tm.morpion_id = m.id_morpion
        ORDER BY t.created_at DESC, t.name ASC, m.name ASC
    """
    rows = execute_select_query_dict(connexion, query) or []

    teams = {}
    for row in rows:
        team_id = row['id_team']
        team_entry = teams.setdefault(team_id, {
            "id_team": team_id,
            "name": row['name'],
            "color": row['color'],
            "created_at": row['created_at'],
            "morpions": [],
        })
        if row['morpion_id'] is not None:
            team_entry["morpions"].append({
                "id_morpion": row['morpion_id'],
                "name": row['morpion_name'],
                "image_url": row['image_url'],
                "hp": row['hp'],
                "attack": row['attack'],
                "mana": row['mana'],
                "accuracy": row['accuracy'],
            })

    for team_entry in teams.values():
        team_entry["morpion_count"] = len(team_entry["morpions"])

    return list(teams.values())


def get_teams_for_game_selection(connexion):
    """
    Retourne toutes les équipes avec leur nombre de morpions.
    Filtre pour ne garder que les équipes avec au moins 6 morpions.
    """
    query = """
        SELECT 
            t.id_team,
            t.name,
            t.color,
            COUNT(tm.morpion_id) as morpion_count
        FROM team t
        LEFT JOIN team_morpion tm ON t.id_team = tm.team_id
        GROUP BY t.id_team, t.name, t.color
        HAVING COUNT(tm.morpion_id) >= %s
        ORDER BY t.name ASC
    """
    return execute_select_query_dict(connexion, query, [MIN_MORPIONS_PER_TEAM]) or []


def get_games_for_team(connexion, team_id, limit_per_team=None):
    """
    Retourne les parties liées à une équipe spécifique.
    
    Args:
        connexion: Connexion à la base de données
        team_id: ID de l'équipe
        limit_per_team: Limite du nombre de parties à retourner (optionnel)
    
    Returns:
        list: Liste des parties auxquelles l'équipe a participé
    """
    games_map = get_games_for_teams(connexion, [team_id], limit_per_team=limit_per_team)
    return games_map.get(team_id, [])


def get_games_for_teams(connexion, team_ids, limit_per_team=None):
    """
    Retourne un dictionnaire {team_id: [games]} pour une liste d'équipes.
    Évite les requêtes répétées lors de l'affichage de plusieurs équipes.
    
    Args:
        connexion: Connexion à la base de données
        team_ids: Liste des IDs des équipes
        limit_per_team: Limite du nombre de parties par équipe (optionnel)
    
    Returns:
        dict: Dictionnaire avec les parties pour chaque équipe
    """
    if not team_ids:
        return {}

    base_cte = """
        WITH detailed_games AS (
            SELECT
                g.id_game,
                g.id_team1 AS team1_id,
                t1.name AS team1_name,
                t1.color AS team1_color,
                g.id_team2 AS team2_id,
                t2.name AS team2_name,
                t2.color AS team2_color,
                g.id_winner AS winner_team_id,
                tw.name AS winner_name,
                g.started_at,
                g.ended_at,
                g.id_config AS config_id,
                c.grid_size,
                c.max_turns
            FROM game g
            JOIN team t1 ON t1.id_team = g.id_team1
            JOIN team t2 ON t2.id_team = g.id_team2
            LEFT JOIN team tw ON tw.id_team = g.id_winner
            JOIN game_config c ON c.id_config = g.id_config
        )
    """

    if limit_per_team:
        query = base_cte + """
        , selected_games AS (
            SELECT dg.*, dg.team1_id AS team_ref
            FROM detailed_games dg
            WHERE dg.team1_id = ANY(%s)
            UNION ALL
            SELECT dg.*, dg.team2_id AS team_ref
            FROM detailed_games dg
            WHERE dg.team2_id = ANY(%s)
        ),
        ranked_games AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY team_ref ORDER BY started_at DESC, id_game DESC) AS rn,
                   COUNT(*) OVER (PARTITION BY team_ref) AS total_games
            FROM selected_games
        )
        SELECT * FROM ranked_games
        WHERE rn <= %s
        ORDER BY started_at DESC;
        """
        params = [team_ids, team_ids, limit_per_team]
    else:
        query = base_cte + """
        SELECT *,
               NULL::INTEGER AS team_ref,
               NULL::INTEGER AS total_games
        FROM detailed_games
        WHERE team1_id = ANY(%s) OR team2_id = ANY(%s)
        ORDER BY started_at DESC;
        """
        params = [team_ids, team_ids]

    rows = execute_select_query_dict(connexion, query, params) or []
    games_by_team = {team_id: [] for team_id in team_ids}

    for row in rows:
        team_ref = row.pop('team_ref', None)
        total_games = row.pop('total_games', None)
        if team_ref is not None:
            games_by_team.setdefault(team_ref, []).append({**row, 'total_games': total_games})
        else:
            games_by_team.setdefault(row['team1_id'], []).append(dict(row))
            games_by_team.setdefault(row['team2_id'], []).append(dict(row))

    return games_by_team


def delete_games_for_team(connexion, cursor, team_id):
    """
    Supprime toutes les parties associées à une équipe.
    
    Args:
        connexion: Connexion à la base de données
        cursor: Curseur de la base de données
        team_id: ID de l'équipe
    """
    query = """
        DELETE FROM game
        WHERE id_team1 = %s OR id_team2 = %s
    """
    cursor.execute(query, [team_id, team_id])


def delete_team(connexion, team_id, delete_games=False):
    """
    Supprime une équipe et éventuellement ses parties associées.
    
    Args:
        connexion: Connexion à la base de données
        team_id: ID de l'équipe à supprimer
        delete_games: Booléen indiquant si les parties doivent être supprimées (optionnel)
    
    Returns:
        bool: True si l'équipe a été supprimée avec succès, False sinon
    """
    try:
        with connexion.cursor() as cursor:
            if delete_games:
                delete_games_for_team(connexion, cursor, team_id)

            query = "DELETE FROM team WHERE id_team = %s"
            cursor.execute(query, [team_id])
            rowcount = cursor.rowcount
        connexion.commit()
        return rowcount > 0
    except psycopg.Error as err:
        logger.error(f"Erreur lors de la suppression de l'équipe: {err}")
        connexion.rollback()
        return False
