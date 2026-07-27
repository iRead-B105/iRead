from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from update_submodule_pointers import (
    Submodule,
    current_gitlink,
    load_submodules,
    update_submodule,
)


class SubmodulePointerUpdateTest(unittest.TestCase):
    def test_load_submodules_uses_configured_branch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".gitmodules").write_text(
                '[submodule "services/frontend"]\n'
                "\tpath = services/frontend\n"
                "\turl = https://example.com/frontend.git\n"
                "\tbranch = release\n",
                encoding="utf-8",
            )

            self.assertEqual(
                [
                    Submodule(
                        name="services/frontend",
                        path=Path("services/frontend"),
                        branch="release",
                    )
                ],
                load_submodules(root),
            )

    def test_current_gitlink_rejects_regular_directory(self) -> None:
        result = type(
            "Result",
            (),
            {"stdout": "040000 tree abcdef services/frontend\n"},
        )()
        with patch("update_submodule_pointers.git", return_value=result):
            with self.assertRaisesRegex(RuntimeError, "Expected submodule gitlink"):
                current_gitlink(
                    Submodule(
                        name="services/frontend",
                        path=Path("services/frontend"),
                        branch="develop",
                    )
                )

    def test_update_rejects_non_fast_forward_target(self) -> None:
        submodule = Submodule(
            name="services/frontend",
            path=Path("services/frontend"),
            branch="develop",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / submodule.path).mkdir(parents=True)
            responses = [
                type("Result", (), {"returncode": 0, "stdout": ""})(),
                type("Result", (), {"returncode": 0, "stdout": "b" * 40 + "\n"})(),
                type("Result", (), {"returncode": 0, "stdout": ""})(),
                type(
                    "Result",
                    (),
                    {
                        "returncode": 1,
                        "stdout": "",
                        "stderr": "",
                    },
                )(),
            ]
            with (
                patch("update_submodule_pointers.current_gitlink", return_value="a" * 40),
                patch("update_submodule_pointers.git", side_effect=responses),
            ):
                with self.assertRaisesRegex(RuntimeError, "non-fast-forward"):
                    update_submodule(submodule, root)

    def test_update_checks_out_fast_forward_target(self) -> None:
        submodule = Submodule(
            name="services/frontend",
            path=Path("services/frontend"),
            branch="develop",
        )
        previous = "a" * 40
        target = "b" * 40
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / submodule.path).mkdir(parents=True)
            responses = [
                type("Result", (), {"returncode": 0, "stdout": ""})(),
                type("Result", (), {"returncode": 0, "stdout": target + "\n"})(),
                type("Result", (), {"returncode": 0, "stdout": ""})(),
                type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
                type("Result", (), {"returncode": 0, "stdout": ""})(),
            ]
            with (
                patch(
                    "update_submodule_pointers.current_gitlink",
                    return_value=previous,
                ),
                patch(
                    "update_submodule_pointers.git",
                    side_effect=responses,
                ) as git_mock,
            ):
                self.assertEqual(
                    (previous, target),
                    update_submodule(submodule, root),
                )

            self.assertEqual("checkout", git_mock.call_args_list[-1].args[2])
            self.assertEqual(target, git_mock.call_args_list[-1].args[4])


if __name__ == "__main__":
    unittest.main()
