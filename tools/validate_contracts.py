from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from contract_resolutions import load_resolutions, resolve_snapshot
from generate_erd import render_erd


ROOT = Path(__file__).resolve().parents[1]
OPENAPI_FILES = (
    ROOT / "contracts/openapi/app-api.yaml",
    ROOT / "contracts/openapi/admin-api.yaml",
    ROOT / "contracts/openapi/auth-api.yaml",
    ROOT / "contracts/openapi/ai-api.yaml",
)
NOTION_OPENAPI_FILES = set(OPENAPI_FILES[:3])
AI_OPENAPI = ROOT / "contracts/openapi/ai-api.yaml"
SNAPSHOT = ROOT / "contracts/notion/spec-snapshot.json"
RESOLUTIONS = ROOT / "contracts/api-resolutions.json"
TRACEABILITY = ROOT / "contracts/traceability.json"
SCHEMA = ROOT / "contracts/database/schema.sql"
ERD = ROOT / "contracts/database/erd.md"
FLYWAY_MIGRATIONS = (
    ROOT / "services/backend/src/main/resources/db/migration"
)
BACKEND_JAVA = ROOT / "services/backend/src/main/java"
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
        if path in NOTION_OPENAPI_FILES:
            components = document.get("components", {})
            schema_names = set(components.get("schemas", {}))
            required_schemas = {
                "ErrorDetail",
                "ErrorResponse",
                "SuccessResponse",
            }
            if not required_schemas.issubset(schema_names):
                errors.append(
                    f"{path.relative_to(ROOT)}: missing common schemas "
                    f"{sorted(required_schemas - schema_names)}"
                )
            required_responses = {
                "BadRequest",
                "Unauthorized",
                "Forbidden",
                "NotFound",
                "Conflict",
                "TooManyRequests",
                "BadGateway",
            }
            response_names = set(components.get("responses", {}))
            if not required_responses.issubset(response_names):
                errors.append(
                    f"{path.relative_to(ROOT)}: missing common responses "
                    f"{sorted(required_responses - response_names)}"
                )
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

                if path in NOTION_OPENAPI_FILES:
                    contract_source = operation.get(
                        "x-contract-source",
                        "notion",
                    )
                    notion_page_id = operation.get("x-notion-page-id", "")
                    if contract_source == "notion" and not notion_page_id:
                        errors.append(
                            f"{operation_id}: missing x-notion-page-id"
                        )
                    elif contract_source == "notion":
                        notion_page_ids.append(notion_page_id)
                    elif contract_source != "git":
                        errors.append(
                            f"{operation_id}: invalid x-contract-source"
                        )

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
        responsibility = row.get("responsibility")
        if responsibility not in {"server", "client", "unmapped"}:
            errors.append(
                f"{row['feature_id']}: invalid responsibility {responsibility}"
            )
        if (
            not row["deprecated"]
            and not row["operation_ids"]
            and responsibility != "client"
        ):
            errors.append(
                f"{row['feature_id']}: active feature has no API operation"
            )
        if responsibility == "client" and row["operation_ids"]:
            errors.append(
                f"{row['feature_id']}: client feature has server API operation"
            )
    return errors


def validate_ai_contract() -> list[str]:
    errors: list[str] = []
    document = json.loads(AI_OPENAPI.read_text(encoding="utf-8"))
    expected_paths = {
        "/api/v1/trainings/generate",
        "/api/v1/trainings/evaluate",
        "/api/v1/story/generate",
        "/api/v1/story/continue",
        "/api/v1/speech/transcribe",
        "/api/v1/speech/pronunciation/analyze",
        "/api/v1/speech/synthesize",
        "/api/v1/gaze/analyze",
    }
    actual_paths = set(document.get("paths", {}))
    if actual_paths != expected_paths:
        errors.append(
            "Backend-AI path mismatch: "
            f"missing={sorted(expected_paths - actual_paths)}, "
            f"extra={sorted(actual_paths - expected_paths)}"
        )

    api_key = (
        document.get("components", {})
        .get("securitySchemes", {})
        .get("apiKeyAuth", {})
    )
    if api_key != {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-Key",
    }:
        errors.append("Backend-AI X-API-Key security scheme is invalid")

    for route, path_item in document.get("paths", {}).items():
        operation = path_item.get("post", {})
        if operation.get("security") != [{"apiKeyAuth": []}]:
            errors.append(f"POST {route}: apiKeyAuth is required")
        parameters = operation.get("parameters", [])
        if {"$ref": "#/components/parameters/IdempotencyKey"} not in parameters:
            errors.append(f"POST {route}: Idempotency-Key is required")
        timeout = operation.get("x-timeout-ms")
        if not isinstance(timeout, int) or timeout <= 0:
            errors.append(f"POST {route}: positive x-timeout-ms is required")
        if not operation.get("x-retry-policy"):
            errors.append(f"POST {route}: x-retry-policy is required")
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
    expected_erd = render_erd(sql)
    if not ERD.is_file():
        errors.append("missing generated database ERD")
    elif ERD.read_text(encoding="utf-8") != expected_erd:
        errors.append(
            "database ERD is out of date; run python tools/generate_erd.py"
        )
    flyway_baseline = FLYWAY_MIGRATIONS / "V1__baseline_schema.sql"
    if not flyway_baseline.is_file():
        errors.append("missing backend Flyway V1 baseline")
    else:
        baseline_sql = flyway_baseline.read_text(encoding="utf-8-sig")
        baseline_tables = set(re.findall(r"CREATE TABLE `([^`]+)`", baseline_sql))
        current_tables = set(re.findall(r"CREATE TABLE `([^`]+)`", sql))
        if baseline_sql != sql:
            errors.append(
                "schema contract must exactly match the single Flyway V1 baseline"
            )
    migration_files = sorted(FLYWAY_MIGRATIONS.glob("V*__*.sql"))
    migration_versions = [
        re.match(r"V(\d+)__", path.name).group(1)
        for path in migration_files
        if re.match(r"V(\d+)__", path.name)
    ]
    if len(migration_versions) != len(set(migration_versions)):
        errors.append("duplicate backend Flyway migration version")
    if [path.name for path in migration_files] != ["V1__baseline_schema.sql"]:
        errors.append("backend Flyway must use a single V1 baseline before DB rollout")
    tables = re.findall(r"CREATE TABLE `([^`]+)` \((.*?)\);", sql, re.DOTALL)
    primary_keys = re.findall(r"\bPRIMARY KEY\b", sql, re.IGNORECASE)
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
    if "test" in table_names or "tests" not in table_names:
        errors.append("test table must use the backend-compatible name tests")
    renamed_data_tables = {"training_contents", "test_questions"} & table_names
    if renamed_data_tables:
        errors.append(
            f"renamed data table names remain: {sorted(renamed_data_tables)}"
        )
    for required_table in (
        "training_datas",
        "test_datas",
        "test_curriculums",
        "story_scenes",
        "story_choices",
        "reading_features",
        "student_feature_profiles",
    ):
        if required_table not in table_names:
            errors.append(f"required table is missing: {required_table}")
    if "auth_refresh_sessions" not in table_names:
        errors.append("required auth table is missing: auth_refresh_sessions")
    if "auth_revoked_access_tokens" in table_names:
        errors.append("unused auth_revoked_access_tokens table remains")
    application_assigned_ids = {
        "test_curriculums",
        "test_datas",
        "reading_features",
        "student_feature_profiles",
    }
    for table_name, definition in tables:
        id_column = re.search(r"`id`\s+bigint\s+NOT NULL([^\n]*)", definition)
        if (
            id_column
            and table_name not in application_assigned_ids
            and "AUTO_INCREMENT" not in id_column.group(1)
        ):
            errors.append(f"{table_name}.id must be AUTO_INCREMENT")
    story = dict(tables).get("stories", "")
    story_lines = dict(tables).get("story_lines", "")
    if "CHK_STORIES_PROGRESS" not in story:
        errors.append("stories progress check is missing")
    if "has_choices" not in story_lines:
        errors.append("story_lines.has_choices is missing")
    if re.search(r"\blong\b", sql, re.IGNORECASE) or "timestmap" in sql.lower():
        errors.append("legacy invalid MySQL type remains")
    forbidden_identifiers = (
        "achivement",
        "created__at",
        "story_templates_id",
        "`login_id`",
        "`Field`",
        "`Field2`",
    )
    for identifier in forbidden_identifiers:
        if identifier in sql:
            errors.append(f"legacy schema identifier remains: {identifier}")
    required_fragments = (
        "CREATE TABLE `tests`",
        "CREATE TABLE `test_curriculums`",
        "CREATE TABLE `story_scenes`",
        "CREATE TABLE `story_choices`",
        "CREATE TABLE `reading_features`",
        "CREATE TABLE `student_feature_profiles`",
        "`train_id` bigint NOT NULL",
        "`progress` tinyint unsigned NOT NULL",
        "`scene_id` bigint NOT NULL",
        "`has_choices` boolean NOT NULL",
        "`use_location` varchar(10) NOT NULL",
        "`data` json NULL",
        "`start_date` timestamp NOT NULL",
        "`end_date` timestamp NOT NULL",
        "UK_STORY_LINES_SEQUENCE",
        "UK_STORY_CHOICES_STORY_LINE",
        "UK_TESTS_SEQUENCE",
        "FK_STORIES_STUDENT",
        "FK_STORIES_STORY_TEMPLATE",
        "FK_STORY_SCENES_STORY",
        "FK_STORY_LINES_SCENE",
        "FK_STORY_CHOICES_STORY_LINE",
        "FK_TESTS_TEST_CURRICULUM",
        "FK_TESTS_TRAINING_TEMPLATE",
        "FK_TEST_CURRICULUMS_STUDENT",
        "FK_TEST_DATAS_TEST",
        "FK_REPORTS_STUDENT",
        "CHK_AUTH_REFRESH_SESSIONS_AUDIENCE",
        "CHK_GAZE_SESSIONS_CONTENT",
        "CHK_WORD_ATTEMPT_LOGS_LOCATION",
        "CHK_REPORTS_PERIOD",
        "UK_TEACHERS_EMAIL",
        "UK_AUTH_REFRESH_SESSIONS_TOKEN_HASH",
    )
    for fragment in required_fragments:
        if fragment not in sql:
            errors.append(f"required schema contract is missing: {fragment}")
    removed_tables = {
        "student_study_progresses",
        "student_word_stats",
        "sounds",
        "images",
        "videos",
    } & table_names
    if removed_tables:
        errors.append(
            f"tables removed by the approved ERD remain: {sorted(removed_tables)}"
        )
    if len(foreign_keys) < 31:
        errors.append(
            f"schema has too few foreign keys: {len(foreign_keys)}"
        )
    if len(unique_constraints) < 11:
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
        for path in (SNAPSHOT, RESOLUTIONS, TRACEABILITY)
        if not path.is_file()
    ]
    if missing:
        print("Missing contract inputs:")
        for path in missing:
            print(f"  - {path}")
        return 1

    raw_snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    try:
        snapshot = resolve_snapshot(
            raw_snapshot,
            load_resolutions(RESOLUTIONS),
        )
    except (KeyError, TypeError, ValueError) as error:
        print(f"Invalid contract resolutions: {error}")
        return 1
    traceability = json.loads(TRACEABILITY.read_text(encoding="utf-8"))

    errors = validate_snapshot(raw_snapshot)
    openapi_errors, openapi_stats = validate_openapi(snapshot, traceability)
    errors.extend(openapi_errors)
    errors.extend(validate_ai_contract())
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
