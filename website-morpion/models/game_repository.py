"""
Fonctions liées à la gestion des parties (fonctionnalité 3 et 4).
Funciones base compartidas por ambas funcionalidades.
"""

import psycopg
from logzero import logger
from .db_utils import execute_select_query_dict

__all__ = [
    "create_config",
    "create_game",
    "get_game_with_details",
    "get_team_morpions_for_game",
    "add_log_entry",
    "get_game_logs",
    "update_game_end",
]


def create_config(connexion, grid_size, max_turns):
    """
    Crée une nouvelle configuration de partie.
    Retourne l'id_config ou None en cas d'erreur.
    """
    query = """
        INSERT INTO game_config (grid_size, max_turns)
        VALUES (%s, %s)
        RETURNING id_config
    """
    try:
        with connexion.cursor() as cursor:
            cursor.execute(query, [grid_size, max_turns])
            result = cursor.fetchone()
        connexion.commit()
        return result[0] if result else None
    except psycopg.Error as err:
        logger.error(f"Erreur lors de la création de la config: {err}")
        connexion.rollback()
        return None


def create_game(connexion, team1_id, team2_id, config_id):
    """
    Crée une nouvelle partie entre deux équipes.
    Retourne l'id_game ou None en cas d'erreur.
    """
    query = """
        INSERT INTO game (id_team1, id_team2, id_config)
        VALUES (%s, %s, %s)
        RETURNING id_game
    """
    try:
        with connexion.cursor() as cursor:
            cursor.execute(query, [team1_id, team2_id, config_id])
            result = cursor.fetchone()
        connexion.commit()
        return result[0] if result else None
    except psycopg.Error as err:
        logger.error(f"Erreur lors de la création de la partie: {err}")
        connexion.rollback()
        return None


def get_game_with_details(connexion, game_id):
    """
    Retourne les détails complets d'une partie.
    """
    query = """
        SELECT
            g.id_game,
            g.id_team1 AS team1_id,
            t1.name AS team1_name,
            t1.color AS team1_color,
            g.id_team2 AS team2_id,
            t2.name AS team2_name,
            t2.color AS team2_color,
            g.id_config AS config_id,
            c.grid_size,
            c.max_turns,
            g.started_at,
            g.ended_at,
            g.id_winner AS winner_team_id,
            tw.name AS winner_name
        FROM game g
        JOIN team t1 ON g.id_team1 = t1.id_team
        JOIN team t2 ON g.id_team2 = t2.id_team
        JOIN game_config c ON g.id_config = c.id_config
        LEFT JOIN team tw ON g.id_winner = tw.id_team
        WHERE g.id_game = %s
    """
    result = execute_select_query_dict(connexion, query, [game_id])
    return result[0] if result else None


def get_team_morpions_for_game(connexion, team_id):
    """
    Retourne la liste des morpions d'une équipe pour une partie.
    """
    query = """
        SELECT
            m.id_morpion,
            m.name,
            m.image_url,
            m.hp,
            m.attack,
            m.mana,
            m.accuracy
        FROM morpion m
        JOIN team_morpion tm ON m.id_morpion = tm.morpion_id
        WHERE tm.team_id = %s
        ORDER BY m.name ASC
    """
    return execute_select_query_dict(connexion, query, [team_id]) or []


def add_log_entry(connexion, game_id, message):
    """
    Ajoute une entrée dans le journal de la partie.
    Gère log_num manuellement (1, 2, 3, ...) par partie.
    """
    query_last = """
        SELECT log_num
        FROM game_log
        WHERE id_game = %s
        ORDER BY log_num DESC
        LIMIT 1
        FOR UPDATE
    """
    query_insert = """
        INSERT INTO game_log (id_game, log_num, message)
        VALUES (%s, %s, %s)
    """
    try:
        with connexion.cursor() as cursor:
            cursor.execute(query_last, [game_id])
            row = cursor.fetchone()
            next_num = (row[0] if row else 0) + 1
            cursor.execute(query_insert, [game_id, next_num, message])
        connexion.commit()
        return True
    except psycopg.Error as err:
        logger.error(f"Erreur lors de l'ajout d'une entrée de log: {err}")
        connexion.rollback()
        return False


def get_game_logs(connexion, game_id, limit=None):
    """
    Retourne los logs d'una partie, triés par numéro.
    Si limit est spécifié, retourne seulement les N derniers logs.
    """
    query = """
        SELECT log_num AS num, created_at, message
        FROM game_log
        WHERE id_game = %s
        ORDER BY log_num ASC
    """
    if limit:
        query += f" LIMIT {int(limit)}"
    
    result = execute_select_query_dict(connexion, query, [game_id]) or []
    logger.info(f"get_game_logs: game_id={game_id}, found {len(result)} logs")
    return result


def update_game_end(connexion, game_id, winner_team_id=None):
    """
    Marque une partie comme terminée avec un éventuel gagnant.
    winner_team_id peut être None (égalité ou grille pleine).
    """
    query = """
        UPDATE game
        SET ended_at = CURRENT_TIMESTAMP,
            id_winner = %s
        WHERE id_game = %s
    """
    try:
        with connexion.cursor() as cursor:
            cursor.execute(query, [winner_team_id, game_id])
        connexion.commit()
        return True
    except psycopg.Error as err:
        logger.error(f"Erreur lors de la mise à jour de la fin de partie: {err}")
        connexion.rollback()
        return False
