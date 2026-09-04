from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from tools.validate import validate_repository


ROOT = Path(__file__).resolve().parents[1]


class ValidateTests(unittest.TestCase):
    def test_repository_is_valid(self) -> None:
        self.assertEqual(validate_repository(ROOT), [])

    def test_missing_lesson_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "INDEX.md").write_text(
                "| 仓库 | 审计提交 | 状态 | 条目 |\n"
                "|---|---|---|---:|\n"
                "| `demo` | `" + "a" * 40 + "` | 已登记 | 1 |\n",
                encoding="utf-8",
            )
            self.assertTrue(any("缺少 lessons.md" in item for item in validate_repository(root)))

    def test_zero_entry_needs_no_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "INDEX.md").write_text(
                "| 仓库 | 审计提交 | 状态 | 条目 |\n"
                "|---|---|---|---:|\n"
                "| `demo` | `" + "a" * 40 + "` | 未发现已验证失败 | 0 |\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_repository(root), [])

    def test_each_entry_needs_its_own_source_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "INDEX.md").write_text(
                "| `demo` | `" + "a" * 40 + "` | 已登记 | 2 |\n",
                encoding="utf-8",
            )
            project = root / "demo"
            project.mkdir()
            fields = "- 类型：范围限制。\n- 为何失败：x\n- 避坑：x\n- 边界：x\n"
            (project / "lessons.md").write_text(
                "## DEMO-01 one\n\n"
                + fields
                + "- 证据：`ziyu24/demo@"
                + "a" * 40
                + "` 的 `README.md`。\n\n"
                + "## DEMO-02 two\n\n"
                + fields
                + "- 证据：只有相对路径 `README.md`。\n",
                encoding="utf-8",
            )
            self.assertTrue(
                any("条目缺少 40 位来源提交" in item for item in validate_repository(root))
            )


if __name__ == "__main__":
    unittest.main()
