from __future__ import annotations

import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from validate_contracts import validate_schema
from generate_erd import render_erd
from generate_contracts import schema_for_type
from contract_resolutions import resolve_snapshot


class ValidateSchemaTest(unittest.TestCase):
    def test_single_v1_schema_contract_is_valid(self) -> None:
        errors, counts = validate_schema()

        self.assertEqual([], errors)
        self.assertEqual(26, counts["tables"])
        self.assertEqual(26, counts["primary_keys"])
        self.assertEqual(35, counts["foreign_keys"])
        self.assertEqual(15, counts["unique_constraints"])

    def test_named_primary_key_constraint_is_rendered(self) -> None:
        sql = """
CREATE TABLE `samples` (
    `id` bigint NOT NULL,
    CONSTRAINT `PK_SAMPLES` PRIMARY KEY (`id`)
);
"""

        rendered = render_erd(sql)

        self.assertIn('BIGINT id PK "required"', rendered)

    def test_openapi_enum_preserves_contract_casing(self) -> None:
        self.assertEqual(
            {"type": "string", "enum": ["MALE", "FEMALE"]},
            schema_for_type("string(MALE|FEMALE)"),
        )

    def test_feature_resolution_can_move_feature_to_client(self) -> None:
        snapshot = {
            "apis": [
                {
                    "method": "GET",
                    "path": "/api/app/student/{studentId}/growth",
                    "page_id": "api-page",
                    "feature_ids": ["feature-page"],
                    "domain": "student",
                }
            ],
            "features": [
                {
                    "feature_id": "GR-STAT-03",
                    "page_id": "feature-page",
                    "name": "기존 이름",
                    "description": "기존 설명",
                    "api_page_ids": ["api-page"],
                }
            ],
        }
        resolutions = {
            "version": 1,
            "resolutions": [],
            "feature_resolutions": [
                {
                    "feature_id": "GR-STAT-03",
                    "name": "꽃 성장 콘텐츠 표시",
                    "description": "완료 횟수로 꽃 성장 단계를 계산한다.",
                    "responsibility": "client",
                    "clear_api_links": True,
                }
            ],
        }

        resolved = resolve_snapshot(snapshot, resolutions)
        feature = resolved["features"][0]

        self.assertEqual("꽃 성장 콘텐츠 표시", feature["name"])
        self.assertEqual("client", feature["contract_responsibility"])
        self.assertEqual("student", feature["contract_domain"])
        self.assertEqual([], feature["api_page_ids"])

    def test_api_can_be_deprecated_and_replaced_by_addition(self) -> None:
        snapshot = {
            "apis": [
                {
                    "method": "POST",
                    "path": "/api/auth/admin/find-id",
                    "page_id": "find-api",
                    "url": "https://example.com/find",
                    "feature_ids": ["find-feature-page"],
                    "domain": "auth",
                }
            ],
            "features": [
                {
                    "feature_id": "LG-ID-01",
                    "page_id": "find-feature-page",
                    "name": "아이디 찾기",
                    "description": "기존 기능",
                    "api_page_ids": ["find-api"],
                },
                {
                    "feature_id": "LG-PW-02",
                    "page_id": "reset-feature-page",
                    "name": "재설정 요청",
                    "description": "재설정 링크 요청",
                    "api_page_ids": [],
                },
            ],
        }
        resolutions = {
            "version": 1,
            "resolutions": [
                {
                    "source": "POST /api/auth/admin/find-id",
                    "action": "deprecate",
                }
            ],
            "additional_apis": [
                {
                    "page_id": "reset-api",
                    "url": "https://example.com/reset",
                    "method": "POST",
                    "path": "/api/auth/admin/password-reset/request",
                    "domain": "auth",
                    "feature_ids": ["reset-feature-page"],
                    "request_parameters": [],
                    "response_fields": [],
                    "response_codes": ["202"],
                }
            ],
            "feature_resolutions": [],
        }

        resolved = resolve_snapshot(snapshot, resolutions)

        self.assertEqual(
            ["/api/auth/admin/password-reset/request"],
            [api["path"] for api in resolved["apis"]],
        )
        deprecated = resolved["features"][0]
        self.assertEqual("deprecated", deprecated["contract_domain"])
        self.assertEqual([], deprecated["api_page_ids"])
        self.assertEqual(
            ["reset-api"],
            resolved["features"][1]["api_page_ids"],
        )


if __name__ == "__main__":
    unittest.main()
