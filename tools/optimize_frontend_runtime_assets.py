"""Create display-sized frontend assets while preserving approved masters."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_AVATAR = (
    ROOT
    / "services"
    / "frontend-app"
    / "src"
    / "assets"
    / "header"
    / "learner-default-avatar.png"
)
MASTER_AVATAR = (
    ROOT
    / "design-resources"
    / "masters"
    / "header"
    / "learner-default-avatar-1254.png"
)
RUNTIME_LESSON_BOARD = (
    ROOT
    / "services"
    / "frontend-app"
    / "src"
    / "assets"
    / "training"
    / "ui"
    / "lesson-progress-title-board.webp"
)
MASTER_LESSON_BOARD = (
    ROOT
    / "design-resources"
    / "masters"
    / "training"
    / "ui"
    / "lesson-progress-title-board-master.webp"
)
RUNTIME_CURRICULUM_HEADER = (
    ROOT
    / "services"
    / "frontend-app"
    / "src"
    / "assets"
    / "training"
    / "ui"
    / "curriculum-integrated-header.webp"
)
MASTER_CURRICULUM_HEADER = (
    ROOT
    / "design-resources"
    / "masters"
    / "training"
    / "ui"
    / "curriculum-integrated-header-master.webp"
)


def optimize_avatar() -> None:
    MASTER_AVATAR.parent.mkdir(parents=True, exist_ok=True)
    if not MASTER_AVATAR.exists():
        shutil.copy2(RUNTIME_AVATAR, MASTER_AVATAR)

    with Image.open(MASTER_AVATAR) as master:
        runtime = master.convert("RGBA")
        runtime.thumbnail((256, 256), Image.Resampling.LANCZOS)
        runtime.save(RUNTIME_AVATAR, optimize=True)

    print(
        f"{RUNTIME_AVATAR.relative_to(ROOT)} "
        f"({RUNTIME_AVATAR.stat().st_size / 1024:.1f} KiB)"
    )


def optimize_lesson_board() -> None:
    MASTER_LESSON_BOARD.parent.mkdir(parents=True, exist_ok=True)
    if not MASTER_LESSON_BOARD.exists():
        shutil.copy2(RUNTIME_LESSON_BOARD, MASTER_LESSON_BOARD)

    with Image.open(MASTER_LESSON_BOARD) as master:
        runtime = master.convert("RGBA")
        alpha_bounds = runtime.getchannel("A").getbbox()
        if alpha_bounds is None:
            raise ValueError("Lesson progress board has no visible alpha content.")

        padding = 12
        left, top, right, bottom = alpha_bounds
        crop_box = (
            max(0, left - padding),
            max(0, top - padding),
            min(runtime.width, right + padding),
            min(runtime.height, bottom + padding),
        )
        runtime = runtime.crop(crop_box)
        runtime.save(
            RUNTIME_LESSON_BOARD,
            format="WEBP",
            quality=88,
            method=6,
            exact=True,
        )

    print(
        f"{RUNTIME_LESSON_BOARD.relative_to(ROOT)} "
        f"({runtime.width}×{runtime.height}, "
        f"{RUNTIME_LESSON_BOARD.stat().st_size / 1024:.1f} KiB)"
    )


def optimize_curriculum_header() -> None:
    MASTER_CURRICULUM_HEADER.parent.mkdir(parents=True, exist_ok=True)
    if not MASTER_CURRICULUM_HEADER.exists():
        shutil.copy2(RUNTIME_CURRICULUM_HEADER, MASTER_CURRICULUM_HEADER)

    with Image.open(MASTER_CURRICULUM_HEADER) as master:
        runtime = master.convert("RGBA")
        alpha_bounds = runtime.getchannel("A").getbbox()
        if alpha_bounds is None:
            raise ValueError("Curriculum header has no visible alpha content.")

        padding = 10
        left, top, right, bottom = alpha_bounds
        runtime = runtime.crop(
            (
                max(0, left - padding),
                max(0, top - padding),
                min(runtime.width, right + padding),
                min(runtime.height, bottom + padding),
            )
        )
        runtime.thumbnail((1800, 440), Image.Resampling.LANCZOS)
        runtime.save(
            RUNTIME_CURRICULUM_HEADER,
            format="WEBP",
            quality=88,
            method=6,
            exact=True,
        )

    print(
        f"{RUNTIME_CURRICULUM_HEADER.relative_to(ROOT)} "
        f"({runtime.width}x{runtime.height}, "
        f"{RUNTIME_CURRICULUM_HEADER.stat().st_size / 1024:.1f} KiB)"
    )


def main() -> None:
    optimize_avatar()
    optimize_lesson_board()
    optimize_curriculum_header()


if __name__ == "__main__":
    main()
