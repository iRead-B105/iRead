from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".gitignore",
    ".gitattributes",
    ".github/pull_request_template.md",
    ".github/workflows/validate-harness.yml",
    "README.md",
    "AGENTS.md",
    "PLANS.md",
    "docs/README.md",
    "docs/context/project-context.md",
    "docs/context/glossary.md",
    "docs/product/vision-and-scope.md",
    "docs/product/requirements.md",
    "docs/architecture/system-context.md",
    "docs/architecture/repository-strategy.md",
    "docs/decisions/README.md",
    "docs/planning/backlog.md",
    "docs/workflows/ai-development.md",
    "docs/workflows/git-flow.md",
)

MODEL_SPECIFIC_INSTRUCTION_FILES = (
    "CLAUDE.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
)

LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_PATTERN = re.compile(r"\[(?:TBD|ASSUMPTION|BLOCKED)\]")


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)


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


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    model_specific = [
        name for name in MODEL_SPECIFIC_INSTRUCTION_FILES if (ROOT / name).is_file()
    ]
    files = markdown_files()
    links = broken_links(files)
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

    if missing or links or model_specific:
        print("Harness validation failed.")
        return 1

    print(
        f"Harness validation passed: {len(files)} Markdown files, "
        f"{placeholders} explicit open markers."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
