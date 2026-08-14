from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from validate_harness import (
    adr_index_errors,
    broken_links,
    record_document_errors,
    repository_markdown_files,
)


class HarnessValidationTest(unittest.TestCase):
    def test_repository_files_exclude_ignored_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)

            (root / ".gitignore").write_text(".cache/\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs/tracked.md").write_text("# Tracked\n", encoding="utf-8")
            (root / "new.md").write_text("# New\n", encoding="utf-8")
            (root / ".cache").mkdir()
            (root / ".cache/README.md").write_text("# Ignored\n", encoding="utf-8")
            subprocess.run(
                ["git", "add", ".gitignore", "docs/tracked.md"],
                cwd=root,
                check=True,
            )

            relative = {
                path.relative_to(root).as_posix()
                for path in repository_markdown_files(root)
            }

            self.assertIn("docs/tracked.md", relative)
            self.assertIn("new.md", relative)
            self.assertNotIn(".cache/README.md", relative)

    def test_links_into_unchecked_out_submodules_are_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "contracts/database/erd.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                "[migration](../../services/backend/src/main/resources/db/migration/)\n",
                encoding="utf-8",
            )
            (root / ".gitmodules").write_text(
                '[submodule "services/backend"]\n'
                "\tpath = services/backend\n"
                "\turl = https://example.com/backend.git\n",
                encoding="utf-8",
            )

            self.assertEqual([], broken_links([source], root))

    def test_frontmatter_is_required_only_for_record_documents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            general = root / "docs/context/general.md"
            adr = root / "docs/decisions/ADR-0001-example.md"
            minimal_adr = root / "docs/decisions/ADR-0002-minimal.md"
            general.parent.mkdir(parents=True)
            adr.parent.mkdir(parents=True)
            general.write_text("# General\n", encoding="utf-8")
            adr.write_text("# ADR\n", encoding="utf-8")
            minimal_adr.write_text(
                "---\ntype: Architecture Decision\n---\n# Minimal ADR\n",
                encoding="utf-8",
            )

            errors = record_document_errors([general, adr, minimal_adr], root)

            self.assertEqual(1, len(errors))
            self.assertIn("ADR-0001-example.md", errors[0])

    def test_every_adr_must_be_linked_from_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            decisions = root / "docs/decisions"
            decisions.mkdir(parents=True)
            index = decisions / "index.md"
            first = decisions / "ADR-0001-first.md"
            second = decisions / "ADR-0002-second.md"
            index.write_text("[ADR-0001](ADR-0001-first.md)\n", encoding="utf-8")
            first.write_text("# First\n", encoding="utf-8")
            second.write_text("# Second\n", encoding="utf-8")

            errors = adr_index_errors([index, first, second], root)

            self.assertEqual(1, len(errors))
            self.assertIn("ADR-0002-second.md", errors[0])


if __name__ == "__main__":
    unittest.main()
