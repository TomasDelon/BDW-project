#!/usr/bin/env python3
"""
Utilitaires communs pour les scripts de base de données.
 - Lecture de config-bd.toml
 - Préparation des commandes psql/pg_dump
 - Connexion psycopg avec le bon search_path
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import psycopg
from psycopg import sql

try:
    import tomllib
except ModuleNotFoundError:
    sys.exit("Python 3.11+ est requis pour tomllib (ou installez tomli si vous restez en 3.10).")

ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = ROOT / "website-morpion" / "sql"
BACKUP_DIR = Path(__file__).resolve().parent / "backups"
CONFIG_PATH = ROOT / "config-bd.toml"

REQUIRED_KEYS = [
    "POSTGRESQL_SERVER",
    "POSTGRESQL_USER",
    "POSTGRESQL_PASSWORD",
    "POSTGRESQL_DATABASE",
    "POSTGRESQL_SCHEMA",
]


def load_config(config_path: Path = CONFIG_PATH) -> dict:
    """
    Charge le fichier TOML local et valide les champs attendus.
    """
    cfg_path = Path(config_path)
    if not cfg_path.exists():
        sys.exit(
            f"Fichier de configuration introuvable : {cfg_path}. "
            "Copiez config-bd.toml.example vers config-bd.toml puis renseignez vos identifiants."
        )

    with cfg_path.open("rb") as fh:
        raw = tomllib.load(fh)

    missing = [key for key in REQUIRED_KEYS if not raw.get(key)]
    if missing:
        sys.exit(f"Champs manquants dans {cfg_path} : {', '.join(missing)}.")

    return {
        "server": raw["POSTGRESQL_SERVER"],
        "user": raw["POSTGRESQL_USER"],
        "password": raw["POSTGRESQL_PASSWORD"],
        "database": raw["POSTGRESQL_DATABASE"],
        "schema": raw.get("POSTGRESQL_SCHEMA", "public"),
        "port": int(raw.get("POSTGRESQL_PORT", 5432)),
    }


def build_pg_env(config: dict) -> dict:
    """
    Prépare les variables d'environnement pour les outils CLI PostgreSQL.
    """
    env = os.environ.copy()
    if config.get("password"):
        env["PGPASSWORD"] = str(config["password"])
    env["PGOPTIONS"] = f"-c search_path={config['schema']}"
    return env


def require_binary(binary_name: str) -> None:
    """
    Vérifie que psql/pg_dump sont disponibles côté client.
    """
    if shutil.which(binary_name) is None:
        sys.exit(
            f"Commande requise introuvable : {binary_name}. "
            "Installez les utilitaires client PostgreSQL (psql / pg_dump)."
        )


def psql_base_command(config: dict) -> list[str]:
    """
    Prépare les arguments communs pour psql.
    """
    return [
        "psql",
        "-h",
        config["server"],
        "-p",
        str(config["port"]),
        "-U",
        config["user"],
        "-d",
        config["database"],
        "--set",
        "ON_ERROR_STOP=on",
    ]


def run_sql_file_with_psql(sql_path: Path, config: dict) -> None:
    """
    Exécute un fichier SQL via psql en stoppant dès la première erreur.
    """
    require_binary("psql")
    resolved = Path(sql_path)
    if not resolved.exists():
        sys.exit(f"Script SQL introuvable : {resolved}")

    cmd = psql_base_command(config) + ["-f", str(resolved)]
    result = subprocess.run(cmd, env=build_pg_env(config), capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else f"code {result.returncode}"
        sys.exit(f"Echec lors de l'exécution de {resolved.name} : {stderr}")


def open_connection(config: dict) -> psycopg.Connection:
    """
    Retourne une connexion psycopg avec autocommit et search_path appliqué.
    """
    try:
        connexion = psycopg.connect(
            host=config["server"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            dbname=config["database"],
            autocommit=True,
        )
        connexion.execute(
            sql.SQL("SET search_path TO {}").format(sql.Identifier(config["schema"]))
        )
        return connexion
    except Exception as exc:  # pragma: no cover - utile en mode CLI
        sys.exit(f"Connexion impossible avec les paramètres fournis : {exc}")
