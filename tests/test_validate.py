from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import shutil
import tempfile
import unittest

import yaml

from tools.validate import main, validate_card, validate_repository


REPOSITORY_ROOT = Path(__file__).parents[1]


def canonical_card(**overrides):
    card = {
        "schema_version": 1,
        "lesson_id": "L000001",
        "title": "Reject misaligned labels",
        "category": "data",
        "tags": ["labels", "alignment"],
        "applies_when": ["Samples and labels are joined by position."],
        "not_applicable_when": ["The dataset has no labels."],
        "failure_signature": ["Validation quality collapses after a reorder."],
        "root_cause": "A positional join silently paired records with the wrong labels.",
        "confidence": "HIGH",
        "detection": ["Compare stable record identifiers before training."],
        "prevention": ["Join samples and labels by a validated stable identifier."],
        "recovery": ["Rebuild the manifest and rerun the affected stage."],
        "raw_evidence_summary": "A bounded aggregate showed identifier disagreement.",
        "error_excerpt": ["identifier mismatch detected"],
        "enforcement": "WARN",
        "deterministic": False,
        "reproducible": True,
        "uncontested": True,
        "source_fingerprint": "sha256:" + "a" * 64,
        "created_sha": "b" * 40,
        "revised_sha": "b" * 40,
        "status": "ACTIVE",
    }
    card.update(overrides)
    return card


def index_entry(card, path="cards/data/L000001.yaml"):
    return {
        "lesson_id": card["lesson_id"],
        "path": path,
        "category": card["category"],
        "title": card["title"],
        "tags": card["tags"],
        "enforcement": card["enforcement"],
        "status": card["status"],
    }


def write_repository(root, cards, entries):
    shutil.copyfile(REPOSITORY_ROOT / "SCHEMA.yaml", root / "SCHEMA.yaml")
    (root / "INDEX.yaml").write_text(
        yaml.safe_dump({"schema_version": 1, "entries": entries}, sort_keys=False),
        encoding="utf-8",
    )
    for relative_path, card in cards.items():
        destination = root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(yaml.safe_dump(card, sort_keys=False), encoding="utf-8")


class LessonRepositoryTests(unittest.TestCase):
    def test_empty_canonical_repository_is_valid(self):
        self.assertEqual(validate_repository(REPOSITORY_ROOT), [])

    def test_rejects_oversized_raw_summary_and_sensitive_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card = canonical_card(raw_evidence_summary="x" * 2049, ssh_user="forbidden")
            write_repository(
                root,
                {"cards/data/L000001.yaml": card},
                [index_entry(card)],
            )

            errors = validate_repository(root)

            self.assertTrue(any("raw_evidence_summary" in item for item in errors))
            self.assertTrue(any("sensitive" in item and "ssh_user" in item for item in errors))
            self.assertFalse(any("x" * 100 in item for item in errors))

    def test_rejects_absolute_and_parent_traversing_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_repository(root, {}, [])
            traversal = root / "cards/data/L000001.yaml"
            traversal.parent.mkdir(parents=True)
            traversal.write_text(
                yaml.safe_dump(canonical_card(recovery=["../../private/log.txt"])),
                encoding="utf-8",
            )
            absolute = root / "cards/data/L000002.yaml"
            absolute.write_text(
                yaml.safe_dump(
                    canonical_card(
                        lesson_id="L000002",
                        raw_evidence_summary="C:\\private\\full.log",
                    )
                ),
                encoding="utf-8",
            )

            self.assertTrue(any("unsafe path" in item for item in validate_card(traversal)))
            self.assertTrue(any("unsafe path" in item for item in validate_card(absolute)))

    def test_rejects_unsafe_paths_embedded_in_free_text_without_echoing_them(self):
        unsafe_values = (
            r"Evidence at C:\private\full.log",
            "Evidence at /private/full.log",
            "path=../private/full.log",
        )
        for unsafe_value in unsafe_values:
            with self.subTest(value=unsafe_value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_repository(root, {}, [])
                path = root / "cards/data/L000001.yaml"
                path.parent.mkdir(parents=True)
                path.write_text(
                    yaml.safe_dump(canonical_card(raw_evidence_summary=unsafe_value)),
                    encoding="utf-8",
                )

                errors = validate_card(path)

                self.assertTrue(any("unsafe path" in item for item in errors), errors)
                self.assertNotIn(unsafe_value, "\n".join(errors))

    def test_block_requires_active_deterministic_reproducible_uncontested_card(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_repository(root, {}, [])
            path = root / "cards/data/L000001.yaml"
            path.parent.mkdir(parents=True)
            path.write_text(
                yaml.safe_dump(
                    canonical_card(
                        enforcement="BLOCK",
                        status="CONTESTED",
                        deterministic=False,
                        reproducible=False,
                        uncontested=False,
                    )
                ),
                encoding="utf-8",
            )

            errors = validate_card(path)

            for field in ("status", "deterministic", "reproducible", "uncontested"):
                self.assertTrue(any(field in item for item in errors), errors)

    def test_rejects_more_than_twenty_error_excerpt_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_repository(root, {}, [])
            path = root / "cards/data/L000001.yaml"
            path.parent.mkdir(parents=True)
            path.write_text(
                yaml.safe_dump(canonical_card(error_excerpt=["line"] * 21)),
                encoding="utf-8",
            )

            self.assertTrue(
                any("error_excerpt" in item and "20" in item for item in validate_card(path))
            )

    def test_index_entries_are_unique_and_match_their_cards(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card = canonical_card()
            mismatched = index_entry(card)
            mismatched["title"] = "Wrong title"
            write_repository(
                root,
                {"cards/data/L000001.yaml": card},
                [mismatched, mismatched],
            )

            errors = validate_repository(root)

            self.assertTrue(any("duplicate lesson_id" in item for item in errors), errors)
            self.assertTrue(any("duplicate path" in item for item in errors), errors)
            self.assertTrue(any("does not match card" in item for item in errors), errors)

    def test_rejects_undeclared_yaml_cards(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card = canonical_card()
            write_repository(root, {"cards/data/L000001.yaml": card}, [])

            errors = validate_repository(root)

            self.assertTrue(any("undeclared YAML card" in item for item in errors), errors)

    def test_rejects_index_absolute_and_parent_traversing_paths(self):
        for unsafe_path in ("C:\\private\\L000001.yaml", "cards/data/../../L000001.yaml"):
            with self.subTest(path=unsafe_path), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card = canonical_card()
                write_repository(root, {}, [index_entry(card, path=unsafe_path)])

                errors = validate_repository(root)

                self.assertTrue(any("unsafe path" in item for item in errors), errors)

    def test_cli_errors_are_bounded_and_return_one(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card = canonical_card(raw_evidence_summary="secret-value-" * 500)
            write_repository(
                root,
                {"cards/data/L000001.yaml": card},
                [index_entry(card)],
            )
            output = StringIO()

            with redirect_stdout(output):
                result = main([str(root)])

            self.assertEqual(result, 1)
            self.assertIn("raw_evidence_summary", output.getvalue())
            self.assertNotIn("secret-value", output.getvalue())
            self.assertLess(len(output.getvalue()), 2000)

    def test_cli_does_not_echo_an_unbounded_card_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            long_name = "L" + "9" * 180 + ".yaml"
            relative_path = f"cards/data/{long_name}"
            card = canonical_card()
            write_repository(root, {relative_path: card}, [index_entry(card, relative_path)])
            output = StringIO()

            with redirect_stdout(output):
                result = main([str(root)])

            self.assertEqual(result, 1)
            self.assertNotIn("9" * 100, output.getvalue())


if __name__ == "__main__":
    unittest.main()
