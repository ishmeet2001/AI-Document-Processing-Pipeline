import importlib
import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = PROJECT_ROOT / "src" / "unstructured-data-pipeline"

for path in (PROJECT_ROOT / "src", PACKAGE_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


def reload_module(module_name: str):
    module = importlib.import_module(module_name)
    return importlib.reload(module)


def call_tool_or_func(target, *args, **kwargs):
    """Call a function or a LangChain tool (which wraps the function in .func)."""
    if hasattr(target, "func"):
        return target.func(*args, **kwargs)
    return target(*args, **kwargs)


def load_config_module():
    """Load config.py directly from disk to avoid path resolution issues."""
    config_path = PACKAGE_ROOT / "config.py"
    spec = importlib.util.spec_from_file_location("config", config_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load config from {config_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["config"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(autouse=True)
def test_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("FILES_STORAGE", str(tmp_path / "test_db.sqlite"))
    monkeypatch.setenv("FILE_TYPES_ALLOWED", "txt")
    monkeypatch.setenv("PROCESS_COMMAND", "process <input_path> --db <output_db_path>")
    monkeypatch.setenv("GOOGLE_GEMINI_API_KEY", "test-api-key")

    load_config_module()
    yield


def test_validate_file_rules(test_environment, tmp_path):
    file_naming = reload_module("domain.validators.file_naming")

    assert file_naming.validate_empty_path("") is False
    assert file_naming.validate_empty_path("invoice.txt") is True

    assert file_naming.validate_file_type("note.txt") is True
    assert file_naming.validate_file_type("note.pdf") is False

    existing = tmp_path / "sample.txt"
    existing.write_text("hello")
    assert file_naming.validate_file_existence(str(existing)) is True
    assert file_naming.validate_file_existence(str(existing.with_suffix(".missing"))) is False


def test_read_files_collects_only_valid_txt(test_environment, tmp_path):
    cli_main = reload_module("infrastructure.CLI.main")

    valid_file = tmp_path / "invoice.txt"
    valid_file.write_text("valid content")

    invalid_ext = tmp_path / "notes.md"
    invalid_ext.write_text("invalid content")

    missing_file = tmp_path / "missing.txt"

    result = cli_main.read_files(
        [str(valid_file), str(invalid_ext), str(missing_file)]
    )

    assert result == {"valid content"}


def test_db_file_creation_and_existence(test_environment, tmp_path):
    file_creation = reload_module("domain.tools.file_creation")
    db_path = Path(reload_module("config").GENERATED_SCHEMA_PATH)

    assert call_tool_or_func(file_creation.check_DBfile_existence, str(db_path)) is False

    creation_result = call_tool_or_func(file_creation.db_file_creation, str(db_path))
    assert "Created Successfully" in creation_result
    assert db_path.exists() is True


def test_sql_execution_creates_and_inserts_data(test_environment):
    sql_execution = reload_module("domain.tools.sql_execution")
    db_path = Path(reload_module("config").GENERATED_SCHEMA_PATH)

    create_and_insert = """
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY,
        sender TEXT,
        amount REAL
    );
    INSERT INTO invoices (sender, amount) VALUES ('Acme Corp', 123.45);
    """

    result = call_tool_or_func(sql_execution.manipulating_DBTable, create_and_insert, path=str(db_path))
    assert "successfully" in result

    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute("SELECT sender, amount FROM invoices")
        row = cursor.fetchone()

    assert row == ("Acme Corp", 123.45)


def test_read_files_stateless_sequential_calls(test_environment, tmp_path):
    cli_main = reload_module("infrastructure.CLI.main")

    file_a = tmp_path / "file_a.txt"
    file_a.write_text("content A")

    file_b = tmp_path / "file_b.txt"
    file_b.write_text("content B")

    # First call processing file_a
    result_1 = cli_main.read_files([str(file_a)])
    assert result_1 == {"content A"}

    # Second call processing file_b (should NOT contain "content A")
    result_2 = cli_main.read_files([str(file_b)])
    assert result_2 == {"content B"}





