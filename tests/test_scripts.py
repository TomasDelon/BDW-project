from __future__ import annotations

import io
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import db_backup
import db_restore
import db_wipe
import build_css


class DBScriptsTests(unittest.TestCase):
    def test_db_backup_runs_pg_dump_with_expected_arguments(self):
        temp_dir = Path(tempfile.mkdtemp())
        backup_dir = temp_dir / "backups"
        with (
            patch.object(db_backup, "BACKUP_DIR", backup_dir),
            patch.object(db_backup, "ROOT", temp_dir),
            patch.object(db_backup, "load_config", return_value={
                "server": "localhost",
                "port": 5432,
                "user": "user",
                "database": "db",
                "schema": "morpion",
            }),
            patch.object(db_backup, "build_pg_env", return_value={"PGPASSWORD": "x"}),
            patch.object(db_backup, "require_binary"),
            patch.object(db_backup, "datetime") as mock_datetime,
            patch.object(db_backup.subprocess, "run", return_value=SimpleNamespace(returncode=0, stderr="")) as mock_run,
        ):
            mock_datetime.now.return_value.strftime.return_value = "20240101-010203"
            db_backup.make_backup()

        self.assertTrue((backup_dir).exists())
        cmd = mock_run.call_args.args[0]
        self.assertEqual(cmd[0], "pg_dump")
        self.assertIn("--file", cmd)
        backup_index = cmd.index("--file") + 1
        self.assertTrue(cmd[backup_index].endswith("backup_morpion_20240101-010203.sql"))

    def test_db_backup_exits_on_failure(self):
        temp_dir = Path(tempfile.mkdtemp())
        backup_dir = temp_dir / "backups"
        with (
            patch.object(db_backup, "BACKUP_DIR", backup_dir),
            patch.object(db_backup, "ROOT", temp_dir),
            patch.object(db_backup, "load_config", return_value={
                "server": "localhost",
                "port": 5432,
                "user": "user",
                "database": "db",
                "schema": "morpion",
            }),
            patch.object(db_backup, "build_pg_env", return_value={}),
            patch.object(db_backup, "require_binary"),
            patch.object(db_backup, "datetime") as mock_datetime,
            patch.object(
                db_backup.subprocess,
                "run",
                return_value=SimpleNamespace(returncode=1, stderr="boom"),
            ),
        ):
            mock_datetime.now.return_value.strftime.return_value = "20240101-010203"
            with self.assertRaises(SystemExit) as ctx:
                db_backup.make_backup()
            self.assertIn("boom", str(ctx.exception))

    def test_db_restore_runs_psql_after_confirmation(self):
        backup_file = Path(tempfile.mkdtemp()) / "dump.sql"
        backup_file.write_text("-- sql")
        with (
            patch.object(db_restore, "load_config", return_value={"schema": "morpion"}),
            patch.object(db_restore, "require_binary"),
            patch.object(db_restore, "build_pg_env", return_value={"PGPASSWORD": "x"}),
            patch.object(db_restore, "psql_base_command", return_value=["psql", "-h", "localhost"]),
            patch.object(db_restore.subprocess, "run", return_value=SimpleNamespace(returncode=0, stderr="")) as mock_run,
            patch("builtins.input", return_value="oui"),
        ):
            db_restore.restore_backup(backup_file)
        mock_run.assert_called_once()
        self.assertIn(str(backup_file), mock_run.call_args.args[0])

    def test_db_restore_aborts_on_error(self):
        backup_file = Path(tempfile.mkdtemp()) / "dump.sql"
        backup_file.write_text("-- sql")
        with (
            patch.object(db_restore, "load_config", return_value={"schema": "morpion"}),
            patch.object(db_restore, "require_binary"),
            patch.object(db_restore, "build_pg_env", return_value={}),
            patch.object(db_restore, "psql_base_command", return_value=["psql"]),
            patch.object(db_restore.subprocess, "run", return_value=SimpleNamespace(returncode=2, stderr="psql error")),
            patch("builtins.input", return_value="oui"),
        ):
            with self.assertRaises(SystemExit) as ctx:
                db_restore.restore_backup(backup_file)
            self.assertIn("psql error", str(ctx.exception))

    def test_db_wipe_executes_truncate_when_confirmed(self):
        fake_connection = MagicMock()
        context_manager = MagicMock()
        context_manager.__enter__.return_value = fake_connection
        with (
            patch.object(db_wipe, "load_config", return_value={"schema": "public"}),
            patch.object(db_wipe, "open_connection", return_value=context_manager),
            patch("builtins.input", return_value="y"),
        ):
            db_wipe.wipe_schema()
        fake_connection.execute.assert_called_once()

    def test_db_wipe_aborts_without_confirmation(self):
        with (
            patch.object(db_wipe, "load_config", return_value={"schema": "public"}),
            patch.object(db_wipe, "open_connection") as mock_conn,
            patch("builtins.input", return_value="non"),
        ):
            db_wipe.wipe_schema()
        mock_conn.assert_not_called()


class BuildCssScriptTests(unittest.TestCase):
    def test_build_css_generates_bundle(self):
        temp_dir = Path(tempfile.mkdtemp())
        styles_dir = temp_dir / "styles"
        (styles_dir / "components").mkdir(parents=True)
        sources = ["base.css", "components/buttons.css"]
        for rel_path in sources:
            target = styles_dir / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"/* {rel_path} */\nbody {{ color: red; }}\n")

        output_file = temp_dir / "main.css"
        with (
            patch.object(build_css, "STYLES_DIR", styles_dir),
            patch.object(build_css, "OUTPUT_FILE", output_file),
            patch.object(build_css, "CSS_SOURCES", sources),
            patch.object(build_css, "ROOT", temp_dir),
        ):
            build_css.main()

        content = output_file.read_text()
        self.assertIn("Auto-generated", content)
        for rel_path in sources:
            self.assertIn(f"=== {rel_path} ===", content)


if __name__ == "__main__":
    unittest.main()
