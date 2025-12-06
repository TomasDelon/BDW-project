#!/usr/bin/env python3
"""
Restaure la dernière sauvegarde (ou un fichier donné) dans le schéma morpion.
⚠️ Cette opération écrase les données existantes : confirmation demandée.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from db_utils import BACKUP_DIR, build_pg_env, load_config, psql_base_command, require_binary


def select_backup(name: str | None) -> Path:
    """
    Choisit le fichier de sauvegarde à utiliser.
    """
    if name:
        candidate = Path(name)
        if not candidate.is_absolute():
            candidate = BACKUP_DIR / candidate
        if not candidate.exists():
            sys.exit(f"Sauvegarde introuvable : {candidate}")
        return candidate

    backups = sorted(BACKUP_DIR.glob("backup_morpion_*.sql"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not backups:
        sys.exit(f"Aucune sauvegarde disponible dans {BACKUP_DIR}. Lancez d'abord db_backup.py.")
    return backups[0]


def restore_backup(backup_path: Path) -> None:
    config = load_config()
    require_binary("psql")

    confirmation = input(
        f"⚠️ Cela va écraser les données du schéma '{config['schema']}' avec {backup_path.name}. Continuer ? (oui/non) "
    ).strip().lower()
    if confirmation not in {"oui", "o", "yes", "y"}:
        print("Restauration annulée.")
        return

    cmd = psql_base_command(config) + ["-f", str(backup_path)]
    print(f"Restauration depuis {backup_path} ...")
    result = subprocess.run(cmd, env=build_pg_env(config), capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else f"code {result.returncode}"
        sys.exit(f"Échec de la restauration : {stderr}")

    print("✅ Restauration terminée.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Restaure un dump SQL généré par db_backup.py")
    parser.add_argument(
        "-f",
        "--file",
        dest="backup_name",
        help="Nom du fichier dans scripts/backups/ (ou chemin complet si ailleurs).",
    )
    args = parser.parse_args()

    backup = select_backup(args.backup_name)
    restore_backup(backup)


if __name__ == "__main__":
    main()
