from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".gitignore",
    ".gitattributes",
    ".gitmodules",
    ".github/pull_request_template.md",
    ".github/workflows/validate-harness.yml",
    "README.md",
    "AGENTS.md",
    "PLANS.md",
    "docs/index.md",
    "docs/context/project-context.md",
    "docs/decisions/index.md",
    "docs/workflows/documentation-style.md",
    "docs/workflows/specification-management.md",
    "docs/workflows/git-flow.md",
    "contracts/catalog.md",
    "tools/validate_harness.py",
    "tools/tests/test_validate_harness.py",
)

LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SUBMODULE_PATH_PATTERN = re.compile(r"^\s*path\s*=\s*(.+?)\s*$", re.MULTILINE)
ISO_8601_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$"
)
REQUIRED_RECORD_FIELDS = ("type",)


def repository_markdown_files(root: Path = ROOT) -> list[Path]:
    """Return tracked and new Markdown files, excluding ignored files and submodules."""
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            "*.md",
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or "git ls-files failed"
        raise RuntimeError(detail)

    return sorted(
        root / line
        for line in result.stdout.splitlines()
        if line and (root / line).is_file()
    )


def submodule_directories(root: Path = ROOT) -> list[Path]:
    gitmodules = root / ".gitmodules"
    if not gitmodules.is_file():
        return []

    text = gitmodules.read_text(encoding="utf-8")
    return [
        (root / match).resolve()
        for match in SUBMODULE_PATH_PATTERN.findall(text)
    ]


def broken_links(files: list[Path], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    submodules = submodule_directories(root)
    for source in files:
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (source.parent / unquote(target)).resolve()
            inside_submodule = any(
                resolved == directory or directory in resolved.parents
                for directory in submodules
            )
            if not resolved.exists() and not inside_submodule:
                errors.append(
                    f"{source.relative_to(root)} -> {raw_target} (target not found)"
                )
    return errors


def is_record_document(path: Path, root: Path = ROOT) -> bool:
    relative = path.relative_to(root).as_posix()
    name = path.name

    if relative.startswith("docs/decisions/ADR-") and name != "ADR-template.md":
        return True
    if relative.startswith("plans/") and name != "index.md":
        return True
    if relative.startswith("docs/product/features/") and name != "index.md":
        return True
    return False


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str] | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    try:
        closing = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration:
        return None

    metadata: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata, "\n".join(lines[closing + 1 :])


def record_document_errors(
    files: list[Path], root: Path = ROOT
) -> list[str]:
    errors: list[str] = []
    for path in files:
        if not is_record_document(path, root):
            continue

        relative = path.relative_to(root)
        parsed = parse_frontmatter(path)
        if parsed is None:
            errors.append(f"{relative}: missing or malformed record frontmatter")
            continue

        metadata, body = parsed
        for field in REQUIRED_RECORD_FIELDS:
            if not metadata.get(field):
                errors.append(f"{relative}: missing record field '{field}'")

        timestamp = metadata.get("timestamp", "")
        if timestamp and not ISO_8601_PATTERN.fullmatch(timestamp):
            errors.append(f"{relative}: timestamp is not ISO 8601 with timezone")

        tags = metadata.get("tags", "")
        if tags and not (tags.startswith("[") and tags.endswith("]")):
            errors.append(f"{relative}: tags must use an inline YAML list")

        if not re.search(r"^#\s+\S", body, re.MULTILINE):
            errors.append(f"{relative}: markdown body must contain a level-1 heading")
    return errors


def adr_index_errors(files: list[Path], root: Path = ROOT) -> list[str]:
    index_path = root / "docs/decisions/index.md"
    if not index_path.is_file():
        return []

    index_text = index_path.read_text(encoding="utf-8")
    errors: list[str] = []
    for path in files:
        if (
            path.parent == root / "docs/decisions"
            and path.name.startswith("ADR-")
            and path.name != "ADR-template.md"
            and f"({path.name})" not in index_text
        ):
            errors.append(f"{path.relative_to(root)}: not linked from decisions index")
    return errors


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]

    try:
        files = repository_markdown_files()
    except RuntimeError as error:
        print(f"Unable to list repository Markdown files: {error}")
        return 1

    links = broken_links(files)
    record_errors = record_document_errors(files)
    adr_errors = adr_index_errors(files)

    if missing:
        print("Missing required entry files:")
        for name in missing:
            print(f"  - {name}")

    if links:
        print("Broken internal Markdown links:")
        for link in links:
            print(f"  - {link}")

    if record_errors:
        print("Invalid record documents:")
        for error in record_errors:
            print(f"  - {error}")

    if adr_errors:
        print("Unindexed ADR documents:")
        for error in adr_errors:
            print(f"  - {error}")

    if missing or links or record_errors or adr_errors:
        print("Harness validation failed.")
        return 1

    records = sum(is_record_document(path) for path in files)
    print(
        f"Harness validation passed: {len(files)} repository Markdown files, "
        f"{records} record documents."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
