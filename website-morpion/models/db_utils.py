"""
Fonctions utilitaires génériques pour exécuter des requêtes PostgreSQL.
Ce module centralise les helpers bas niveau afin qu'ils puissent être
réutilisés par les différents sous-modules de la couche modèle.
"""

import psycopg
from psycopg.rows import dict_row
from psycopg import sql
from logzero import logger

__all__ = [
    "execute_select_query",
    "execute_other_query",
    "get_instances",
    "count_instances",
    "execute_select_query_dict",
]


def execute_select_query(connexion, query, params=None):
    """
    Exécute une requête SELECT (retourne typiquement des tuples).
    """
    if params is None:
        params = []
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except psycopg.Error as err:
            logger.error(err)
    return None


def execute_other_query(connexion, query, params=None):
    """
    Exécute une requête INSERT / UPDATE / DELETE et retourne rowcount.
    """
    if params is None:
        params = []
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            return cursor.rowcount
        except psycopg.Error as err:
            logger.error(err)
    return None


def get_instances(connexion, nom_table):
    """
    Retourne toutes les lignes d'une table.
    """
    query = sql.SQL("SELECT * FROM {table}").format(
        table=sql.Identifier(nom_table),
    )
    return execute_select_query(connexion, query)


def count_instances(connexion, nom_table):
    """
    Retourne le nombre de lignes d'une table.
    """
    query = sql.SQL("SELECT COUNT(*) AS nb FROM {table}").format(
        table=sql.Identifier(nom_table),
    )
    rows = execute_select_query(connexion, query)
    if not rows:
        return 0
    return rows[0][0]


def execute_select_query_dict(connexion, query, params=None):
    """
    Exécute une requête SELECT et retourne une liste de dictionnaires.
    """
    if params is None:
        params = []
    try:
        with connexion.cursor() as cursor:
            cursor.row_factory = dict_row
            cursor.execute(query, params)
            return cursor.fetchall()
    except psycopg.Error as err:
        logger.error(err)
    return None

