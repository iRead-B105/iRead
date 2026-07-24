#!/usr/bin/env python3
"""Apply explicitly accepted iRead contract decisions to Notion.

This script only targets known page IDs and never reads database properties.
It may read API page blocks to replace contract text. In particular, it does
not access the priority or implementation-status properties in either Notion
database.
"""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path


NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

STORY_BRANCH_API_PAGE_ID = "3a4027df-9053-8095-b6e0-cc4a2503c036"
STORY_PROGRESS_API_PAGE_ID = "3a7027df-9053-81cb-96f7-cb91b085b400"
STORY_COMPLETE_API_PAGE_ID = "3a7027df-9053-81d0-a374-c4c3a11bd5cf"
STORY_PROGRESS_FEATURE_PAGE_ID = "3a3027df-9053-807d-aa82-cc771d8f741e"
STORY_COMPLETE_FEATURE_PAGE_ID = "3a3027df-9053-80f5-944b-c3e34e688717"
REPORT_TEACHER_MEMO_API_PAGE_ID = "3a6027df-9053-8130-8e99-df15aa032554"
STORY_BRANCH_FEATURE_PAGE_IDS = [
    "3a3027df-9053-80b4-b5f1-f199d3fa45e6",
    "3a3027df-9053-80fe-96ca-c8c0aad5553f",
    "3a3027df-9053-8010-a94c-ffd25255b519",
    "3a3027df-9053-80c2-a65c-ecfd62a16a4c",
    "3a3027df-9053-80e7-9434-e00344bf1154",
    STORY_PROGRESS_FEATURE_PAGE_ID,
    STORY_COMPLETE_FEATURE_PAGE_ID,
]


def notion_request(
    token: str,
    method: str,
    endpoint: str,
    payload: dict[str, object] | None = None,
) -> dict[str, object]:
    request = urllib.request.Request(
        f"{NOTION_API}{endpoint}",
        data=(
            json.dumps(payload).encode("utf-8")
            if payload is not None
            else None
        ),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        if (
            payload == {"archived": True}
            and error.code == 400
            and "archived" in detail
        ):
            return {}
        raise RuntimeError(
            f"Notion {method} {endpoint} failed: {error.code} {detail}"
        ) from error


def patch_page(token: str, page_id: str, payload: dict[str, object]) -> None:
    notion_request(token, "PATCH", f"/pages/{page_id}", payload)


def plain_rich_text(value: str) -> list[dict[str, object]]:
    return [{"type": "text", "text": {"content": value}}]


def replace_contract_block_text(
    token: str,
    parent_block_id: str,
    replacements: dict[str, str],
) -> None:
    cursor: str | None = None
    while True:
        suffix = f"?page_size=100&start_cursor={cursor}" if cursor else "?page_size=100"
        response = notion_request(
            token, "GET", f"/blocks/{parent_block_id}/children{suffix}"
        )
        for block in response.get("results", []):
            block_type = block.get("type")
            block_id = block["id"]
            value = block.get(block_type, {})
            payload: dict[str, object] | None = None
            if block_type == "table_row":
                cells = value.get("cells", [])
                new_texts = []
                changed = False
                for cell in cells:
                    text = "".join(item.get("plain_text", "") for item in cell)
                    replaced = text
                    for old, new in replacements.items():
                        replaced = replaced.replace(old, new)
                    changed = changed or replaced != text
                    new_texts.append(replaced)
                if (
                    len(new_texts) > 1
                    and new_texts[0] == "createdAt"
                    and new_texts[1] == "string"
                ):
                    new_texts[1] = "string(date-time)"
                    changed = True
                if changed:
                    payload = {
                        "table_row": {
                            "cells": [
                                plain_rich_text(text) for text in new_texts
                            ]
                        }
                    }
            elif block_type in {
                "paragraph",
                "heading_1",
                "heading_2",
                "heading_3",
                "bulleted_list_item",
                "numbered_list_item",
                "quote",
                "callout",
                "code",
            }:
                rich_text = value.get("rich_text", [])
                text = "".join(
                    item.get("plain_text", "") for item in rich_text
                )
                replaced = text
                for old, new in replacements.items():
                    replaced = replaced.replace(old, new)
                if replaced != text:
                    updated_value: dict[str, object] = {
                        "rich_text": plain_rich_text(replaced)
                    }
                    if block_type == "code":
                        updated_value["language"] = value.get(
                            "language", "plain text"
                        )
                    payload = {block_type: updated_value}
            if payload:
                notion_request(token, "PATCH", f"/blocks/{block_id}", payload)
            if block.get("has_children"):
                replace_contract_block_text(token, block_id, replacements)
        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--token-file", type=Path, required=True)
    args = parser.parse_args()
    token = args.token_file.read_text(encoding="utf-8").strip()
    if not token:
        raise SystemExit("Notion token file is empty")

    branch_relation = {
        "properties": {
            "API": {
                "relation": [{"id": STORY_BRANCH_API_PAGE_ID}],
            }
        }
    }
    patch_page(token, STORY_PROGRESS_FEATURE_PAGE_ID, branch_relation)
    patch_page(token, STORY_COMPLETE_FEATURE_PAGE_ID, branch_relation)
    patch_page(
        token,
        STORY_BRANCH_API_PAGE_ID,
        {
            "properties": {
                "기능": {
                    "relation": [
                        {"id": page_id} for page_id in STORY_BRANCH_FEATURE_PAGE_IDS
                    ],
                }
            }
        },
    )
    patch_page(token, STORY_PROGRESS_API_PAGE_ID, {"archived": True})
    patch_page(token, STORY_COMPLETE_API_PAGE_ID, {"archived": True})

    patch_page(
        token,
        REPORT_TEACHER_MEMO_API_PAGE_ID,
        {
            "properties": {
                "API 경로": {
                    "title": plain_rich_text(
                        "/api/admin/report/{reportId}/teacher-memo"
                    )
                },
                "요청값": {
                    "rich_text": plain_rich_text(
                        "reportId(path)\nteacherMemo(body)"
                    )
                },
                "응답값": {
                    "rich_text": plain_rich_text(
                        "reportId\nteacherMemo\ncreatedAt"
                    )
                },
                "주석": {"rich_text": []},
            }
        },
    )
    replace_contract_block_text(
        token,
        REPORT_TEACHER_MEMO_API_PAGE_ID,
        {
            "teacher-comments": "teacher-memo",
            "teacherComment": "teacherMemo",
            "updatedAt": "createdAt",
        },
    )
    print("Reconciled story progress and completion contracts in Notion.")


if __name__ == "__main__":
    main()
