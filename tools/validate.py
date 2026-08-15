from __future__ import annotations

import os
from pathlib import Path
import re
import stat
import sys

import yaml
from yaml.events import AliasEvent
from yaml.resolver import BaseResolver


CATEGORIES = {"methodology", "data", "metrics", "implementation", "environment", "compute"}
ENFORCEMENT = {"BLOCK", "WARN"}
STATUS = {"ACTIVE", "CONTESTED", "SUPERSEDED"}
MAX_RAW_SUMMARY_BYTES = 2048
MAX_ERROR_EXCERPT_LINES = 20
SENSITIVE_KEYS = {"host", "ssh_user", "identity_file", "credential", "token", "password"}

MAX_YAML_BYTES = 65536
MAX_INDEX_ENTRIES = 10000
MAX_ERRORS = 100
MAX_OUTPUT_BYTES = 8192
MAX_ERROR_MESSAGE_BYTES = 512
OMITTED_ERRORS = "remaining errors omitted"
CONFIDENCE = {"LOW", "MEDIUM", "HIGH"}
CARD_FIELDS = [
    "schema_version",
    "lesson_id",
    "title",
    "category",
    "tags",
    "applies_when",
    "not_applicable_when",
    "failure_signature",
    "root_cause",
    "confidence",
    "detection",
    "prevention",
    "recovery",
    "raw_evidence_summary",
    "error_excerpt",
    "enforcement",
    "deterministic",
    "reproducible",
    "uncontested",
    "source_fingerprint",
    "created_sha",
    "revised_sha",
    "status",
]
INDEX_FIELDS = ["schema_version", "entries"]
INDEX_ENTRY_FIELDS = [
    "lesson_id",
    "path",
    "category",
    "title",
    "tags",
    "enforcement",
    "status",
]
TEXT_LIMITS = {
    "title": 200,
    "tag": 64,
    "condition": 512,
    "failure_signature": 512,
    "root_cause": 2048,
    "action": 512,
    "raw_evidence_summary": MAX_RAW_SUMMARY_BYTES,
    "error_excerpt_line": 512,
    "source_fingerprint": 80,
}
LIST_LIMITS = {
    "tags": 16,
    "applies_when": 16,
    "not_applicable_when": 16,
    "failure_signature": 16,
    "detection": 16,
    "prevention": 16,
    "recovery": 16,
    "error_excerpt_lines": MAX_ERROR_EXCERPT_LINES,
}
CANONICAL_SCHEMA = {
    "schema_version": 1,
    "card": {
        "additional_fields": False,
        "fields": CARD_FIELDS,
        "categories": [
            "methodology",
            "data",
            "metrics",
            "implementation",
            "environment",
            "compute",
        ],
        "enforcement": ["BLOCK", "WARN"],
        "status": ["ACTIVE", "CONTESTED", "SUPERSEDED"],
        "confidence": ["LOW", "MEDIUM", "HIGH"],
        "text_limits_bytes": TEXT_LIMITS,
        "list_limits": LIST_LIMITS,
    },
    "index": {
        "additional_fields": False,
        "fields": INDEX_FIELDS,
        "entry_fields": INDEX_ENTRY_FIELDS,
    },
}
LESSON_ID_PATTERN = re.compile(r"L[0-9]{6}\Z")
GIT_SHA_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
SOURCE_FINGERPRINT_PATTERN = re.compile(r"sha256:[0-9a-f]{64}\Z")
SAFE_NETWORK_URL_PATTERN = re.compile(
    r"(?<!\w)(?:https?://|//)"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,})"
    r"(?::[0-9]{1,5})?(?:[/?#][^\s]*)?",
    re.IGNORECASE,
)
FILE_URI_PATTERN = re.compile(r"(?<!\w)file:(?:/{1,3}|\\\\)", re.IGNORECASE)
WINDOWS_ABSOLUTE_PATTERN = re.compile(r"(?<!\w)[A-Za-z]:[\\/]")
POSIX_ABSOLUTE_PATTERN = re.compile(r"(?<!\w)/(?![/\s])")
PARENT_TRAVERSAL_PATTERN = re.compile(r"(?<!\w)\.\.[\\/]")
UNC_PATH_PATTERN = re.compile(r"\\\\[^\\\s]+[\\/]")


class _StrictSafeLoader(yaml.SafeLoader):
    def compose_node(self, parent: object, index: object) -> yaml.Node:
        if self.check_event(AliasEvent):
            raise yaml.YAMLError("aliases are forbidden")
        return super().compose_node(parent, index)


def _construct_unique_mapping(
    loader: _StrictSafeLoader, node: yaml.MappingNode, deep: bool = False
) -> dict:
    loader.flatten_mapping(node)
    mapping: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise yaml.YAMLError("mapping keys must be hashable") from error
        if duplicate:
            raise yaml.YAMLError("duplicate mapping key")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_StrictSafeLoader.add_constructor(
    BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def _errors_full(errors: list[str]) -> bool:
    return bool(errors) and errors[-1] == OMITTED_ERRORS


def _add_error(errors: list[str], error: str) -> bool:
    if _errors_full(errors):
        return False
    if len(errors) < MAX_ERRORS:
        errors.append(error)
        return True
    errors.append(OMITTED_ERRORS)
    return False


def _extend_errors(errors: list[str], additions: list[str]) -> bool:
    for addition in additions:
        if not _add_error(errors, addition):
            return False
    return not _errors_full(errors)


def _bounded_message(value: object, maximum_bytes: int) -> str:
    encoded = str(value).encode("utf-8")
    if len(encoded) <= maximum_bytes:
        return encoded.decode("utf-8")
    return encoded[: maximum_bytes - 3].decode("utf-8", errors="ignore") + "..."


def _bounded_label(value: object, limit: int = 80) -> str:
    text = str(value)
    return text if len(text) <= limit else text[:limit] + "..."


def _is_link_or_reparse(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    if is_junction is not None and is_junction():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _no_follow_error(root: Path, path: Path, label: str) -> str | None:
    try:
        root_absolute = Path(os.path.abspath(root))
        path_absolute = Path(os.path.abspath(path))
        relative = path_absolute.relative_to(root_absolute)
    except (OSError, ValueError):
        return f"{label}: path escapes repository"

    current = root_absolute
    try:
        if _is_link_or_reparse(current):
            return f"{label}: link or reparse point is forbidden"
        for part in relative.parts:
            current = current / part
            if _is_link_or_reparse(current):
                return f"{label}: link or reparse point is forbidden"
        resolved_root = root_absolute.resolve(strict=True)
        current.resolve(strict=False).relative_to(resolved_root)
    except (OSError, ValueError):
        return f"{label}: path cannot be safely resolved"
    return None


def _read_yaml(
    path: Path, label: str, *, root: Path | None = None
) -> tuple[object | None, list[str]]:
    if root is not None:
        safety_error = _no_follow_error(root, path, label)
        if safety_error is not None:
            return None, [safety_error]
    if not path.is_file():
        return None, [f"{label}: missing YAML file"]
    try:
        size = path.stat().st_size
    except OSError:
        return None, [f"{label}: cannot inspect YAML file"]
    if size > MAX_YAML_BYTES:
        return None, [f"{label}: YAML file exceeds {MAX_YAML_BYTES} bytes"]
    try:
        text = path.read_text(encoding="utf-8")
        return yaml.load(text, Loader=_StrictSafeLoader), []
    except (OSError, UnicodeError, yaml.YAMLError, RecursionError, MemoryError, ValueError):
        return None, [f"{label}: invalid YAML"]


def _load_schema(root: Path) -> tuple[dict | None, list[str]]:
    value, errors = _read_yaml(root / "SCHEMA.yaml", "SCHEMA.yaml", root=root)
    if errors:
        return None, errors
    if not isinstance(value, dict):
        return None, ["SCHEMA.yaml: top level must be a mapping"]
    if value != CANONICAL_SCHEMA:
        return None, ["SCHEMA.yaml: metadata does not match canonical schema"]
    return value, []


def _root_for_card(path: Path) -> Path | None:
    for candidate in path.parents:
        if os.path.lexists(candidate / "SCHEMA.yaml"):
            return candidate
    return None


def _unsafe_path_text(value: str) -> bool:
    candidate = value.strip()
    without_network_urls = SAFE_NETWORK_URL_PATTERN.sub("", candidate)
    return bool(
        FILE_URI_PATTERN.search(candidate)
        or without_network_urls.startswith("\\")
        or WINDOWS_ABSOLUTE_PATTERN.search(without_network_urls)
        or POSIX_ABSOLUTE_PATTERN.search(without_network_urls)
        or PARENT_TRAVERSAL_PATTERN.search(without_network_urls)
        or UNC_PATH_PATTERN.search(without_network_urls)
    )


def _sensitive_key_errors(value: object, location: str = "card") -> list[str]:
    errors: list[str] = []
    stack = [value]
    visited = 0
    while stack and not _errors_full(errors):
        current = stack.pop()
        visited += 1
        if visited > MAX_INDEX_ENTRIES:
            _add_error(errors, OMITTED_ERRORS)
            break
        if isinstance(current, dict):
            for key, child in current.items():
                key_text = str(key)
                if key_text.lower() in SENSITIVE_KEYS:
                    if not _add_error(
                        errors,
                        f"{location}: sensitive field '{_bounded_label(key_text)}' is forbidden",
                    ):
                        break
                stack.append(child)
        elif isinstance(current, list):
            stack.extend(current)
    return errors


def _closed_fields(
    value: dict, expected: list[object], location: str
) -> list[str]:
    errors: list[str] = []
    expected_names = {item for item in expected if isinstance(item, str)}
    actual_names = {item for item in value if isinstance(item, str)}
    for name in sorted(expected_names - actual_names):
        if not _add_error(errors, f"{location}: missing field '{_bounded_label(name)}'"):
            return errors
    for name in sorted(actual_names - expected_names):
        if not _add_error(
            errors, f"{location}: unexpected field '{_bounded_label(name)}'"
        ):
            return errors
    if any(not isinstance(item, str) for item in value):
        _add_error(errors, f"{location}: field names must be text")
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
        if not _extend_errors(
            errors, _text_errors(item, field, maximum_item_bytes)
        ):
            break
    return errors


def _validate_card_data(path: Path, value: dict, schema: dict) -> list[str]:
    errors = _closed_fields(value, schema["card"]["fields"], "card")
    _extend_errors(errors, _sensitive_key_errors(value))
    card_schema = schema["card"]
    text_limits = card_schema["text_limits_bytes"]
    list_limits = card_schema["list_limits"]
    categories = set(card_schema["categories"])
    confidence = set(card_schema["confidence"])
    enforcement = set(card_schema["enforcement"])
    statuses = set(card_schema["status"])

    if type(value.get("schema_version")) is not int or value.get("schema_version") != 1:
        _add_error(errors, "card: schema_version must be 1")

    _extend_errors(errors, _text_errors(value.get("lesson_id"), "lesson_id", 7))
    lesson_id = value.get("lesson_id")
    if isinstance(lesson_id, str) and not LESSON_ID_PATTERN.fullmatch(lesson_id):
        _add_error(errors, "card: lesson_id must match L followed by six digits")

    _extend_errors(errors, _text_errors(value.get("title"), "title", text_limits["title"]))
    _extend_errors(errors, _text_errors(value.get("category"), "category", 32))
    category = value.get("category")
    if category not in categories:
        _add_error(errors, "card: category is not canonical")

    _extend_errors(
        errors,
        _text_list_errors(
            value.get("tags"), "tags", list_limits["tags"], text_limits["tag"]
        ),
    )
    _extend_errors(
        errors,
        _text_list_errors(
            value.get("applies_when"),
            "applies_when",
            list_limits["applies_when"],
            text_limits["condition"],
        ),
    )
    _extend_errors(
        errors,
        _text_list_errors(
            value.get("not_applicable_when"),
            "not_applicable_when",
            list_limits["not_applicable_when"],
            text_limits["condition"],
        ),
    )
    _extend_errors(
        errors,
        _text_list_errors(
            value.get("failure_signature"),
            "failure_signature",
            list_limits["failure_signature"],
            text_limits["failure_signature"],
        ),
    )
    _extend_errors(
        errors,
        _text_errors(value.get("root_cause"), "root_cause", text_limits["root_cause"]),
    )
    _extend_errors(errors, _text_errors(value.get("confidence"), "confidence", 16))
    if value.get("confidence") not in confidence:
        _add_error(errors, "card: confidence must be LOW, MEDIUM, or HIGH")
    for field in ("detection", "prevention", "recovery"):
        _extend_errors(
            errors,
            _text_list_errors(
                value.get(field), field, list_limits[field], text_limits["action"]
            ),
        )

    _extend_errors(
        errors,
        _text_errors(
            value.get("raw_evidence_summary"),
            "raw_evidence_summary",
            text_limits["raw_evidence_summary"],
            allow_empty=True,
        ),
    )
    excerpt = value.get("error_excerpt")
    _extend_errors(
        errors,
        _text_list_errors(
            excerpt,
            "error_excerpt",
            list_limits["error_excerpt_lines"],
            text_limits["error_excerpt_line"],
            allow_empty=True,
        ),
    )
    if isinstance(excerpt, list) and all(isinstance(item, str) for item in excerpt):
        line_count = sum(item.count("\n") + 1 for item in excerpt)
        if line_count > list_limits["error_excerpt_lines"]:
            _add_error(
                errors,
                f"card: error_excerpt exceeds {list_limits['error_excerpt_lines']} lines",
            )

    _extend_errors(errors, _text_errors(value.get("enforcement"), "enforcement", 8))
    if value.get("enforcement") not in enforcement:
        _add_error(errors, "card: enforcement must be BLOCK or WARN")
    for field in ("deterministic", "reproducible", "uncontested"):
        if type(value.get(field)) is not bool:
            _add_error(errors, f"card: {field} must be boolean")

    _extend_errors(
        errors,
        _text_errors(
            value.get("source_fingerprint"),
            "source_fingerprint",
            text_limits["source_fingerprint"],
        ),
    )
    source_fingerprint = value.get("source_fingerprint")
    if isinstance(source_fingerprint, str) and not SOURCE_FINGERPRINT_PATTERN.fullmatch(
        source_fingerprint
    ):
        _add_error(errors, "card: source_fingerprint must be a sha256 fingerprint")
    for field in ("created_sha", "revised_sha"):
        _extend_errors(errors, _text_errors(value.get(field), field, 40))
        sha = value.get(field)
        if isinstance(sha, str) and not GIT_SHA_PATTERN.fullmatch(sha):
            _add_error(
                errors, f"card: {field} must be a 40-character lowercase Git SHA"
            )

    _extend_errors(errors, _text_errors(value.get("status"), "status", 16))
    if value.get("status") not in statuses:
        _add_error(errors, "card: status is not canonical")

    if value.get("enforcement") == "BLOCK":
        if value.get("status") != "ACTIVE":
            _add_error(errors, "card: BLOCK requires status ACTIVE")
        for field in ("deterministic", "reproducible", "uncontested"):
            if value.get(field) is not True:
                _add_error(errors, f"card: BLOCK requires {field} true")

    root = _root_for_card(path)
    if root is not None:
        try:
            relative = path.resolve().relative_to(root.resolve())
        except (OSError, ValueError):
            _add_error(errors, "card: file location is an unsafe path")
        else:
            parts = relative.parts
            if len(parts) != 3 or parts[0] != "cards":
                _add_error(
                    errors, "card: file must be cards/<category>/<lesson_id>.yaml"
                )
            else:
                if isinstance(category, str) and parts[1] != category:
                    _add_error(errors, "card: category does not match file path")
                if isinstance(lesson_id, str) and parts[2] != f"{lesson_id}.yaml":
                    _add_error(errors, "card: lesson_id does not match file name")
    return errors


def validate_card(path: Path) -> list[str]:
    path = Path(path)
    root = _root_for_card(path)
    if root is None:
        return ["card: cannot locate SCHEMA.yaml"]
    schema, errors = _load_schema(root)
    if errors or schema is None:
        return errors
    safety_error = _no_follow_error(root, path, "card")
    if safety_error is not None:
        return [safety_error]
    value, read_errors = _read_yaml(path, path.name, root=root)
    if read_errors:
        return read_errors
    if not isinstance(value, dict):
        return ["card: top level must be a mapping"]
    try:
        return _validate_card_data(path, value, schema)
    except (RecursionError, MemoryError, ValueError, TypeError):
        return ["card: invalid YAML structure"]


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


def _validate_repository(root: Path) -> list[str]:
    root = Path(root)
    errors: list[str] = []
    if _is_link_or_reparse(root):
        return ["repository: link or reparse point is forbidden"]
    if not root.is_dir():
        return ["repository: root must be a directory"]

    schema, schema_errors = _load_schema(root)
    _extend_errors(errors, schema_errors)
    if schema is None:
        return errors

    cards_root = root / "cards"
    cards_safety_error = _no_follow_error(root, cards_root, "cards")
    scan_is_safe = cards_safety_error is None
    if cards_safety_error is not None:
        _add_error(errors, cards_safety_error)

    for category in sorted(CATEGORIES):
        category_path = cards_root / category
        safety_error = _no_follow_error(root, category_path, f"cards/{category}")
        if safety_error is not None:
            scan_is_safe = False
            if not _add_error(errors, safety_error):
                return errors
            continue
        if not category_path.is_dir():
            if not _add_error(
                errors, f"repository: missing category directory cards/{category}"
            ):
                return errors

    index, index_errors = _read_yaml(root / "INDEX.yaml", "INDEX.yaml", root=root)
    _extend_errors(errors, index_errors)
    if index_errors:
        return errors
    if not isinstance(index, dict):
        _add_error(errors, "INDEX.yaml: top level must be a mapping")
        return errors
    _extend_errors(errors, _closed_fields(index, schema["index"]["fields"], "INDEX.yaml"))
    _extend_errors(errors, _sensitive_key_errors(index, "INDEX.yaml"))
    if type(index.get("schema_version")) is not int or index.get("schema_version") != 1:
        _add_error(errors, "INDEX.yaml: schema_version must be 1")
    entries = index.get("entries")
    if not isinstance(entries, list):
        _add_error(errors, "INDEX.yaml: entries must be a list")
        return errors
    if len(entries) > MAX_INDEX_ENTRIES:
        _add_error(errors, f"INDEX.yaml: entries exceeds {MAX_INDEX_ENTRIES} items")

    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    declared_paths: set[str] = set()

    for number, entry in enumerate(entries, start=1):
        if _errors_full(errors):
            break
        location = f"INDEX.yaml entry {number}"
        if not isinstance(entry, dict):
            _add_error(errors, f"{location}: must be a mapping")
            continue
        _extend_errors(
            errors, _closed_fields(entry, schema["index"]["entry_fields"], location)
        )
        _extend_errors(errors, _sensitive_key_errors(entry, location))
        lesson_id = entry.get("lesson_id")
        index_path = entry.get("path")
        if isinstance(lesson_id, str):
            if lesson_id in seen_ids:
                _add_error(errors, f"{location}: duplicate lesson_id")
            seen_ids.add(lesson_id)
        else:
            _add_error(errors, f"{location}: lesson_id must be text")
        path_errors = _index_path_errors(index_path)
        _extend_errors(
            errors,
            [f"{location}: {item.split(': ', 1)[-1]}" for item in path_errors],
        )
        if not isinstance(index_path, str) or path_errors:
            continue
        if index_path in seen_paths:
            _add_error(errors, f"{location}: duplicate path")
        seen_paths.add(index_path)
        declared_paths.add(index_path)

        card_path = root.joinpath(*index_path.split("/"))
        safety_error = _no_follow_error(root, card_path, location)
        if safety_error is not None:
            _add_error(errors, safety_error)
            continue
        if not card_path.is_file():
            _add_error(errors, f"{location}: card file is missing")
            continue
        card_label = _bounded_label(index_path)
        card_errors = validate_card(card_path)
        _extend_errors(
            errors, [f"{card_label}: {item}" for item in card_errors]
        )
        if card_errors:
            continue
        card, card_read_errors = _read_yaml(card_path, index_path, root=root)
        if card_read_errors or not isinstance(card, dict):
            continue
        for field in ("lesson_id", "category", "title", "tags", "enforcement", "status"):
            if entry.get(field) != card.get(field):
                if not _add_error(errors, f"{location}: {field} does not match card"):
                    break

    if scan_is_safe and cards_root.is_dir() and not _errors_full(errors):
        scanned = 0
        pending_directories = [cards_root]
        while pending_directories and not _errors_full(errors):
            directory = pending_directories.pop()
            for path in directory.iterdir():
                scanned += 1
                if scanned > MAX_INDEX_ENTRIES:
                    _add_error(errors, OMITTED_ERRORS)
                    break
                safety_error = _no_follow_error(root, path, "cards")
                if safety_error is not None:
                    if not _add_error(errors, safety_error):
                        break
                    continue
                if path.is_dir():
                    pending_directories.append(path)
                    continue
                if not path.is_file() or path.suffix.lower() not in {".yaml", ".yml"}:
                    continue
                relative_path = path.relative_to(root).as_posix()
                if relative_path not in declared_paths:
                    if not _add_error(
                        errors,
                        f"repository: undeclared YAML card '{_bounded_label(relative_path)}'",
                    ):
                        break
    return errors


def validate_repository(root: Path) -> list[str]:
    try:
        return _validate_repository(Path(root))
    except (OSError, RecursionError, MemoryError, ValueError, TypeError):
        return ["repository: invalid or unsafe structure"]


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) > 1:
        print("ERROR: expected at most one repository path")
        return 1
    root = Path(arguments[0]) if arguments else Path(".")
    errors = validate_repository(root)
    if errors:
        lines: list[str] = []
        used_bytes = 0
        omission_line = f"ERROR: {OMITTED_ERRORS}"
        omission_bytes = len((omission_line + "\n").encode("utf-8"))
        for error in errors:
            line = f"ERROR: {_bounded_message(error, MAX_ERROR_MESSAGE_BYTES)}"
            line_bytes = len((line + "\n").encode("utf-8"))
            if used_bytes + line_bytes > MAX_OUTPUT_BYTES:
                while lines and used_bytes + omission_bytes > MAX_OUTPUT_BYTES:
                    removed = lines.pop()
                    used_bytes -= len((removed + "\n").encode("utf-8"))
                if not lines or lines[-1] != omission_line:
                    lines.append(omission_line)
                break
            lines.append(line)
            used_bytes += line_bytes
        sys.stdout.write("\n".join(lines) + "\n")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
