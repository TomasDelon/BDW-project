"""
Repository pour la gestion des morpions personnalisés créés par les utilisateurs.
"""

from .db_utils import execute_select_query_dict, execute_other_query
from logzero import logger
import psycopg

__all__ = [
    "create_custom_morpion",
    "get_next_morpion_id",
    "check_morpion_name_exists",
]


def get_next_morpion_id(connexion):
    """
    Récupère le prochain ID disponible pour un morpion.
    Cherche les trous dans la séquence ou retourne max+1.
    """
    query = """
        SELECT COALESCE(MAX(id_morpion), 0) + 1 AS next_id
        FROM morpion
    """
    result = execute_select_query_dict(connexion, query)
    return result[0]['next_id'] if result else 17


def check_morpion_name_exists(connexion, name):
    """
    Vérifie si un morpion avec ce nom existe déjà.
    """
    query = """
        SELECT COUNT(*) as count
        FROM morpion
        WHERE LOWER(name) = LOWER(%s)
    """
    result = execute_select_query_dict(connexion, query, [name])
    return result[0]['count'] > 0 if result else False


def create_custom_morpion(connexion, name, hp, attack, mana, accuracy, image_filename):
    """
    Crée un nouveau morpion personnalisé dans la base de données.

    Args:
        connexion: Connexion PostgreSQL
        name: Nom du morpion
        hp: Points de vie (1-100)
        attack: Points d'attaque (1-100)
        mana: Points de mana (1-100)
        accuracy: Précision (1-100)
        image_filename: Nom du fichier image (ex: "custom_1.png")

    Returns:
        int: ID du morpion créé, ou None si erreur
    """
    query = """
        INSERT INTO morpion (name, hp, attack, mana, accuracy, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id_morpion
    """

    try:
        with connexion.cursor() as cursor:
            cursor.execute(query, [name, hp, attack, mana, accuracy, image_filename])
            result = cursor.fetchone()

        connexion.commit()
        logger.info(f"Morpion personnalisé créé : {name} (ID: {result[0] if result else 'unknown'})")
        return result[0] if result else None

    except psycopg.Error as err:
        logger.error(f"Erreur lors de la création du morpion personnalisé : {err}")
        connexion.rollback()
        return None
