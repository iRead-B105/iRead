"""Generate the frontend asset inventory, contact sheets, and usage map."""

from __future__ import annotations

import os
import re
from collections import Counter, defaultdict
from collections import deque
from pathlib import Path
from textwrap import shorten

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = ROOT / "services" / "frontend-app"
SOURCE_ROOT = FRONTEND_ROOT / "src"
ASSET_ROOT = SOURCE_ROOT / "assets"
OUTPUT = ROOT / "docs" / "product" / "frontend-asset-inventory.md"
SHEET_ROOT = ROOT / "docs" / "product" / "assets" / "frontend-asset-contact-sheets"

SOURCE_SUFFIXES = {".vue", ".ts", ".css"}
PREVIEW_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
IMPORT_PATTERN = re.compile(
    r"""(?:from\s*|import\s*\(\s*|import\s*|@import\s*|src\s*=\s*)["']([^"']+)["']"""
)
IMPORT_META_GLOB_PATTERN = re.compile(
    r"""import\.meta\.glob(?:<[^>]+>)?\(\s*["']([^"']+)["']"""
)

# These modules expose several independent data fields through one facade. A
# module-level import graph cannot tell which field a Vue screen consumes, so
# traversing beyond them would incorrectly assign every asset to every screen.
SEMANTIC_DATA_BOUNDARIES = {
    "apiLearnerContentRepository.ts",
    "learnerDataRepository.ts",
    "learnerRuntimeMock.ts",
    "mockLearnerContentRepository.ts",
}

SCREEN_BY_SOURCE_NAME = {
    "App.vue": "앱 전체 · 전역 오버레이",
    "LearnerLayout.vue": "로그인 이후 모든 아동 화면 · 공통 레이아웃",
    "LearnerHeader.vue": "로그인 이후 모든 아동 화면 · 상단 헤더",
    "LearnerLoginView.vue": "아동 로그인 · 계정 입력/아동 선택",
    "LearnerHomeView.vue": "메인 섬 · 메뉴 지도",
    "IslandMap.vue": "메인 섬 · 메뉴 섬",
    "StorySelectionView.vue": "이야기 나라 · 책 선택/이어 읽기",
    "StoryReaderView.vue": "이야기 읽기 · 장면/분기/친구 보상",
    "TrainingHomeView.vue": "글자 학습 · 커리큘럼/훈련 선택",
    "TrainingLessonView.vue": "글자 학습 · 문제 풀이 공통 화면",
    "TrainingCompleteView.vue": "글자 학습 · 일반/올정답 완료",
    "TodayTrainingCompleteView.vue": "오늘의 학습 · 전체 완료",
    "SkillChallengeView.vue": "실력 도전 · 코스 선택",
    "SkillChallengeCompleteView.vue": "실력 도전 · 완료",
    "GrowthView.vue": "성장 정원 · 화단/이야기 친구",
    "StoryFriendCollectionModal.vue": "성장 정원 · 이야기 친구 모달",
    "PageBackButton.vue": "아동 상세 화면 · 공통 뒤로가기",
    "SoundButton.vue": "소리가 있는 모든 학습 · 듣기/재생/다시 듣기",
    "TrainingCurriculumPath.vue": "글자 학습 · 커리큘럼 경로",
    "TrainingLessonModal.vue": "글자 학습 · 훈련 목록 모달",
    "TrainingLessonCard.vue": "글자 학습 · 훈련 목록 카드",
    "TrainingIntro.vue": "글자 학습 · 훈련 시작",
    "TrainingComplete.vue": "글자 학습 · 문제 세트 완료",
    "LetterCard.vue": "글자 학습 · 자모 카드",
    "RiveGuideCharacter.vue": "글자 학습 · 안내 토끼",
    "ResourceRequired.vue": "글자 학습 · 누락 리소스 자리",
    "learnerRuntimeMock.ts": "목업 데이터 · 이야기/학습 화면 공급",
    "hangulCards.ts": "글자 학습 · 자모 카드 registry",
    "trainingCategories.ts": "글자 학습 · 카테고리 데이터",
}


def classification(relative_path: Path) -> tuple[str, str]:
    value = relative_path.as_posix()
    if value.startswith("training/choice-cards/"):
        return "색 변경 완료", "공통 카드 variant"
    if value.startswith("icons/"):
        return "유지", "공통 의미 아이콘"
    if value.startswith(("backgrounds/", "map/")):
        return "유지+최적화", "표시 크기·차세대 포맷 검토"
    if value.startswith("battle/"):
        return "다듬기", "캐릭터 캔버스·비율 통일 검토"
    if value.startswith("story/"):
        return "다듬기", "동일 인물·화풍 일관성 검토"
    if value.startswith(("challenge/", "growth/")):
        return "다듬기", "메인 섬 팔레트·배치 검토"
    if value.startswith(("cards/", "characters/")):
        return "유지+검수", "교육적 모양·캐릭터 일관성 검토"
    if value.startswith(("header/", "navigation/")):
        return "유지+최적화", "공통 UI 표시 크기 검토"
    if value.startswith("training/"):
        return "유지+검수", "학습 상태 보드에서 검수"
    if value.startswith("fonts/"):
        return "유지", "전체 아동 화면 글꼴"
    return "검수 필요", "화면 사용처 확인"


def default_screen(relative_path: Path) -> str:
    value = relative_path.as_posix()
    if value.startswith("backgrounds/garden-growth/"):
        return "성장 정원 · 화단 단계"
    if value.startswith("backgrounds/challenge"):
        return "실력 도전 · 전체 배경"
    if value.startswith("backgrounds/curriculum"):
        return "글자 학습 · 커리큘럼 배경"
    if value.startswith("backgrounds/story"):
        return "이야기 나라 · 전체 배경"
    if value.startswith("backgrounds/training"):
        return "글자 학습 · 전체/문제 배경"
    if value.startswith("battle/"):
        return "글자 학습 · 한글 배틀 캐릭터"
    if value.startswith("cards/hangul/"):
        return "글자 학습 · 자모 카드"
    if value.startswith("challenge/"):
        return "실력 도전 · 코스 카드"
    if value.startswith("characters/"):
        return "글자 학습 · 활동/안내 캐릭터"
    if value.startswith("fonts/"):
        return "로그인 이후 모든 아동 화면 · 글꼴"
    if value.startswith("growth/"):
        return "성장 정원 · 화단 이름표/장식"
    if value.startswith("header/"):
        return "로그인 이후 모든 아동 화면 · 상단 헤더"
    if value.startswith("icons/"):
        return "공용 UI · 참조 파일에 따라 표시"
    if value.startswith("map/"):
        return "메인 섬 · 메뉴 지도"
    if value.startswith("navigation/"):
        return "글자 학습/상세 화면 · 이동 버튼"
    if value.startswith("sentence-match/"):
        return "글자 학습 · 그림-문장 연결"
    if value.startswith("story/characters/"):
        return "이야기 읽기 보상/성장 정원 · 이야기 친구"
    if value.startswith("story/ui/"):
        return "이야기 나라 · 책 선택 UI"
    if value.startswith("story/"):
        return "이야기 나라 · 표지/본문/분기"
    if value.startswith("training/choice-cards/"):
        return "글자 학습 · 모든 3지선다 선택 카드"
    if value.startswith("training/ui/"):
        return "글자 학습 · 진행도/커리큘럼/완료 UI"
    if value.startswith("training/"):
        return "글자 학습 · 문제 풀이/완료"
    if relative_path.suffix == ".riv":
        return "글자 학습 · 화면 우측 안내 토끼"
    return "코드 참조 위치 확인 필요"


def dimensions(path: Path) -> str:
    try:
        with Image.open(path) as image:
            return f"{image.width}×{image.height}"
    except Exception:
        return "-"


def read_sources() -> dict[Path, str]:
    return {
        path: path.read_text(encoding="utf-8", errors="ignore")
        for path in SOURCE_ROOT.rglob("*")
        if path.is_file() and path.suffix in SOURCE_SUFFIXES
    }


def resolve_source_import(importer: Path, specifier: str) -> Path | None:
    clean_specifier = specifier.split("?", 1)[0]
    if clean_specifier.startswith("@/"):
        candidate = SOURCE_ROOT / clean_specifier[2:]
    elif clean_specifier.startswith("."):
        candidate = importer.parent / clean_specifier
    else:
        return None

    candidates = [
        candidate,
        candidate.with_suffix(".ts"),
        candidate.with_suffix(".vue"),
        candidate.with_suffix(".css"),
        candidate / "index.ts",
        candidate / "index.vue",
        candidate / "index.css",
    ]
    for value in candidates:
        try:
            resolved = value.resolve()
        except OSError:
            continue
        if resolved.is_file() and SOURCE_ROOT.resolve() in resolved.parents:
            return resolved
    return None


def build_reverse_import_graph(sources: dict[Path, str]) -> dict[Path, set[Path]]:
    reverse_graph: dict[Path, set[Path]] = defaultdict(set)
    for importer, text in sources.items():
        for specifier in IMPORT_PATTERN.findall(text):
            imported = resolve_source_import(importer, specifier)
            if imported is not None:
                reverse_graph[imported].add(importer.resolve())
    # Vite loads main.ts as the application entry rather than through a source
    # import. Treat App.vue as its visible root so global CSS reaches a screen.
    main_entry = (SOURCE_ROOT / "main.ts").resolve()
    app_root = (SOURCE_ROOT / "App.vue").resolve()
    if main_entry.is_file() and app_root.is_file():
        reverse_graph[main_entry].add(app_root)
    return reverse_graph


def glob_usage_files(asset_path: Path, sources: dict[Path, str]) -> list[Path]:
    matches: list[Path] = []
    resolved_asset = asset_path.resolve()
    for source, text in sources.items():
        for pattern in IMPORT_META_GLOB_PATTERN.findall(text):
            if not pattern.startswith("."):
                continue
            try:
                glob_matches = source.parent.glob(pattern)
                if any(path.resolve() == resolved_asset for path in glob_matches):
                    matches.append(source)
            except (OSError, ValueError):
                continue
    return matches


def usage_files(
    asset_path: Path,
    relative_path: Path,
    sources: dict[Path, str],
) -> list[Path]:
    exact_name_pattern = re.compile(
        rf"""(?:^|[/\\'"(]){re.escape(relative_path.name)}(?:\?[^"' )]+)?(?:["')]|$)"""
    )
    matches = [
        path
        for path, text in sources.items()
        if exact_name_pattern.search(text)
    ]
    matches.extend(glob_usage_files(asset_path, sources))
    return sorted(set(matches))


def semantic_vue_files(relative_path: Path) -> set[Path]:
    """Map assets stored in aggregate data objects to their real consumers."""
    value = relative_path.as_posix()
    learner_views = SOURCE_ROOT / "views" / "learner"
    common_components = SOURCE_ROOT / "components" / "common"

    if value.startswith("story/covers/"):
        return {learner_views / "StorySelectionView.vue"}
    if value.startswith("story/characters/"):
        return {
            learner_views / "GrowthView.vue",
            learner_views / "StoryReaderView.vue",
        }
    if value == "story/story-reader-turtle-scene-mock.png":
        return {
            learner_views / "StoryReaderView.vue",
            common_components / "GazeCalibrationModal.vue",
        }
    return set()


def reachable_vue_files(
    relative_path: Path,
    references: list[Path],
    reverse_graph: dict[Path, set[Path]],
) -> list[Path]:
    semantic_files = semantic_vue_files(relative_path)
    queue = deque(
        path.resolve()
        for path in references
        if path.name not in SEMANTIC_DATA_BOUNDARIES
    )
    visited = set(queue)
    vue_files: set[Path] = {path.resolve() for path in semantic_files if path.is_file()}
    while queue:
        current = queue.popleft()
        if current.suffix == ".vue":
            vue_files.add(current)
        if current.name in SEMANTIC_DATA_BOUNDARIES:
            continue
        for importer in reverse_graph.get(current, set()):
            if importer not in visited:
                visited.add(importer)
                queue.append(importer)
    return sorted(vue_files)


def screen_label(source: Path) -> str | None:
    if source.name in SCREEN_BY_SOURCE_NAME:
        return SCREEN_BY_SOURCE_NAME[source.name]
    if "components" in source.parts and "activities" in source.parts:
        return f"글자 학습 · {source.stem.replace('Activity', '')} 활동"
    if "styles" in source.parts and "training" in source.parts:
        return "글자 학습 · 참조 스타일이 적용되는 화면"
    if "styles" in source.parts and "story" in source.parts:
        return "이야기 나라 · 참조 스타일이 적용되는 화면"
    if "styles" in source.parts and "world" in source.parts:
        return "메인 섬/성장 정원 · 참조 스타일이 적용되는 화면"
    return None


def usage_summary(
    relative_path: Path,
    references: list[Path],
    vue_files: list[Path],
) -> str:
    if not references:
        return f"[TBD] 현재 노출 화면 확인 안 됨<br>예상 용도: {default_screen(relative_path)}"

    labels = {
        label
        for source in vue_files
        if (label := screen_label(source)) is not None
    }
    labels.update(
        label
        for source in references
        if source.suffix == ".css" and (label := screen_label(source)) is not None
    )
    if not labels:
        labels.add(default_screen(relative_path))
    return "<br>".join(sorted(labels))


def connection_status(references: list[Path], vue_files: list[Path]) -> str:
    if vue_files:
        return "Vue 연결 확인"
    if references:
        return "코드 참조 확인<br>[TBD] 최종 Vue 경로 미확인"
    return "[TBD] 현재 src 코드 참조 없음"


def reference_summary(references: list[Path]) -> str:
    if not references:
        return "—"
    visible = [
        source.relative_to(FRONTEND_ROOT).as_posix()
        for source in references[:4]
    ]
    if len(references) > 4:
        visible.append(f"외 {len(references) - 4}개")
    return "<br>".join(f"`{value}`" for value in visible)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/malgun.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def create_contact_sheet(group: str, entries: list[tuple[str, Path]]) -> Path | None:
    raster_entries = [
        (preview_id, path)
        for preview_id, path in entries
        if path.suffix.lower() in PREVIEW_SUFFIXES
    ]
    if not raster_entries:
        return None

    columns = 4
    cell_width, cell_height = 240, 180
    rows = (len(raster_entries) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), "#f4f6fa")
    draw = ImageDraw.Draw(sheet)
    id_font = load_font(18)
    name_font = load_font(14)

    for index, (preview_id, path) in enumerate(raster_entries):
        column, row = index % columns, index // columns
        x, y = column * cell_width, row * cell_height
        draw.rounded_rectangle(
            (x + 7, y + 7, x + cell_width - 7, y + cell_height - 7),
            radius=16,
            fill="#ffffff",
            outline="#d9dfeb",
            width=2,
        )
        with Image.open(path) as source:
            image = source.convert("RGBA")
            image.thumbnail((204, 118), Image.Resampling.LANCZOS)
            preview = Image.new("RGBA", image.size, "#eef1f6")
            preview.alpha_composite(image)
            paste_x = x + (cell_width - preview.width) // 2
            paste_y = y + 15 + (118 - preview.height) // 2
            sheet.paste(preview.convert("RGB"), (paste_x, paste_y))
        draw.text((x + 15, y + 137), preview_id, font=id_font, fill="#315d96")
        label = shorten(path.name, width=27, placeholder="…")
        draw.text((x + 58, y + 140), label, font=name_font, fill="#27364d")

    SHEET_ROOT.mkdir(parents=True, exist_ok=True)
    destination = SHEET_ROOT / f"{group}.jpg"
    sheet.save(destination, quality=84, optimize=True, progressive=True)
    return destination


def preview_cell(preview_id: str, path: Path) -> str:
    if path.suffix.lower() in PREVIEW_SUFFIXES:
        return preview_id
    if path.suffix.lower() == ".svg":
        relative = Path(os.path.relpath(path, OUTPUT.parent)).as_posix()
        return f'<img src="{relative}" width="54" alt="{path.stem} 미리보기">'
    return "—"


def asset_sort_key(path: Path) -> str:
    value = path.as_posix()
    for index, color in enumerate(("yellow", "mint", "purple")):
        value = value.replace(f"-{color}", f"-{index}-{color}")
    return value


def main() -> None:
    assets = sorted(
        (path for path in ASSET_ROOT.rglob("*") if path.is_file()),
        key=asset_sort_key,
    )
    sources = read_sources()
    reverse_graph = build_reverse_import_graph(sources)
    total_bytes = sum(path.stat().st_size for path in assets)
    extensions = Counter(path.suffix.lower() or "(none)" for path in assets)
    grouped: dict[str, list[Path]] = defaultdict(list)
    for path in assets:
        grouped[path.relative_to(ASSET_ROOT).parts[0]].append(path)

    lines = [
        "# Frontend 에셋 인벤토리",
        "",
        "- 생성 기준: `tools/audit_frontend_assets.py`",
        "- 대상: `services/frontend-app/src/assets`",
        "- 기준일: 2026-07-30",
        f"- 파일: {len(assets)}개 · {total_bytes / 1024 / 1024:.2f} MiB",
        "- 각 리소스의 미리보기, 실제 Vue 연결 상태, 노출 화면·위치, 직접 참조 파일과 1차 정비 분류를 함께 관리한다.",
        "",
        "## 문서 읽는 법",
        "",
        "- 각 영역의 미리보기 모음에서 ID와 이미지를 확인한다.",
        "- `화면·위치`는 아동이 실제로 보는 화면과 배치 역할이다.",
        "- `직접 참조`는 현재 파일을 import하거나 CSS URL로 참조하는 코드다.",
        "- `Vue 연결 확인`은 직접 참조부터 최종 Vue 컴포넌트까지 import 경로가 이어진 상태다.",
        "- `[TBD] 현재 src 코드 참조 없음`은 자동 삭제 대상이 아니다. 동적 경로나 외부 계약을 추가 확인하기 전까지 미결 상태로 둔다.",
        "",
        "## 형식 요약",
        "",
        "| 형식 | 개수 |",
        "| --- | ---: |",
    ]
    lines.extend(
        f"| `{extension}` | {count} |"
        for extension, count in sorted(extensions.items(), key=lambda item: (-item[1], item[0]))
    )

    for group, paths in sorted(grouped.items()):
        entries = [
            (f"{group[:2].upper()}{index:02d}", path)
            for index, path in enumerate(paths, start=1)
        ]
        sheet_path = create_contact_sheet(group, entries)
        lines.extend(["", f"## `{group}`", ""])
        if sheet_path:
            sheet_link = sheet_path.relative_to(OUTPUT.parent).as_posix()
            lines.extend([
                f"![{group} 리소스 미리보기 모음]({sheet_link})",
                "",
            ])
        lines.extend([
            "| 미리보기 | 리소스 | 크기·픽셀 | 연결 상태 | 화면·위치 | 직접 참조 | 분류·다음 검토 |",
            "| --- | --- | ---: | --- | --- | --- | --- |",
        ])
        for preview_id, path in entries:
            relative = path.relative_to(ASSET_ROOT)
            references = usage_files(path, relative, sources)
            vue_files = reachable_vue_files(relative, references, reverse_graph)
            state, note = classification(relative)
            size_kib = path.stat().st_size / 1024
            lines.append(
                "| "
                f"{preview_cell(preview_id, path)} | "
                f"`{relative.as_posix()}` | "
                f"{size_kib:.1f} KiB<br>{dimensions(path)} | "
                f"{connection_status(references, vue_files)} | "
                f"{usage_summary(relative, references, vue_files)} | "
                f"{reference_summary(references)} | "
                f"{state}<br>{note} |"
            )

    lines.extend([
        "",
        "## 누락 리소스",
        "",
        "| 리소스 | 표시 예정 화면·위치 | 상태 |",
        "| --- | --- | --- |",
        "| 쌍자음 카드 | 글자 학습 · 자모 선택 카드 | 신규 필요 |",
        "| 가방, 나비, 모자, 다리, 사과 그림 | 글자 학습 · 그림-문장/낱말 연결 카드 | 신규 필요 |",
        "| 기리 토끼 도움·일반 정답·올정답 완료 상태 | 글자 학습 · 화면 우측 안내/완료 | 신규 필요 |",
        "| 이야기 친구 정원 공통 캔버스 | 성장 정원 · 고정 4슬롯 | template 필요 |",
        "| 기리 토끼와 이야기 친구 음성 | 글자 학습 안내/성장 정원 감사 인사 | 녹음 필요 |",
        "",
        "신규·삭제·경로 변경 후에는 생성 스크립트를 다시 실행하고 문서 검증을 수행한다.",
        "",
    ])
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
