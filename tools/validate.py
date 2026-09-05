from __future__ import annotations

from pathlib import Path
import re
import sys


SHA_RE = re.compile(r"`ziyu24/[^`]+@[0-9a-f]{40}`")
ROW_RE = re.compile(r"^\| `([^`]+)` \| `([^`]*)` \| ([^|]+) \| ([0-9]+) \|$")
LESSON_RE = re.compile(r"(?m)^## 教训[一二三四五六七八九十]+：")
REQUIRED_FIELDS = ("- 失败命题：", "- 失败原因：", "- 后续做法：", "- 边界：", "- 证据：")


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

    lesson_root = root / "lesson"
    if not lesson_root.is_dir():
        errors.append("缺少 lesson/ 目录")

    root_lessons = sorted(root.glob("*.lessons.md"))
    for path in root_lessons:
        errors.append(f"{path.name}: 避坑文件必须位于 lesson/")

    nested_lessons = sorted(
        path for path in lesson_root.rglob("*.lessons.md") if path.parent != lesson_root
    ) if lesson_root.is_dir() else []
    for path in nested_lessons:
        errors.append(f"{path.relative_to(root)}: lesson/ 内不得建立项目子目录")

    lesson_files = {
        path.name.removesuffix(".lessons.md"): path
        for path in lesson_root.glob("*.lessons.md")
    }
    for name, (status, count) in rows.items():
        path = lesson_files.get(name)
        if count == 0:
            if path is not None:
                errors.append(f"{name}: 索引为 0 但存在 lessons 文件")
            continue
        if status != "已登记":
            errors.append(f"{name}: 非零条目必须标为已登记")
        if path is None:
            errors.append(f"{name}: 缺少 {name}.lessons.md")
            continue
        text = path.read_text(encoding="utf-8")
        for heading in ("## 项目研究什么", "## 实际采用过的方法"):
            if heading not in text:
                errors.append(f"{name}: 缺少 {heading}")
        headings = list(LESSON_RE.finditer(text))
        if len(headings) != count:
            errors.append(f"{name}: 索引 {count} 条，实际 {len(headings)} 条")
        for index_number, heading in enumerate(headings):
            end = headings[index_number + 1].start() if index_number + 1 < len(headings) else len(text)
            section = text[heading.start():end]
            for field in REQUIRED_FIELDS:
                if field not in section:
                    errors.append(f"{name}: 条目缺少 {field}")
            if not SHA_RE.search(section):
                errors.append(f"{name}: 条目缺少 40 位来源提交")
            if re.search(r"\br\d{3,}\b", section, re.IGNORECASE):
                errors.append(f"{name}: 条目含项目内部任务号")

    for name in sorted(set(lesson_files) - set(rows)):
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
