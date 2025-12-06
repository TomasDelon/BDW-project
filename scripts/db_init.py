#!/usr/bin/env python3
"""
Initialise le schéma morpion avec les scripts SQL fournis.
Par défaut : schema.sql + add_ai_team.sql (aucune suppression).
Option --reset : exécute reset.sql (DROP CASCADE) avant de recharger.
"""
import argparse

from db_utils import SQL_DIR, load_config, run_sql_file_with_psql


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialise la base avec les scripts SQL existants.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Supprime le schéma puis le recrée via reset.sql (destructif).",
    )
    args = parser.parse_args()

    config = load_config()
    schema_script = SQL_DIR / "schema.sql"
    add_ai_script = SQL_DIR / "add_ai_team.sql"

    if args.reset:
        reset_script = SQL_DIR / "reset.sql"
        confirmation = input(
            f"⚠️ Réinitialisation complète du schéma '{config['schema']}'. Continuer ? (oui/non) "
        ).strip().lower()
        if confirmation not in {"oui", "o", "yes", "y"}:
            print("Réinitialisation annulée.")
            return
        print("Réinitialisation complète...")
        run_sql_file_with_psql(reset_script, config)
    else:
        print("Initialisation sans suppression préalable...")
        run_sql_file_with_psql(schema_script, config)

    print("Ajout/validation de l'équipe IA...")
    run_sql_file_with_psql(add_ai_script, config)
    print("✅ Base de démonstration prête.")


if __name__ == "__main__":
    main()
