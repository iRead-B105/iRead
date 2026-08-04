from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "contracts/admin/teacher-screen-fixtures.json"
RESOLUTIONS = ROOT / "contracts/api-resolutions.json"
OPENAPI = ROOT / "contracts/openapi/admin-api.yaml"


class TeacherStoryGazeContractTest(unittest.TestCase):
    def setUp(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.story = fixture["storyHistory"]["response"]["data"]

    def test_story_fixture_contains_authoritative_metrics_events_and_meta(self) -> None:
        self.assertTrue(self.story["wordMetrics"])
        events = self.story["replay"]["events"]
        self.assertTrue(events)

        required_event_fields = {
            "pageNo",
            "eventIndex",
            "eventAtMs",
            "fromTokenIndex",
            "toTokenIndex",
            "movementType",
            "dwellQualified",
            "dwellDurationMs",
            "skippedTokenIndexes",
        }
        for event in events:
            self.assertTrue(required_event_fields.issubset(event))
            self.assertIn(event["movementType"], {"READ", "SKIP", "REGRESSION"})
            self.assertNotIn("x", event)
            self.assertNotIn("y", event)

        meta = self.story["analysisMeta"]
        self.assertEqual("story-gaze-word-v1", meta["calculationVersion"])
        self.assertEqual("BACKEND", meta["calculationSource"])
        self.assertEqual("PAGE_RELATIVE_MAX", meta["heatmapScale"])
        self.assertEqual("PAGE_CHARACTER_AVERAGE", meta["dwellThresholdMethod"])
        self.assertEqual(80, meta["sampleTailMs"])
        self.assertEqual(250, meta["maxSampleGapMs"])
        self.assertEqual("PAGE_FIRST_VALID_SAMPLE", meta["firstSeenReference"])
        self.assertTrue(meta["skipRequiresDwell"])
        self.assertTrue(meta["regressionRequiresDwell"])

    def test_skip_marks_omitted_token_and_preserves_event(self) -> None:
        skipped_metric = next(
            metric for metric in self.story["wordMetrics"] if metric["tokenIndex"] == 1
        )
        skip_event = next(
            event
            for event in self.story["replay"]["events"]
            if event["movementType"] == "SKIP"
        )

        self.assertTrue(skipped_metric["skipped"])
        self.assertEqual([1], skip_event["skippedTokenIndexes"])
        self.assertEqual(2, skip_event["toTokenIndex"])

    def test_resolution_and_generated_openapi_expose_replay_event_contract(self) -> None:
        resolutions = json.loads(RESOLUTIONS.read_text(encoding="utf-8"))
        operation = next(
            item
            for item in resolutions["additional_apis"]
            if item["page_id"] == "git-admin-story-gaze-analysis-v1"
        )
        response = json.loads(operation["response_example"])["data"]
        self.assertIn("events", response["replay"])
        self.assertEqual(250, response["analysisMeta"]["maxSampleGapMs"])

        openapi = json.loads(OPENAPI.read_text(encoding="utf-8"))
        generated = openapi["paths"][operation["path"]]["get"]
        description = generated["description"]
        self.assertIn("replay.events", description)
        self.assertIn("250ms", description)
        self.assertIn("700ms", description)


if __name__ == "__main__":
    unittest.main()
