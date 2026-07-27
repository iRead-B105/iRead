from __future__ import annotations

import configparser
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Submodule:
    name: str
    path: Path
    branch: str


def git(
    *args: str,
    cwd: Path = ROOT,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git failed"
        raise RuntimeError(f"git {' '.join(args)}: {detail}")
    return result


def load_submodules(root: Path = ROOT) -> list[Submodule]:
    config_path = root / ".gitmodules"
    parser = configparser.ConfigParser()
    parser.read(config_path, encoding="utf-8")

    submodules: list[Submodule] = []
    for section in parser.sections():
        if not section.startswith('submodule "') or not section.endswith('"'):
            continue
        name = section[len('submodule "') : -1]
        path = Path(parser.get(section, "path"))
        branch = parser.get(section, "branch", fallback="develop")
        submodules.append(Submodule(name=name, path=path, branch=branch))
    return submodules


def current_gitlink(submodule: Submodule, root: Path = ROOT) -> str:
    result = git("ls-tree", "HEAD", "--", submodule.path.as_posix(), cwd=root)
    fields = result.stdout.strip().split()
    if len(fields) < 3 or fields[0] != "160000" or fields[1] != "commit":
        raise RuntimeError(f"Expected submodule gitlink: {submodule.path}")
    return fields[2]


def update_submodule(submodule: Submodule, root: Path = ROOT) -> tuple[str, str] | None:
    directory = root / submodule.path
    if not directory.is_dir():
        raise RuntimeError(f"Submodule is not initialized: {submodule.path}")

    previous = current_gitlink(submodule, root)
    git(
        "-C",
        str(directory),
        "fetch",
        "--no-tags",
        "origin",
        submodule.branch,
        cwd=root,
    )
    target = git(
        "-C",
        str(directory),
        "rev-parse",
        "FETCH_HEAD",
        cwd=root,
    ).stdout.strip()

    if previous == target:
        return None

    present = git(
        "-C",
        str(directory),
        "cat-file",
        "-e",
        f"{previous}^{{commit}}",
        cwd=root,
        check=False,
    )
    if present.returncode != 0:
        git(
            "-C",
            str(directory),
            "fetch",
            "--no-tags",
            "origin",
            previous,
            cwd=root,
        )

    ancestor = git(
        "-C",
        str(directory),
        "merge-base",
        "--is-ancestor",
        previous,
        target,
        cwd=root,
        check=False,
    )
    if ancestor.returncode == 1:
        raise RuntimeError(
            f"Refusing non-fast-forward update for {submodule.path}: "
            f"{previous} -> {target}"
        )
    if ancestor.returncode != 0:
        detail = ancestor.stderr.strip() or "merge-base failed"
        raise RuntimeError(f"Unable to validate {submodule.path}: {detail}")

    git("-C", str(directory), "checkout", "--detach", target, cwd=root)
    return previous, target


def main() -> int:
    try:
        changes: list[str] = []
        for submodule in load_submodules():
            updated = update_submodule(submodule)
            if updated is None:
                continue
            previous, target = updated
            changes.append(
                f"{submodule.path.as_posix()}: "
                f"{previous[:12]} -> {target[:12]}"
            )
    except (OSError, RuntimeError, configparser.Error) as error:
        print(error, file=sys.stderr)
        return 1

    print("\n".join(changes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
