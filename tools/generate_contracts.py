from __future__ import annotations

import argparse
import html
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from contract_resolutions import load_resolutions, resolve_snapshot


HTTP_METHODS = {"get", "post", "put", "patch", "delete"}
FEATURE_DATABASE_URL = (
    "https://app.notion.com/p/de0027df905383e98fb00120c64321fc"
)
PREFIX_FILES = {
    "app": "app-api.yaml",
    "admin": "admin-api.yaml",
    "auth": "auth-api.yaml",
}
ERROR_RESPONSES = {
    "400": ("BadRequest", "요청값 검증 실패"),
    "401": ("Unauthorized", "인증 실패"),
    "403": ("Forbidden", "접근 권한 없음"),
    "404": ("NotFound", "리소스를 찾을 수 없음"),
    "409": ("Conflict", "현재 상태와 요청 충돌"),
    "429": ("TooManyRequests", "요청 한도 초과"),
    "502": ("BadGateway", "외부 처리 실패"),
}


def operation_id(api: dict[str, Any]) -> str:
    prefix = api_prefix(api["path"])
    tokens = []
    for part in api["path"].strip("/").split("/"):
        if part in {"api", prefix}:
            continue
        token = part.strip("{}")
        token = re.sub(r"[^A-Za-z0-9]+", "_", token).strip("_")
        if part.startswith("{"):
            token = f"by_{token}"
        if token:
            tokens.append(token)
    joined = "_".join(tokens)
    return f"{api['method'].lower()}_{prefix}_{joined}"


def api_prefix(path: str) -> str:
    match = re.match(r"^/api/([^/]+)", path)
    return match.group(1) if match else "other"


def schema_for_type(raw_type: str, field_name: str = "") -> dict[str, Any]:
    value = html.unescape(raw_type).strip().lower().replace(" ", "")
    array_match = re.fullmatch(r"(?:array<(.+)>|(.+)\[\])", value)
    if array_match:
        inner = array_match.group(1) or array_match.group(2) or "object"
        return {"type": "array", "items": schema_for_type(inner)}
    if value in {"number", "float", "double", "decimal"}:
        return {"type": "number"}
    if value in {"integer", "int", "long"}:
        return {"type": "integer", "format": "int64"}
    if value in {"boolean", "bool"}:
        return {"type": "boolean"}
    if value in {"object", "json", "map"}:
        return {"type": "object", "additionalProperties": True}
    if value in {"file", "binary"}:
        return {"type": "string", "format": "binary"}
    string_match = re.fullmatch(r"string\(([^)]+)\)", value)
    if string_match:
        qualifier = string_match.group(1)
        schema = {"type": "string"}
        if qualifier in {"date", "date-time", "uuid"}:
            schema["format"] = qualifier
        elif "|" in qualifier:
            schema["enum"] = qualifier.split("|")
        return schema

    schema: dict[str, Any] = {"type": "string"}
    lowered_name = field_name.lower()
    if lowered_name.endswith("date") and not lowered_name.endswith("updatedate"):
        schema["format"] = "date"
    if lowered_name.endswith(("at", "datetime")):
        schema["format"] = "date-time"
    return schema


def add_response_field(
    properties: dict[str, Any], field: dict[str, Any]
) -> None:
    name = field["name"]
    description = field.get("description", "")
    if "[]." in name:
        root, child = name.split("[].", 1)
        root_schema = properties.setdefault(
            root,
            {"type": "array", "items": {"type": "object", "properties": {}}},
        )
        item_properties = root_schema.setdefault("items", {}).setdefault(
            "properties", {}
        )
        child_schema = schema_for_type(field.get("type", "string"), child)
        if description:
            child_schema["description"] = description
        item_properties[child] = child_schema
        return

    normalized = name.removesuffix("[]")
    schema = schema_for_type(field.get("type", "string"), normalized)
    if name.endswith("[]") and schema.get("type") != "array":
        schema = {"type": "array", "items": schema}
    if description:
        schema["description"] = description
    properties[normalized] = schema


def parse_example(text: str) -> Any | None:
    if not text.strip():
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def request_body(api: dict[str, Any]) -> dict[str, Any] | None:
    body_parameters = [
        parameter
        for parameter in api["request_parameters"]
        if parameter["in"].strip().lower() == "body"
    ]
    if not body_parameters:
        return None

    properties: dict[str, Any] = {}
    required: list[str] = []
    binary = False
    for parameter in body_parameters:
        schema = schema_for_type(parameter["type"], parameter["name"])
        if schema.get("format") == "binary":
            binary = True
        if parameter.get("description"):
            schema["description"] = parameter["description"]
        properties[parameter["name"]] = schema
        if parameter["required"]:
            required.append(parameter["name"])

    body_schema: dict[str, Any] = {"type": "object", "properties": properties}
    if required:
        body_schema["required"] = required
    media_type = "multipart/form-data" if binary else "application/json"
    media: dict[str, Any] = {"schema": body_schema}
    example = parse_example(api.get("request_example", ""))
    if isinstance(example, dict):
        body_example = example.get("body", example)
        if body_example:
            media["example"] = body_example
    return {
        "required": bool(required),
        "content": {media_type: media},
    }


def openapi_parameters(api: dict[str, Any]) -> list[dict[str, Any]]:
    parameters: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for parameter in api["request_parameters"]:
        location = parameter["in"].strip().lower()
        if location == "body":
            continue
        if location not in {"path", "query", "header", "cookie"}:
            continue
        key = (parameter["name"], location)
        if key in seen:
            continue
        seen.add(key)
        item: dict[str, Any] = {
            "name": parameter["name"],
            "in": location,
            "required": True if location == "path" else parameter["required"],
            "schema": schema_for_type(parameter["type"], parameter["name"]),
        }
        if parameter.get("description"):
            item["description"] = parameter["description"]
        parameters.append(item)

    path_names = re.findall(r"\{([^}]+)\}", api["path"])
    existing = {
        parameter["name"]
        for parameter in parameters
        if parameter["in"] == "path"
    }
    for name in path_names:
        if name not in existing:
            parameters.append(
                {
                    "name": name,
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                    "description": f"{name} 식별자",
                }
            )
    return parameters


def success_response(api: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    success_codes = [
        code for code in api["response_codes"] if code.startswith("2")
    ]
    status = success_codes[0] if success_codes else "200"
    if status == "204":
        return status, {"description": "요청 성공"}
    if api.get("response_media_type") and api.get("response_schema"):
        return status, {
            "description": "요청 성공",
            "content": {
                api["response_media_type"]: {
                    "schema": api["response_schema"],
                }
            },
        }

    fields = [
        field for field in api["response_fields"] if field["name"] != "success"
    ]
    properties: dict[str, Any] = {}
    for field in fields:
        add_response_field(properties, field)

    if properties:
        required_fields = list(
            dict.fromkeys(
                field["name"].removesuffix("[]")
                for field in fields
                if field.get("required") and "[]." not in field["name"]
            )
        )
        data_schema: dict[str, Any] = {
            "type": "object",
            "properties": properties,
        }
        if required_fields:
            data_schema["required"] = required_fields
        schema: dict[str, Any] = {
            "allOf": [
                {"$ref": "#/components/schemas/SuccessResponse"},
                {
                    "type": "object",
                    "properties": {"data": data_schema},
                    "required": ["data"],
                },
            ]
        }
    else:
        schema = {"$ref": "#/components/schemas/SuccessResponse"}

    media: dict[str, Any] = {"schema": schema}
    example = parse_example(api.get("response_example", ""))
    if example is not None:
        media["example"] = example
    return status, {
        "description": "요청 성공",
        "content": {"application/json": media},
    }


def api_operation(
    api: dict[str, Any],
    feature_by_page: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    related_features = [
        feature_by_page[page_id]
        for page_id in api["feature_ids"]
        if page_id in feature_by_page
    ]
    feature_ids = [
        feature["feature_id"] for feature in related_features if feature["feature_id"]
    ]
    feature_names = [
        feature["name"]
        for feature in related_features
        if not feature["name"].startswith("[폐기]")
    ]
    summary = ", ".join(feature_names[:3]) or f"{api['method']} {api['path']}"
    operation: dict[str, Any] = {
        "operationId": operation_id(api),
        "summary": summary,
        "tags": [api["domain"] or api_prefix(api["path"])],
        "parameters": openapi_parameters(api),
        "responses": {},
        "x-notion-page-id": api["page_id"],
        "x-notion-url": api["url"],
        "x-feature-ids": feature_ids,
    }
    if api.get("note"):
        operation["description"] = api["note"]
    if api.get("request_summary"):
        operation["x-notion-request-summary"] = api["request_summary"]
    if api.get("response_summary"):
        operation["x-notion-response-summary"] = api["response_summary"]
    operation["x-review-status"] = (
        "needs-review" if "검수 필요" in api.get("note", "") else "reviewed"
    )

    body = request_body(api)
    if body:
        operation["requestBody"] = body

    success_status, success = success_response(api)
    operation["responses"][success_status] = success
    for status in api["response_codes"]:
        if status.startswith("2"):
            continue
        response_component = ERROR_RESPONSES.get(status)
        if response_component:
            operation["responses"][status] = {
                "$ref": f"#/components/responses/{response_component[0]}"
            }
        else:
            operation["responses"][status] = {
                "description": "요청 실패",
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/ErrorResponse"
                        }
                    }
                },
            }

    if api_prefix(api["path"]) != "auth":
        operation["security"] = [{"bearerAuth": []}]
    return operation


def openapi_document(
    prefix: str,
    apis: list[dict[str, Any]],
    feature_by_page: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    paths: dict[str, Any] = {}
    for api in sorted(apis, key=lambda item: (item["path"], item["method"])):
        paths.setdefault(api["path"], {})[api["method"].lower()] = api_operation(
            api, feature_by_page
        )
    return {
        "openapi": "3.1.0",
        "info": {
            "title": f"iRead {prefix.capitalize()} API",
            "version": "0.1.0",
            "description": (
                "Notion API 명세에서 이전한 계약이다. "
                "x-notion-* 확장 필드는 원본 추적에 사용한다."
            ),
        },
        "paths": paths,
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
            "schemas": {
                "ErrorDetail": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "message": {"type": "string"},
                    },
                    "required": ["code", "message"],
                },
                "ErrorResponse": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "$ref": "#/components/schemas/ErrorDetail"
                        },
                    },
                    "required": ["error"],
                },
                "SuccessResponse": {
                    "type": "object",
                    "properties": {"success": {"type": "boolean"}},
                    "required": ["success"],
                },
            },
            "responses": {
                component_name: {
                    "description": description,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ErrorResponse"
                            }
                        }
                    },
                }
                for component_name, description in ERROR_RESPONSES.values()
            },
        },
    }


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\r", "").replace("\n", "<br>")


def feature_domain(
    feature: dict[str, Any], api_by_page: dict[str, dict[str, Any]]
) -> str:
    domains = sorted(
        {
            api_by_page[page_id]["domain"]
            for page_id in feature["api_page_ids"]
            if page_id in api_by_page and api_by_page[page_id]["domain"]
        }
    )
    if domains:
        return domains[0]
    if feature.get("contract_domain"):
        return feature["contract_domain"]
    if feature["name"].startswith("[폐기]"):
        return "deprecated"
    return "unmapped"


def write_feature_catalogs(
    features: list[dict[str, Any]],
    apis: list[dict[str, Any]],
    output_dir: Path,
) -> None:
    api_by_page = {api["page_id"]: api for api in apis}
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for feature in features:
        groups[feature_domain(feature, api_by_page)].append(feature)

    output_dir.mkdir(parents=True, exist_ok=True)
    index_lines = [
        "# 기능 카탈로그",
        "",
        "Notion 기능 명세를 도메인별 OKF 개념 문서로 이전한 카탈로그다.",
        "",
    ]
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    for domain, items in sorted(groups.items()):
        filename = f"{domain}.md"
        index_lines.append(
            f"* [{domain}]({filename}) - {len(items)}개 기능 항목"
        )
        lines = [
            "---",
            "type: Feature Catalog",
            f'title: "기능 카탈로그: {domain}"',
            f'description: "{domain} 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."',
            f"tags: [feature, catalog, {domain}]",
            f"timestamp: {timestamp}",
            "---",
            f"# 기능 카탈로그: {domain}",
            "",
            "| 기능 ID | 기능 | 설명 | 책임 | API operationId |",
            "| --- | --- | --- | --- | --- |",
        ]
        for feature in sorted(
            items, key=lambda item: (item["feature_id"], item["name"])
        ):
            operations = [
                operation_id(api_by_page[page_id])
                for page_id in feature["api_page_ids"]
                if page_id in api_by_page
            ]
            operation_text = ", ".join(f"`{value}`" for value in operations) or "-"
            responsibility = feature.get(
                "contract_responsibility",
                "server" if operations else "-",
            )
            lines.append(
                "| "
                + " | ".join(
                    [
                        markdown_escape(feature["feature_id"]),
                        markdown_escape(feature["name"]),
                        markdown_escape(feature["description"]),
                        responsibility,
                        operation_text,
                    ]
                )
                + " |"
            )
        lines.extend(
            [
                "",
                "# Sources",
                "",
                f"[Notion 기능 명세]({FEATURE_DATABASE_URL})",
                "",
            ]
        )
        (output_dir / filename).write_text(
            "\n".join(lines), encoding="utf-8"
        )

    (output_dir / "index.md").write_text(
        "\n".join(index_lines) + "\n", encoding="utf-8"
    )


def traceability(
    features: list[dict[str, Any]], apis: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    api_by_page = {api["page_id"]: api for api in apis}
    rows = []
    for feature in features:
        related = [
            api_by_page[page_id]
            for page_id in feature["api_page_ids"]
            if page_id in api_by_page
        ]
        rows.append(
            {
                "feature_id": feature["feature_id"],
                "feature_page_id": feature["page_id"],
                "deprecated": feature["name"].startswith("[폐기]"),
                "responsibility": feature.get(
                    "contract_responsibility",
                    "server" if related else "unmapped",
                ),
                "api_page_ids": [api["page_id"] for api in related],
                "operation_ids": [operation_id(api) for api in related],
            }
        )
    return rows


def review_reasons(api: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if "검수 필요" in api.get("note", ""):
        reasons.append("Notion 주석에 검수 필요 표시")
    raw_types = [
        parameter["type"] for parameter in api["request_parameters"]
    ] + [field["type"] for field in api["response_fields"]]
    if any("enum" in html.unescape(value).lower() for value in raw_types):
        reasons.append("ENUM 허용값 미정의")
    if api["request_summary"] and not api["request_parameters"]:
        reasons.append("요청 요약은 있으나 상세 요청 표가 없음")
    success_codes = [
        code for code in api["response_codes"] if code.startswith("2")
    ]
    if (
        api["response_summary"]
        and not api["response_fields"]
        and not api.get("response_schema")
        and "204" not in success_codes
    ):
        reasons.append("응답 요약은 있으나 상세 응답 표가 없음")
    return reasons


REVIEW_RECOMMENDATIONS = {
    "/api/admin/navigation/sidebar": (
        "클라이언트 화면 상태",
        "권한 정보로 클라이언트가 메뉴를 구성하고 API는 제거",
    ),
    "/api/admin/report/selection": (
        "클라이언트 화면 상태",
        "학생 목록 조회 결과를 사용하고 API는 제거",
    ),
    "/api/admin/student/actions": (
        "클라이언트 화면 상태",
        "권한과 학생 상태로 버튼을 구성하고 API는 제거",
    ),
    "/api/admin/student/filter": (
        "기존 API 통합",
        "학생 목록의 query parameter로 통합",
    ),
    "/api/admin/student/list-state": (
        "클라이언트 화면 상태",
        "학생 목록 응답과 클라이언트 상태로 대체",
    ),
    "/api/admin/student/selection": (
        "클라이언트 화면 상태",
        "클라이언트 선택 상태로 전환하고 API는 제거",
    ),
    "/api/admin/student/{studentId}/form": (
        "기존 API 통합",
        "GET /api/admin/student/{studentId}로 통합",
    ),
    "/api/admin/student/{studentId}/form-submit": (
        "기존 API 통합",
        "PATCH /api/admin/student/{studentId}로 통합",
    ),
    "/api/admin/student/{studentId}/reading-accuracy-trend": (
        "기존 API 통합",
        "GET /api/admin/student/{studentId}/accuracy-trend로 통합",
    ),
    "/api/admin/teacher/profile/edit": (
        "기존 API 통합",
        "GET /api/admin/teacher/info로 통합",
    ),
    "/api/admin/teacher/profile/view": (
        "기존 API 통합",
        "GET /api/admin/teacher/info로 통합",
    ),
    "/api/admin/teacher/profile/save-state": (
        "경로 정규화",
        "PATCH /api/admin/teacher/info로 이름과 계약을 정규화",
    ),
    "/api/admin/test/{studentId}/comparison-selection": (
        "기존 API 통합",
        "GET /api/admin/test/{studentId}/compare의 query parameter로 통합",
    ),
    "/api/admin/training/{studentId}/history/filter": (
        "기존 API 통합",
        "훈련 이력 조회의 query parameter로 통합",
    ),
    "/api/admin/training/{studentId}/history/selection": (
        "클라이언트 화면 상태",
        "클라이언트 선택 상태로 전환하고 API는 제거",
    ),
    "/api/admin/training/{studentId}/{curriculumId}/curriculum-editor": (
        "기존 API 통합",
        "PATCH /api/admin/training/{studentId}/{curriculumId}로 통합",
    ),
    "/api/admin/training/{studentId}/{curriculumId}/editor-selection": (
        "기존 API 통합",
        "GET /api/admin/training/{studentId}/{curriculumId}로 통합",
    ),
    "/api/app/story/{studentId}/{storyId}/guide": (
        "클라이언트 화면 상태",
        "사용 안내는 앱 정적 자원으로 관리하고 API는 제거",
    ),
    "/api/app/story/{studentId}/{storyId}/navigation": (
        "기존 API 통합",
        "이야기 장면 조회 응답으로 통합",
    ),
    "/api/app/story/{studentId}/{storyTemplateId}/detail-state": (
        "기존 API 통합",
        "GET /api/app/story/{studentId}/{storyTemplateId}로 통합",
    ),
    "/api/app/user/home-navigation": (
        "클라이언트 화면 상태",
        "인증 사용자 정보로 앱이 이동을 결정하고 API는 제거",
    ),
    "/api/app/user/session-navigation": (
        "클라이언트 화면 상태",
        "세션·화면 이동 상태를 클라이언트로 이전하고 API는 제거",
    ),
}


def review_recommendation(api: dict[str, Any]) -> tuple[str, str]:
    path = api["path"]
    if path in REVIEW_RECOMMENDATIONS:
        return REVIEW_RECOMMENDATIONS[path]
    if path.endswith("/audio-state"):
        return (
            "클라이언트 화면 상태",
            "문항 응답의 음성 URL과 클라이언트 재생 상태로 대체",
        )
    if path.endswith("/intro-navigation"):
        return (
            "기존 API 통합",
            "해당 학습의 intro 조회 응답으로 통합",
        )
    if path.endswith("/question-navigation"):
        return (
            "기존 API 통합",
            "문항 번호 기반 GET 문항 조회로 통합",
        )
    if path.endswith("/questions/display-state"):
        return (
            "기존 API 통합",
            "문항 번호 기반 GET 문항 조회로 통합",
        )
    if path.endswith("/recording-state"):
        return (
            "기존 API 통합",
            "문항별 recordings 업로드 API로 통합",
        )
    if path.endswith("/selection-state"):
        return (
            "기존 API 통합",
            "문항별 responses 저장 API로 통합",
        )
    if path.endswith("/session-reset"):
        return (
            "세션 계약 정리",
            "start의 재시작 의미 또는 별도 reset 필요성을 결정",
        )
    if path.endswith("/submission-status"):
        return (
            "경로 정규화",
            "상태 조회형 이름 대신 submit 또는 complete 명령으로 정규화",
        )
    return (
        "서버 계약 상세화",
        "ERD 필드와 요청·응답 의미를 대조한 뒤 유지",
    )


def write_review_queue(apis: list[dict[str, Any]], output: Path) -> None:
    rows = [
        (api, review_reasons(api))
        for api in apis
        if review_reasons(api)
    ]
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    lines = [
        "---",
        "type: Contract Review Queue",
        'title: "API 계약 검토 목록"',
        'description: "Notion에서 OpenAPI로 이전했지만 추가 의미 검토가 필요한 API를 정리합니다."',
        "tags: [contracts, openapi, review]",
        f"timestamp: {timestamp}",
        "---",
        "# API 계약 검토 목록",
        "",
        f"활성 API {len(apis)}건 가운데 {len(rows)}건에 추가 검토 표시가 남아 있다.",
        "",
        "권장 처리는 기존 ERD와 정식 도메인 API를 우선하고, 화면 이동·선택·재생 상태는 클라이언트 책임으로 분리한 결과다.",
        "",
        "| API | 분류 | 권장 처리 | 검토 사유 | Notion |",
        "| --- | --- | --- | --- | --- |",
    ]
    for api, reasons in sorted(
        rows, key=lambda item: (item[0]["path"], item[0]["method"])
    ):
        category, recommendation = review_recommendation(api)
        lines.append(
            f"| `{api['method']} {api['path']}` "
            f"| {category} "
            f"| {markdown_escape(recommendation)} "
            f"| {markdown_escape(', '.join(reasons))} "
            f"| [원본]({api['url']}) |"
        )
    lines.extend(
        [
            "",
            "## 별도 미결 사항",
            "",
            "- Backend–AI 내부 계약은 `contracts/openapi/ai-api.yaml`에서 관리한다.",
            "- Backend MySQL Flyway 누적 migration과 실행 검증 결과는 `contracts/database/backend-alignment.md`에서 관리한다.",
            "- 기존 데이터가 있는 환경은 V1 직접 적용 전에 별도 baseline과 변환 migration이 필요하다.",
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=Path("contracts/notion/spec-snapshot.json"),
    )
    parser.add_argument(
        "--resolutions",
        type=Path,
        default=Path("contracts/api-resolutions.json"),
    )
    parser.add_argument(
        "--openapi-dir", type=Path, default=Path("contracts/openapi")
    )
    parser.add_argument(
        "--feature-dir",
        type=Path,
        default=Path("docs/product/features/catalog"),
    )
    parser.add_argument(
        "--traceability",
        type=Path,
        default=Path("contracts/traceability.json"),
    )
    parser.add_argument(
        "--review-queue",
        type=Path,
        default=Path("contracts/review-queue.md"),
    )
    args = parser.parse_args()

    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    snapshot = resolve_snapshot(
        snapshot,
        load_resolutions(args.resolutions),
    )
    apis = snapshot["apis"]
    features = snapshot["features"]
    feature_by_page = {feature["page_id"]: feature for feature in features}

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for api in apis:
        grouped[api_prefix(api["path"])].append(api)

    args.openapi_dir.mkdir(parents=True, exist_ok=True)
    for prefix, filename in PREFIX_FILES.items():
        document = openapi_document(
            prefix, grouped.get(prefix, []), feature_by_page
        )
        (args.openapi_dir / filename).write_text(
            json.dumps(document, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(
            f"Wrote {filename}: {len(document['paths'])} paths",
            flush=True,
        )

    write_feature_catalogs(features, apis, args.feature_dir)
    rows = traceability(features, apis)
    args.traceability.parent.mkdir(parents=True, exist_ok=True)
    args.traceability.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_review_queue(apis, args.review_queue)
    print(f"Wrote {len(rows)} feature traceability rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
