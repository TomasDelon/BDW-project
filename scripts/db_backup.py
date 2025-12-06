#!/usr/bin/env python3
"""
Sauvegarde le schéma morpion (structure + données) dans scripts/backups/.
Utilise pg_dump avec --clean pour pouvoir restaurer facilement.
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from db_utils import BACKUP_DIR, ROOT, build_pg_env, load_config, require_binary


def make_backup() -> None:
    config = load_config()
    require_binary("pg_dump")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = BACKUP_DIR / f"backup_morpion_{timestamp}.sql"

    cmd = [
        "pg_dump",
        "-h",
        config["server"],
        "-p",
        str(config["port"]),
        "-U",
        config["user"],
        "-d",
        config["database"],
        "-n",
        config["schema"],
        "--format=plain",
        "--clean",
        "--if-exists",
        "--no-owner",
        "--file",
        str(backup_file),
    ]

    print(f"Export du schéma '{config['schema']}' vers {backup_file} ...")
    result = subprocess.run(cmd, env=build_pg_env(config), capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else f"code {result.returncode}"
        sys.exit(f"Échec de la sauvegarde : {stderr}")

    rel_path = backup_file.relative_to(ROOT)
    print(f"Sauvegarde terminée : {rel_path}")


if __name__ == "__main__":
    make_backup()
