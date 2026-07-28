from __future__ import annotations

import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from validate_contracts import validate_schema
from generate_erd import render_erd
from contract_resolutions import resolve_snapshot


class ValidateSchemaTest(unittest.TestCase):
    def test_single_v1_schema_contract_is_valid(self) -> None:
        errors, counts = validate_schema()

        self.assertEqual([], errors)
        self.assertEqual(25, counts["tables"])
        self.assertEqual(25, counts["primary_keys"])
        self.assertEqual(34, counts["foreign_keys"])
        self.assertEqual(11, counts["unique_constraints"])

    def test_named_primary_key_constraint_is_rendered(self) -> None:
        sql = """
CREATE TABLE `samples` (
    `id` bigint NOT NULL,
    CONSTRAINT `PK_SAMPLES` PRIMARY KEY (`id`)
);
"""

        rendered = render_erd(sql)

        self.assertIn('BIGINT id PK "required"', rendered)

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


if __name__ == "__main__":
    unittest.main()
