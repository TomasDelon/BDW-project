"""
Shared test helpers.

Ensures the `models` package inside website-morpion is importable without
requiring callers to tweak PYTHONPATH manually before running pytest/unittest.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
import types


def _install_dependency_stubs() -> None:
    """
    Create lightweight stand-ins for external dependencies (psycopg/logzero)
    so unit tests can import the project without requiring native packages.
    """
    if "psycopg" not in sys.modules:
        psycopg_stub = types.ModuleType("psycopg")

        class Error(Exception):
            pass

        psycopg_stub.Error = Error

        def connect(*args, **kwargs):  # pragma: no cover - never called in tests
            raise RuntimeError("psycopg stub does not support connections")

        psycopg_stub.connect = connect

        class SQL:
            def __init__(self, text: str):
                self.text = text

            def format(self, other):
                other_text = other.text if isinstance(other, SQL) else str(other)
                return SQL(self.text.format(other_text))

            def join(self, iterable):
                parts = [str(item.text if isinstance(item, SQL) else item) for item in iterable]
                return SQL(self.text.join(parts))

            def __str__(self):
                return self.text

        def Identifier(*parts):
            return SQL(".".join(str(p) for p in parts))

        sql_module = types.ModuleType("psycopg.sql")
        sql_module.SQL = SQL
        sql_module.Identifier = Identifier

        psycopg_stub.sql = sql_module

        class Connection:  # pragma: no cover - typing helper
            pass

        psycopg_stub.Connection = Connection

        rows_module = types.ModuleType("psycopg.rows")

        def dict_row(*args, **kwargs):  # pragma: no cover - placeholder
            return dict

        rows_module.dict_row = dict_row

        sys.modules["psycopg"] = psycopg_stub
        sys.modules["psycopg.sql"] = sql_module
        sys.modules["psycopg.rows"] = rows_module

    if "logzero" not in sys.modules:
        logzero_stub = types.ModuleType("logzero")

        class _Logger:
            def debug(self, *args, **kwargs):
                pass

            info = warning = error = debug

        logzero_stub.logger = _Logger()
        sys.modules["logzero"] = logzero_stub


def _ensure_website_package_on_path() -> None:
    root = Path(__file__).resolve().parents[1]
    extra_roots = [
        root / "website-morpion",
        root / "scripts",
    ]
    for extra in extra_roots:
        if not extra.exists():
            continue
        str_path = str(extra)
        if str_path not in sys.path:
            sys.path.insert(0, str_path)


_install_dependency_stubs()
_ensure_website_package_on_path()
