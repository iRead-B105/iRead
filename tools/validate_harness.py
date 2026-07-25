from __future__ import annotations

import re
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
    ".github/workflows/validate-contracts.yml",
    "README.md",
    "AGENTS.md",
    "PLANS.md",
    "docs/index.md",
    "docs/log.md",
    "docs/context/project-context.md",
    "docs/context/glossary.md",
    "docs/product/vision-and-scope.md",
    "docs/product/requirements.md",
    "docs/product/features/index.md",
    "docs/product/features/story-branch.md",
    "docs/product/features/student-management.md",
    "docs/product/features/report.md",
    "docs/product/features/catalog/index.md",
    "docs/architecture/system-context.md",
    "docs/architecture/repository-strategy.md",
    "docs/architecture/data-model.md",
    "docs/decisions/index.md",
    "docs/decisions/ADR-0006-mysql-primary-database.md",
    "docs/decisions/ADR-0007-okf-and-specification-sources.md",
    "docs/planning/backlog.md",
    "docs/workflows/ai-development.md",
    "docs/workflows/specification-management.md",
    "docs/workflows/documentation-style.md",
    "docs/workflows/git-flow.md",
    "docs/workflows/submodules.md",
    "plans/index.md",
    "contracts/index.md",
    "contracts/catalog.md",
    "contracts/review-queue.md",
    "contracts/traceability.json",
    "contracts/openapi/index.md",
    "contracts/openapi/app-api.yaml",
    "contracts/openapi/admin-api.yaml",
    "contracts/openapi/auth-api.yaml",
    "contracts/database/index.md",
    "contracts/database/schema.sql",
    "contracts/notion/index.md",
    "contracts/notion/spec-snapshot.json",
    "tools/export_notion_specs.py",
    "tools/generate_contracts.py",
    "tools/reconcile_notion_decisions.py",
    "tools/validate_contracts.py",
)

MODEL_SPECIFIC_INSTRUCTION_FILES = (
    "CLAUDE.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
)

LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_PATTERN = re.compile(r"\[(?:TBD|ASSUMPTION|BLOCKED)\]")
FRONTMATTER_DELIMITER = re.compile(r"^---\s*$", re.MULTILINE)
ISO_8601_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$"
)
DATE_HEADING_PATTERN = re.compile(r"^## \d{4}-\d{2}-\d{2}\s*$", re.MULTILINE)
OKF_REQUIRED_FIELDS = ("type", "title", "description", "tags", "timestamp")
OKF_ROOT_CONCEPTS = (
    ROOT / "AGENTS.md",
    ROOT / "PLANS.md",
)
OKF_DIRECTORIES = (
    ROOT / "docs",
    ROOT / "plans",
    ROOT / "contracts",
)
OKF_RESERVED_NAMES = ("index.md", "log.md")
SUBMODULE_DIRS = (
    ROOT / "services/backend",
    ROOT / "services/frontend",
    ROOT / "services/ai",
    ROOT / "services/app",
)


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
        and not any(directory in path.parents for directory in SUBMODULE_DIRS)
    )


def broken_links(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for source in files:
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (source.parent / unquote(target)).resolve()
            if not resolved.exists():
                errors.append(
                    f"{source.relative_to(ROOT)} -> {raw_target} (target not found)"
                )
    return errors


def okf_concept_files() -> list[Path]:
    files = [path for path in OKF_ROOT_CONCEPTS if path.is_file()]
    for directory in OKF_DIRECTORIES:
        if not directory.is_dir():
            continue
        files.extend(
            path
            for path in directory.rglob("*.md")
            if path.name not in OKF_RESERVED_NAMES
        )
    return sorted(set(files))


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


def okf_frontmatter_errors(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        parsed = parse_frontmatter(path)
        relative = path.relative_to(ROOT)
        if parsed is None:
            errors.append(f"{relative}: missing or malformed YAML frontmatter")
            continue

        metadata, body = parsed
        for field in OKF_REQUIRED_FIELDS:
            if not metadata.get(field):
                errors.append(f"{relative}: missing OKF field '{field}'")

        timestamp = metadata.get("timestamp", "")
        if timestamp and not ISO_8601_PATTERN.fullmatch(timestamp):
            errors.append(f"{relative}: timestamp is not ISO 8601 with timezone")

        tags = metadata.get("tags", "")
        if tags and not (tags.startswith("[") and tags.endswith("]")):
            errors.append(f"{relative}: tags must use an inline YAML list")

        if not re.search(r"^#\s+\S", body, re.MULTILINE):
            errors.append(f"{relative}: markdown body must contain a level-1 heading")
    return errors


def okf_reserved_file_errors() -> list[str]:
    errors: list[str] = []
    reserved = sorted(
        path
        for directory in OKF_DIRECTORIES
        if directory.is_dir()
        for path in directory.rglob("*.md")
        if path.name in OKF_RESERVED_NAMES
    )
    for path in reserved:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)

        if path.name == "index.md":
            body = text
            if text.startswith("---"):
                parsed = parse_frontmatter(path)
                if parsed is None:
                    errors.append(f"{relative}: malformed index frontmatter")
                    continue
                metadata, body = parsed
                if path != ROOT / "docs/index.md":
                    errors.append(
                        f"{relative}: frontmatter is only allowed on the bundle-root index"
                    )
                if metadata.get("okf_version") != "0.1":
                    errors.append(f"{relative}: bundle root must declare okf_version 0.1")
            if not re.search(r"^#\s+\S", body, re.MULTILINE):
                errors.append(f"{relative}: index must contain a level-1 heading")

        if path.name == "log.md":
            if text.startswith("---"):
                errors.append(f"{relative}: log files must not contain frontmatter")
            if not DATE_HEADING_PATTERN.search(text):
                errors.append(f"{relative}: log must contain a YYYY-MM-DD heading")
    return errors


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    model_specific = [
        name for name in MODEL_SPECIFIC_INSTRUCTION_FILES if (ROOT / name).is_file()
    ]
    files = markdown_files()
    links = broken_links(files)
    okf_files = okf_concept_files()
    okf_frontmatter = okf_frontmatter_errors(okf_files)
    okf_reserved = okf_reserved_file_errors()
    placeholders = sum(
        len(PLACEHOLDER_PATTERN.findall(path.read_text(encoding="utf-8")))
        for path in files
    )

    if missing:
        print("Missing required files:")
        for name in missing:
            print(f"  - {name}")

    if links:
        print("Broken internal Markdown links:")
        for link in links:
            print(f"  - {link}")

    if model_specific:
        print("Model-specific instruction files must be consolidated into AGENTS.md:")
        for name in model_specific:
            print(f"  - {name}")

    if okf_frontmatter:
        print("Invalid OKF concept documents:")
        for error in okf_frontmatter:
            print(f"  - {error}")

    if okf_reserved:
        print("Invalid OKF reserved files:")
        for error in okf_reserved:
            print(f"  - {error}")

    if missing or links or model_specific or okf_frontmatter or okf_reserved:
        print("Harness validation failed.")
        return 1

    print(
        f"Harness validation passed: {len(files)} Markdown files, "
        f"{len(okf_files)} OKF concepts, "
        f"{placeholders} explicit open markers."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
