from __future__ import annotations

from pathlib import Path
import re
import sys

import yaml


CATEGORIES = {"methodology", "data", "metrics", "implementation", "environment", "compute"}
ENFORCEMENT = {"BLOCK", "WARN"}
STATUS = {"ACTIVE", "CONTESTED", "SUPERSEDED"}
MAX_RAW_SUMMARY_BYTES = 2048
MAX_ERROR_EXCERPT_LINES = 20
SENSITIVE_KEYS = {"host", "ssh_user", "identity_file", "credential", "token", "password"}

MAX_YAML_BYTES = 65536
MAX_INDEX_ENTRIES = 10000
LESSON_ID_PATTERN = re.compile(r"L[0-9]{6}\Z")
GIT_SHA_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
SOURCE_FINGERPRINT_PATTERN = re.compile(r"sha256:[0-9a-f]{64}\Z")
WINDOWS_ABSOLUTE_PATTERN = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")
POSIX_ABSOLUTE_PATTERN = re.compile(r"(?<![A-Za-z0-9/:])/(?![/\s])")
PARENT_TRAVERSAL_PATTERN = re.compile(r"(?<![A-Za-z0-9.])\.\.[\\/]")
UNC_PATH_PATTERN = re.compile(r"\\\\[^\\\s]+[\\/]")


def _bounded_label(value: object, limit: int = 80) -> str:
    text = str(value)
    return text if len(text) <= limit else text[:limit] + "..."


def _read_yaml(path: Path, label: str) -> tuple[object | None, list[str]]:
    if not path.is_file():
        return None, [f"{label}: missing YAML file"]
    try:
        size = path.stat().st_size
    except OSError:
        return None, [f"{label}: cannot inspect YAML file"]
    if size > MAX_YAML_BYTES:
        return None, [f"{label}: YAML file exceeds {MAX_YAML_BYTES} bytes"]
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, yaml.YAMLError):
        return None, [f"{label}: invalid UTF-8 YAML"]


def _load_schema(root: Path) -> tuple[dict | None, list[str]]:
    value, errors = _read_yaml(root / "SCHEMA.yaml", "SCHEMA.yaml")
    if errors:
        return None, errors
    if not isinstance(value, dict):
        return None, ["SCHEMA.yaml: top level must be a mapping"]
    if value.get("schema_version") != 1:
        return None, ["SCHEMA.yaml: schema_version must be 1"]
    card = value.get("card")
    index = value.get("index")
    if not isinstance(card, dict) or not isinstance(card.get("fields"), list):
        return None, ["SCHEMA.yaml: card.fields must be a list"]
    if not isinstance(index, dict) or not isinstance(index.get("fields"), list):
        return None, ["SCHEMA.yaml: index.fields must be a list"]
    if not isinstance(index.get("entry_fields"), list):
        return None, ["SCHEMA.yaml: index.entry_fields must be a list"]
    return value, []


def _root_for_card(path: Path) -> Path | None:
    for candidate in path.parents:
        if (candidate / "SCHEMA.yaml").is_file():
            return candidate
    return None


def _unsafe_path_text(value: str) -> bool:
    candidate = value.strip()
    return bool(
        candidate.startswith("\\")
        or WINDOWS_ABSOLUTE_PATTERN.search(candidate)
        or POSIX_ABSOLUTE_PATTERN.search(candidate)
        or PARENT_TRAVERSAL_PATTERN.search(candidate)
        or UNC_PATH_PATTERN.search(candidate)
    )


def _sensitive_key_errors(value: object, location: str = "card") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if key_text.lower() in SENSITIVE_KEYS:
                errors.append(
                    f"{location}: sensitive field '{_bounded_label(key_text)}' is forbidden"
                )
            errors.extend(_sensitive_key_errors(child, location))
    elif isinstance(value, list):
        for child in value:
            errors.extend(_sensitive_key_errors(child, location))
    return errors


def _closed_fields(
    value: dict, expected: list[object], location: str
) -> list[str]:
    errors: list[str] = []
    expected_names = {item for item in expected if isinstance(item, str)}
    actual_names = {item for item in value if isinstance(item, str)}
    for name in sorted(expected_names - actual_names):
        errors.append(f"{location}: missing field '{_bounded_label(name)}'")
    for name in sorted(actual_names - expected_names):
        errors.append(f"{location}: unexpected field '{_bounded_label(name)}'")
    if any(not isinstance(item, str) for item in value):
        errors.append(f"{location}: field names must be text")
    return errors


def _text_errors(
    value: object, field: str, maximum_bytes: int, *, allow_empty: bool = False
) -> list[str]:
    if not isinstance(value, str):
        return [f"card: {field} must be text"]
    errors: list[str] = []
    if not allow_empty and not value.strip():
        errors.append(f"card: {field} must not be empty")
    if len(value.encode("utf-8")) > maximum_bytes:
        errors.append(f"card: {field} exceeds {maximum_bytes} bytes")
    if _unsafe_path_text(value):
        errors.append(f"card: {field} contains an unsafe path")
    return errors


def _text_list_errors(
    value: object,
    field: str,
    maximum_items: int,
    maximum_item_bytes: int,
    *,
    allow_empty: bool = False,
) -> list[str]:
    if not isinstance(value, list):
        return [f"card: {field} must be a list"]
    errors: list[str] = []
    if len(value) > maximum_items:
        errors.append(f"card: {field} exceeds {maximum_items} items")
    if not allow_empty and not value:
        errors.append(f"card: {field} must not be empty")
    for item in value:
        errors.extend(_text_errors(item, field, maximum_item_bytes))
    return errors


def _validate_card_data(path: Path, value: dict, schema: dict) -> list[str]:
    errors = _closed_fields(value, schema["card"]["fields"], "card")
    errors.extend(_sensitive_key_errors(value))

    if type(value.get("schema_version")) is not int or value.get("schema_version") != 1:
        errors.append("card: schema_version must be 1")

    errors.extend(_text_errors(value.get("lesson_id"), "lesson_id", 7))
    lesson_id = value.get("lesson_id")
    if isinstance(lesson_id, str) and not LESSON_ID_PATTERN.fullmatch(lesson_id):
        errors.append("card: lesson_id must match L followed by six digits")

    errors.extend(_text_errors(value.get("title"), "title", 200))
    errors.extend(_text_errors(value.get("category"), "category", 32))
    category = value.get("category")
    if category not in CATEGORIES:
        errors.append("card: category is not canonical")

    errors.extend(_text_list_errors(value.get("tags"), "tags", 16, 64))
    errors.extend(_text_list_errors(value.get("applies_when"), "applies_when", 16, 512))
    errors.extend(
        _text_list_errors(
            value.get("not_applicable_when"), "not_applicable_when", 16, 512
        )
    )
    errors.extend(
        _text_list_errors(value.get("failure_signature"), "failure_signature", 16, 512)
    )
    errors.extend(_text_errors(value.get("root_cause"), "root_cause", 2048))
    errors.extend(_text_errors(value.get("confidence"), "confidence", 16))
    if value.get("confidence") not in {"LOW", "MEDIUM", "HIGH"}:
        errors.append("card: confidence must be LOW, MEDIUM, or HIGH")
    for field in ("detection", "prevention", "recovery"):
        errors.extend(_text_list_errors(value.get(field), field, 16, 512))

    errors.extend(
        _text_errors(
            value.get("raw_evidence_summary"),
            "raw_evidence_summary",
            MAX_RAW_SUMMARY_BYTES,
            allow_empty=True,
        )
    )
    excerpt = value.get("error_excerpt")
    errors.extend(
        _text_list_errors(
            excerpt,
            "error_excerpt",
            MAX_ERROR_EXCERPT_LINES,
            512,
            allow_empty=True,
        )
    )
    if isinstance(excerpt, list) and all(isinstance(item, str) for item in excerpt):
        line_count = sum(item.count("\n") + 1 for item in excerpt)
        if line_count > MAX_ERROR_EXCERPT_LINES:
            errors.append(
                f"card: error_excerpt exceeds {MAX_ERROR_EXCERPT_LINES} lines"
            )

    errors.extend(_text_errors(value.get("enforcement"), "enforcement", 8))
    if value.get("enforcement") not in ENFORCEMENT:
        errors.append("card: enforcement must be BLOCK or WARN")
    for field in ("deterministic", "reproducible", "uncontested"):
        if type(value.get(field)) is not bool:
            errors.append(f"card: {field} must be boolean")

    errors.extend(
        _text_errors(value.get("source_fingerprint"), "source_fingerprint", 80)
    )
    source_fingerprint = value.get("source_fingerprint")
    if isinstance(source_fingerprint, str) and not SOURCE_FINGERPRINT_PATTERN.fullmatch(
        source_fingerprint
    ):
        errors.append("card: source_fingerprint must be a sha256 fingerprint")
    for field in ("created_sha", "revised_sha"):
        errors.extend(_text_errors(value.get(field), field, 40))
        sha = value.get(field)
        if isinstance(sha, str) and not GIT_SHA_PATTERN.fullmatch(sha):
            errors.append(f"card: {field} must be a 40-character lowercase Git SHA")

    errors.extend(_text_errors(value.get("status"), "status", 16))
    if value.get("status") not in STATUS:
        errors.append("card: status is not canonical")

    if value.get("enforcement") == "BLOCK":
        if value.get("status") != "ACTIVE":
            errors.append("card: BLOCK requires status ACTIVE")
        for field in ("deterministic", "reproducible", "uncontested"):
            if value.get(field) is not True:
                errors.append(f"card: BLOCK requires {field} true")

    root = _root_for_card(path)
    if root is not None:
        try:
            relative = path.resolve().relative_to(root.resolve())
        except (OSError, ValueError):
            errors.append("card: file location is an unsafe path")
        else:
            parts = relative.parts
            if len(parts) != 3 or parts[0] != "cards":
                errors.append("card: file must be cards/<category>/<lesson_id>.yaml")
            else:
                if isinstance(category, str) and parts[1] != category:
                    errors.append("card: category does not match file path")
                if isinstance(lesson_id, str) and parts[2] != f"{lesson_id}.yaml":
                    errors.append("card: lesson_id does not match file name")
    return errors


def validate_card(path: Path) -> list[str]:
    path = Path(path)
    root = _root_for_card(path)
    if root is None:
        return ["card: cannot locate SCHEMA.yaml"]
    schema, errors = _load_schema(root)
    if errors or schema is None:
        return errors
    if path.is_symlink():
        return ["card: symbolic links are forbidden"]
    value, read_errors = _read_yaml(path, path.name)
    if read_errors:
        return read_errors
    if not isinstance(value, dict):
        return ["card: top level must be a mapping"]
    return _validate_card_data(path, value, schema)


def _index_path_errors(value: object) -> list[str]:
    if not isinstance(value, str) or not value:
        return ["INDEX.yaml: entry path must be non-empty text"]
    if _unsafe_path_text(value):
        return ["INDEX.yaml: entry path contains an unsafe path"]
    if "\\" in value:
        return ["INDEX.yaml: entry path must use forward slashes"]
    parts = value.split("/")
    if (
        len(parts) != 3
        or parts[0] != "cards"
        or parts[1] not in CATEGORIES
        or not parts[2].endswith(".yaml")
    ):
        return ["INDEX.yaml: entry path must be cards/<category>/<lesson_id>.yaml"]
    return []


def validate_repository(root: Path) -> list[str]:
    root = Path(root)
    errors: list[str] = []
    if not root.is_dir():
        return ["repository: root must be a directory"]

    schema, schema_errors = _load_schema(root)
    errors.extend(schema_errors)
    if schema is None:
        return errors

    for category in sorted(CATEGORIES):
        if not (root / "cards" / category).is_dir():
            errors.append(f"repository: missing category directory cards/{category}")

    index, index_errors = _read_yaml(root / "INDEX.yaml", "INDEX.yaml")
    errors.extend(index_errors)
    if index_errors:
        return errors
    if not isinstance(index, dict):
        return errors + ["INDEX.yaml: top level must be a mapping"]
    errors.extend(_closed_fields(index, schema["index"]["fields"], "INDEX.yaml"))
    errors.extend(_sensitive_key_errors(index, "INDEX.yaml"))
    if type(index.get("schema_version")) is not int or index.get("schema_version") != 1:
        errors.append("INDEX.yaml: schema_version must be 1")
    entries = index.get("entries")
    if not isinstance(entries, list):
        return errors + ["INDEX.yaml: entries must be a list"]
    if len(entries) > MAX_INDEX_ENTRIES:
        errors.append(f"INDEX.yaml: entries exceeds {MAX_INDEX_ENTRIES} items")

    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    declared_paths: set[str] = set()
    root_resolved = root.resolve()

    for number, entry in enumerate(entries, start=1):
        location = f"INDEX.yaml entry {number}"
        if not isinstance(entry, dict):
            errors.append(f"{location}: must be a mapping")
            continue
        errors.extend(_closed_fields(entry, schema["index"]["entry_fields"], location))
        errors.extend(_sensitive_key_errors(entry, location))
        lesson_id = entry.get("lesson_id")
        index_path = entry.get("path")
        if isinstance(lesson_id, str):
            if lesson_id in seen_ids:
                errors.append(f"{location}: duplicate lesson_id")
            seen_ids.add(lesson_id)
        else:
            errors.append(f"{location}: lesson_id must be text")
        path_errors = _index_path_errors(index_path)
        errors.extend(f"{location}: {item.split(': ', 1)[-1]}" for item in path_errors)
        if not isinstance(index_path, str) or path_errors:
            continue
        if index_path in seen_paths:
            errors.append(f"{location}: duplicate path")
        seen_paths.add(index_path)
        declared_paths.add(index_path)

        card_path = root.joinpath(*index_path.split("/"))
        try:
            card_path.resolve().relative_to(root_resolved)
        except (OSError, ValueError):
            errors.append(f"{location}: resolved path escapes repository")
            continue
        if not card_path.is_file():
            errors.append(f"{location}: card file is missing")
            continue
        card_label = _bounded_label(index_path)
        errors.extend(f"{card_label}: {item}" for item in validate_card(card_path))
        card, card_read_errors = _read_yaml(card_path, index_path)
        if card_read_errors or not isinstance(card, dict):
            continue
        for field in ("lesson_id", "category", "title", "tags", "enforcement", "status"):
            if entry.get(field) != card.get(field):
                errors.append(f"{location}: {field} does not match card")

    cards_root = root / "cards"
    if cards_root.is_dir():
        actual_cards = {
            path.relative_to(root).as_posix()
            for path in cards_root.rglob("*")
            if path.is_file() and path.suffix.lower() in {".yaml", ".yml"}
        }
        for undeclared in sorted(actual_cards - declared_paths):
            errors.append(f"repository: undeclared YAML card '{_bounded_label(undeclared)}'")
    return errors


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) > 1:
        print("ERROR: expected at most one repository path")
        return 1
    root = Path(arguments[0]) if arguments else Path(".")
    errors = validate_repository(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
