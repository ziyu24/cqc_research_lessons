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
                "| `demo` | `" + "a" * 40 + "` | 已登记 | 1 |\n", encoding="utf-8"
            )
            self.assertTrue(any("缺少 demo.lessons.md" in item for item in validate_repository(root)))

    def test_zero_entry_needs_no_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "INDEX.md").write_text(
                "| `demo` | `" + "a" * 40 + "` | 占位仓库，无可审计证据 | 0 |\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_repository(root), [])

    def test_internal_run_number_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "INDEX.md").write_text(
                "| `demo` | `" + "a" * 40 + "` | 已登记 | 1 |\n", encoding="utf-8"
            )
            (root / "demo.lessons.md").write_text(
                "## 项目研究什么\n\nx\n\n## 实际采用过的方法\n\nx\n\n"
                "## 教训一：科学标题\n\n"
                "- 失败命题：r009 已失败。\n- 失败原因：x\n- 后续做法：x\n- 边界：x\n"
                "- 证据：`ziyu24/demo@" + "a" * 40 + "` 的 `README.md`。\n",
                encoding="utf-8",
            )
            self.assertTrue(any("内部任务号" in item for item in validate_repository(root)))

    def test_each_lesson_needs_source_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "INDEX.md").write_text(
                "| `demo` | `" + "a" * 40 + "` | 已登记 | 1 |\n", encoding="utf-8"
            )
            (root / "demo.lessons.md").write_text(
                "## 项目研究什么\n\nx\n\n## 实际采用过的方法\n\nx\n\n"
                "## 教训一：科学标题\n\n"
                "- 失败命题：x\n- 失败原因：x\n- 后续做法：x\n- 边界：x\n"
                "- 证据：只有相对路径 `README.md`。\n",
                encoding="utf-8",
            )
            self.assertTrue(any("缺少 40 位来源提交" in item for item in validate_repository(root)))


if __name__ == "__main__":
    unittest.main()
