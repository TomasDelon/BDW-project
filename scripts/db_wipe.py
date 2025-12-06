#!/usr/bin/env python3
"""
Vide complètement le schéma morpion via TRUNCATE ... CASCADE.
Utile pour tester l'UI sans données ou avant une restauration.
"""
import sys

from psycopg import sql

from db_utils import load_config, open_connection


def wipe_schema() -> None:
    config = load_config()
    confirmation = input(
        f"⚠️ Suppression de toutes les données dans le schéma '{config['schema']}'. Continuer ? (oui/non) "
    ).strip().lower()
    if confirmation not in {"oui", "o", "yes", "y"}:
        print("Vidage annulé.")
        return

    tables = ["game_log", "game", "game_config", "team_morpion", "team", "morpion"]
    with open_connection(config) as connexion:
        table_idents = [sql.Identifier(config["schema"], name) for name in tables]
        truncate_query = sql.SQL("TRUNCATE TABLE {} CASCADE;").format(
            sql.SQL(", ").join(table_idents)
        )
        connexion.execute(truncate_query)

    print("✅ Schéma vidé. Relancez db_init.py ou db_restore.py pour recharger des données.")


if __name__ == "__main__":
    wipe_schema()
