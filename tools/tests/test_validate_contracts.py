from __future__ import annotations

import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from validate_contracts import validate_schema


class ValidateSchemaTest(unittest.TestCase):
    def test_cumulative_flyway_schema_contract_is_valid(self) -> None:
        errors, counts = validate_schema()

        self.assertEqual([], errors)
        self.assertEqual(26, counts["tables"])
        self.assertEqual(26, counts["primary_keys"])
        self.assertEqual(27, counts["foreign_keys"])


if __name__ == "__main__":
    unittest.main()
