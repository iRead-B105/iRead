from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "contracts/database/schema.sql"
DEFAULT_OUTPUT = ROOT / "contracts/database/erd.md"


@dataclass(frozen=True)
class Column:
    name: str
    data_type: str
    nullable: bool
    primary_key: bool


@dataclass(frozen=True)
class ForeignKey:
    child_table: str
    child_column: str
    parent_table: str
    parent_column: str


CREATE_TABLE_PATTERN = re.compile(
    r"CREATE TABLE `(?P<table>[^`]+)` \(\s*(?P<body>.*?)\s*\);",
    re.DOTALL,
)
COLUMN_PATTERN = re.compile(
    r"^\s*`(?P<name>[^`]+)`\s+"
    r"(?P<type>[A-Za-z]+(?:\([^)]+\))?(?:\s+unsigned)?)\s+"
    r"(?P<nullability>NOT NULL|NULL)\b(?P<rest>.*)$",
    re.IGNORECASE,
)
ALTER_TABLE_PATTERN = re.compile(
    r"ALTER TABLE `(?P<table>[^`]+)`(?P<body>.*?);",
    re.DOTALL,
)
FOREIGN_KEY_PATTERN = re.compile(
    r"FOREIGN KEY \(`(?P<child_column>[^`]+)`\)\s+"
    r"REFERENCES `(?P<parent_table>[^`]+)` "
    r"\(`(?P<parent_column>[^`]+)`\)",
    re.IGNORECASE,
)


def parse_schema(sql: str) -> tuple[dict[str, list[Column]], list[ForeignKey]]:
    tables: dict[str, list[Column]] = {}
    for match in CREATE_TABLE_PATTERN.finditer(sql):
        columns: list[Column] = []
        for line in match.group("body").splitlines():
            column_match = COLUMN_PATTERN.match(line.rstrip(","))
            if not column_match:
                continue
            columns.append(
                Column(
                    name=column_match.group("name"),
                    data_type=column_match.group("type"),
                    nullable=column_match.group("nullability").upper() == "NULL",
                    primary_key="PRIMARY KEY" in column_match.group("rest").upper(),
                )
            )
        tables[match.group("table")] = columns

    foreign_keys: list[ForeignKey] = []
    for match in ALTER_TABLE_PATTERN.finditer(sql):
        child_table = match.group("table")
        for foreign_key in FOREIGN_KEY_PATTERN.finditer(match.group("body")):
            foreign_keys.append(
                ForeignKey(
                    child_table=child_table,
                    child_column=foreign_key.group("child_column"),
                    parent_table=foreign_key.group("parent_table"),
                    parent_column=foreign_key.group("parent_column"),
                )
            )
    return tables, foreign_keys


def mermaid_type(data_type: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", data_type).strip("_").upper()


def render_erd(sql: str) -> str:
    tables, foreign_keys = parse_schema(sql)
    foreign_key_columns = {
        (foreign_key.child_table, foreign_key.child_column)
        for foreign_key in foreign_keys
    }
    lines = [
        "---",
        "type: Contract Diagram",
        'title: "MySQL ERD"',
        'description: "Flyway와 동일한 MySQL 스키마 계약에서 자동 생성한 엔터티 관계도입니다."',
        "tags: [contracts, database, mysql, erd, generated]",
        "timestamp: 2026-07-25T00:00:00+09:00",
        "---",
        "# MySQL ERD",
        "",
        "- 상태: generated",
        "- 기준 원본: [Backend Flyway V1](../../services/backend/src/main/resources/db/migration/V1__baseline_schema.sql)",
        "- 검토용 미러: [schema.sql](schema.sql)",
        "- 생성 명령: `python tools/generate_erd.py`",
        "",
        "이 파일은 `contracts/database/schema.sql`의 테이블과 외래 키에서 자동 생성한다. 직접 수정하지 않고 스키마를 변경한 뒤 생성 명령을 다시 실행한다.",
        "",
        "```mermaid",
        "erDiagram",
    ]

    for table_name, columns in tables.items():
        lines.append(f"    {table_name} {{")
        for column in columns:
            keys = []
            if column.primary_key:
                keys.append("PK")
            if (table_name, column.name) in foreign_key_columns:
                keys.append("FK")
            key_suffix = f" {','.join(keys)}" if keys else ""
            nullability = "nullable" if column.nullable else "required"
            lines.append(
                f'        {mermaid_type(column.data_type)} {column.name}'
                f'{key_suffix} "{nullability}"'
            )
        lines.append("    }")

    for foreign_key in foreign_keys:
        child_columns = {
            column.name: column for column in tables[foreign_key.child_table]
        }
        child = child_columns[foreign_key.child_column]
        parent_cardinality = "o|" if child.nullable else "||"
        lines.append(
            f'    {foreign_key.parent_table} {parent_cardinality}--o{{ '
            f'{foreign_key.child_table} : "{foreign_key.child_column}"'
        )

    lines.extend(["```", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="MySQL schema contract에서 Mermaid ERD 문서를 생성한다."
    )
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="생성 결과가 현재 파일과 같은지만 확인한다.",
    )
    args = parser.parse_args()

    rendered = render_erd(args.schema.read_text(encoding="utf-8-sig"))
    if args.check:
        if not args.output.is_file():
            print(f"ERD output is missing: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print("ERD output is out of date. Run: python tools/generate_erd.py")
            return 1
        print("ERD output is up to date.")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    tables, foreign_keys = parse_schema(
        args.schema.read_text(encoding="utf-8-sig")
    )
    print(
        f"Wrote {args.output.relative_to(ROOT)}: "
        f"{len(tables)} tables, {len(foreign_keys)} foreign keys"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
