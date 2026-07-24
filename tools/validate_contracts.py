from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OPENAPI_FILES = (
    ROOT / "contracts/openapi/app-api.yaml",
    ROOT / "contracts/openapi/admin-api.yaml",
    ROOT / "contracts/openapi/auth-api.yaml",
)
SNAPSHOT = ROOT / "contracts/notion/spec-snapshot.json"
TRACEABILITY = ROOT / "contracts/traceability.json"
SCHEMA = ROOT / "contracts/database/schema.sql"
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}
OBSOLETE_PATHS = {
    "/api/app/story/{studentId}/{storyId}/branch-state",
    "/api/admin/student/{studentId}/communications",
    "/api/admin/student/{studentId}/learning-notes",
    "/api/admin/report/{reportId}/view",
    "/api/admin/report/generation",
    "/api/admin/report/{reportId}/draft-status",
    "/api/admin/report/{reportId}/publication",
    "/api/admin/report/{reportId}/share-management",
    "/api/admin/report/{reportId}/shares",
    "/api/admin/report/shared/{shareToken}",
}


def request_property_names(operation: dict[str, Any]) -> set[str]:
    names = {
        parameter.get("name", "")
        for parameter in operation.get("parameters", [])
    }
    for media in operation.get("requestBody", {}).get("content", {}).values():
        names.update(
            media.get("schema", {}).get("properties", {}).keys()
        )
    return names


def validate_openapi(
    snapshot: dict[str, Any], traceability: list[dict[str, Any]]
) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    operation_ids: list[str] = []
    notion_page_ids: list[str] = []
    feature_ids = {row["feature_id"] for row in traceability}
    review_counts: Counter[str] = Counter()
    operation_count = 0
    path_count = 0

    for path in OPENAPI_FILES:
        if not path.is_file():
            errors.append(f"missing OpenAPI file: {path.relative_to(ROOT)}")
            continue
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"{path.relative_to(ROOT)}: invalid YAML JSON subset: {error}")
            continue

        if document.get("openapi") != "3.1.0":
            errors.append(f"{path.relative_to(ROOT)}: openapi must be 3.1.0")
        paths = document.get("paths", {})
        path_count += len(paths)
        for route, path_item in paths.items():
            if route in OBSOLETE_PATHS:
                errors.append(f"{path.relative_to(ROOT)}: obsolete path remains: {route}")
            placeholders = set(re.findall(r"\{([^}]+)\}", route))
            for method, operation in path_item.items():
                if method not in HTTP_METHODS:
                    continue
                operation_count += 1
                operation_id = operation.get("operationId", "")
                if not operation_id:
                    errors.append(f"{method.upper()} {route}: missing operationId")
                operation_ids.append(operation_id)

                notion_page_id = operation.get("x-notion-page-id", "")
                if not notion_page_id:
                    errors.append(
                        f"{operation_id}: missing x-notion-page-id"
                    )
                notion_page_ids.append(notion_page_id)

                status = operation.get("x-review-status", "")
                if status not in {"reviewed", "needs-review"}:
                    errors.append(f"{operation_id}: invalid x-review-status")
                review_counts[status] += 1

                related = operation.get("x-feature-ids", [])
                unknown = sorted(set(related) - feature_ids)
                if unknown:
                    errors.append(
                        f"{operation_id}: unknown feature IDs {unknown}"
                    )

                path_parameters = {
                    parameter.get("name")
                    for parameter in operation.get("parameters", [])
                    if parameter.get("in") == "path"
                    and parameter.get("required") is True
                }
                if placeholders != path_parameters:
                    errors.append(
                        f"{operation_id}: path parameters {sorted(path_parameters)} "
                        f"do not match placeholders {sorted(placeholders)}"
                    )

                request_names = {
                    value.lower()
                    for value in request_property_names(operation)
                }
                if "teacherid" in request_names:
                    errors.append(
                        f"{operation_id}: teacherId must not be a client request field"
                    )

                if not operation.get("responses"):
                    errors.append(f"{operation_id}: missing responses")

    duplicate_operations = [
        value for value, count in Counter(operation_ids).items() if count > 1
    ]
    if duplicate_operations:
        errors.append(f"duplicate operationIds: {duplicate_operations}")

    duplicate_pages = [
        value for value, count in Counter(notion_page_ids).items() if count > 1
    ]
    if duplicate_pages:
        errors.append(f"duplicate Notion API page mappings: {duplicate_pages}")

    expected_api_pages = {api["page_id"] for api in snapshot["apis"]}
    if set(notion_page_ids) != expected_api_pages:
        missing = sorted(expected_api_pages - set(notion_page_ids))
        extra = sorted(set(notion_page_ids) - expected_api_pages)
        errors.append(
            f"OpenAPI/Notion API page mismatch: missing={missing}, extra={extra}"
        )

    return errors, {
        "paths": path_count,
        "operations": operation_count,
        "reviewed": review_counts["reviewed"],
        "needs_review": review_counts["needs-review"],
    }


def validate_traceability(
    snapshot: dict[str, Any], rows: list[dict[str, Any]]
) -> list[str]:
    errors: list[str] = []
    feature_ids = [row["feature_id"] for row in rows]
    duplicates = [
        value for value, count in Counter(feature_ids).items() if count > 1
    ]
    if duplicates:
        errors.append(f"duplicate feature IDs: {duplicates}")
    if any(not value for value in feature_ids):
        errors.append("empty feature ID exists")

    snapshot_features = {
        feature["feature_id"]: feature for feature in snapshot["features"]
    }
    if set(feature_ids) != set(snapshot_features):
        errors.append("traceability feature set differs from Notion snapshot")

    for row in rows:
        if row["deprecated"] and row["operation_ids"]:
            errors.append(
                f"{row['feature_id']}: deprecated feature linked to active API"
            )
        if not row["deprecated"] and not row["operation_ids"]:
            errors.append(
                f"{row['feature_id']}: active feature has no API operation"
            )
    return errors


def validate_snapshot(snapshot: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    api_pairs = [(api["path"], api["method"]) for api in snapshot["apis"]]
    duplicate_pairs = [
        value for value, count in Counter(api_pairs).items() if count > 1
    ]
    if duplicate_pairs:
        errors.append(f"duplicate Notion API method/path pairs: {duplicate_pairs}")

    forbidden_keys = {"우선순위", "구현여부"}

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            present = forbidden_keys.intersection(value)
            if present:
                errors.append(
                    f"snapshot contains excluded properties: {sorted(present)}"
                )
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(snapshot)
    return errors


def validate_schema() -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    if not SCHEMA.is_file():
        return ["missing contracts/database/schema.sql"], {
            "tables": 0,
            "primary_keys": 0,
        }
    sql = SCHEMA.read_text(encoding="utf-8-sig")
    tables = re.findall(r"CREATE TABLE `([^`]+)` \((.*?)\);", sql, re.DOTALL)
    primary_keys = re.findall(
        r"ALTER TABLE `([^`]+)` ADD CONSTRAINT `([^`]+)` PRIMARY KEY "
        r"\(\s*`([^`]+)`\s*\);",
        sql,
        re.DOTALL,
    )
    foreign_keys = re.findall(r"\bFOREIGN KEY\s*\(", sql, re.IGNORECASE)
    unique_constraints = re.findall(
        r"\bCONSTRAINT\s+`[^`]+`\s+UNIQUE\s*\(", sql, re.IGNORECASE
    )
    if len(tables) != len(primary_keys):
        errors.append(
            f"schema table/primary-key count mismatch: "
            f"{len(tables)}/{len(primary_keys)}"
        )
    table_names = {name for name, _ in tables}
    if "story_choices" in table_names:
        errors.append("obsolete story_choices table remains")
    story = dict(tables).get("stories", "")
    story_lines = dict(tables).get("story_lines", "")
    if "CHK_STORIES_PROGRESS" not in story:
        errors.append("stories progress check is missing")
    if "requires_branch_input" not in story_lines:
        errors.append("story_lines.requires_branch_input is missing")
    if re.search(r"\blong\b", sql, re.IGNORECASE) or "timestmap" in sql.lower():
        errors.append("legacy invalid MySQL type remains")
    forbidden_identifiers = (
        "achivement",
        "created__at",
        "story_templates_id",
        "`train_id`",
        "`Field`",
        "`Field2`",
    )
    for identifier in forbidden_identifiers:
        if identifier in sql:
            errors.append(f"legacy schema identifier remains: {identifier}")
    required_fragments = (
        "`student_word_stats`",
        "`student_id`\tbigint\tNOT NULL",
        "`word_id`\tbigint\tNOT NULL",
        "`is_representative`\tboolean\tNOT NULL",
        "UK_STUDENT_WORD_STATS",
        "UK_STORY_LINES_SEQUENCE",
        "FK_STORIES_STUDENT",
        "FK_STORIES_STORY_TEMPLATE",
        "FK_REPORTS_STUDENT",
        "CHK_GAZE_SESSIONS_CONTENT",
        "CHK_REPORTS_PERIOD",
    )
    for fragment in required_fragments:
        if fragment not in sql:
            errors.append(f"required schema contract is missing: {fragment}")
    if len(foreign_keys) < 20:
        errors.append(
            f"schema has too few foreign keys: {len(foreign_keys)}"
        )
    if len(unique_constraints) < 8:
        errors.append(
            f"schema has too few unique constraints: {len(unique_constraints)}"
        )
    return errors, {
        "tables": len(tables),
        "primary_keys": len(primary_keys),
        "foreign_keys": len(foreign_keys),
        "unique_constraints": len(unique_constraints),
    }


def main() -> int:
    missing = [
        path.relative_to(ROOT)
        for path in (SNAPSHOT, TRACEABILITY)
        if not path.is_file()
    ]
    if missing:
        print("Missing contract inputs:")
        for path in missing:
            print(f"  - {path}")
        return 1

    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    traceability = json.loads(TRACEABILITY.read_text(encoding="utf-8"))

    errors = validate_snapshot(snapshot)
    openapi_errors, openapi_stats = validate_openapi(snapshot, traceability)
    errors.extend(openapi_errors)
    errors.extend(validate_traceability(snapshot, traceability))
    schema_errors, schema_stats = validate_schema()
    errors.extend(schema_errors)

    if errors:
        print("Contract validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "Contract validation passed: "
        f"{openapi_stats['operations']} operations, "
        f"{len(traceability)} features, "
        f"{openapi_stats['reviewed']} reviewed, "
        f"{openapi_stats['needs_review']} need review, "
        f"{schema_stats['tables']} MySQL tables, "
        f"{schema_stats['foreign_keys']} foreign keys."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
