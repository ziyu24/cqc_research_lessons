from __future__ import annotations

from pathlib import Path
import re
import sys


SHA_RE = re.compile(r"`ziyu24/[^`]+@[0-9a-f]{40}`")
ROW_RE = re.compile(r"^\| `([^`]+)` \| `([^`]*)` \| ([^|]+) \| ([0-9]+) \|$")
REQUIRED_FIELDS = ("- 类型：", "- 为何失败：", "- 避坑：", "- 边界：", "- 证据：")


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []
    index = root / "INDEX.md"
    if not index.is_file():
        return ["缺少 INDEX.md"]

    rows: dict[str, tuple[str, int]] = {}
    for line in index.read_text(encoding="utf-8").splitlines():
        match = ROW_RE.fullmatch(line)
        if not match:
            continue
        name, _commit, status, count_text = match.groups()
        if name in rows:
            errors.append(f"INDEX.md 仓库重复: {name}")
        rows[name] = (status.strip(), int(count_text))

    if not rows:
        errors.append("INDEX.md 没有仓库行")

    lesson_dirs = {
        path.parent.name: path
        for path in root.glob("*/lessons.md")
        if path.parent.parent == root
    }
    for name, (status, count) in rows.items():
        path = lesson_dirs.get(name)
        if count == 0:
            if path is not None:
                errors.append(f"{name}: 索引为 0 但存在 lessons.md")
            continue
        if status != "已登记":
            errors.append(f"{name}: 非零条目必须标为已登记")
        if path is None:
            errors.append(f"{name}: 缺少 lessons.md")
            continue
        text = path.read_text(encoding="utf-8")
        headings = re.findall(r"(?m)^## [A-Z0-9-]+ ", text)
        if len(headings) != count:
            errors.append(f"{name}: 索引 {count} 条，实际 {len(headings)} 条")
        for section in re.split(r"(?m)(?=^## [A-Z0-9-]+ )", text)[1:]:
            for field in REQUIRED_FIELDS:
                if field not in section:
                    errors.append(f"{name}: 条目缺少 {field}")
            if not SHA_RE.search(section):
                errors.append(f"{name}: 条目缺少 40 位来源提交")

    for name in sorted(set(lesson_dirs) - set(rows)):
        errors.append(f"{name}: 未登记到 INDEX.md")
    return errors


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    root = Path(arguments[0] if arguments else ".").resolve()
    errors = validate_repository(root)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
