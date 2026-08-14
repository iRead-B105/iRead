from __future__ import annotations

import argparse
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


API_DATABASE_ID = "573027df905382f39586815f878bef18"
FEATURE_DATABASE_ID = "de0027df905383e98fb00120c64321fc"
NOTION_VERSION = "2022-06-28"
NOTION_API = "https://api.notion.com/v1"

_request_lock = threading.Lock()
_last_request_at = 0.0


def plain_text(items: list[dict[str, Any]] | None) -> str:
    return "".join(item.get("plain_text", "") for item in items or [])


def property_text(prop: dict[str, Any] | None) -> str:
    if not prop:
        return ""
    kind = prop.get("type")
    if kind == "title":
        return plain_text(prop.get("title"))
    if kind == "rich_text":
        return plain_text(prop.get("rich_text"))
    if kind == "select":
        return (prop.get("select") or {}).get("name", "")
    if kind == "status":
        return (prop.get("status") or {}).get("name", "")
    if kind == "url":
        return prop.get("url") or ""
    return ""


class NotionClient:
    def __init__(self, token: str) -> None:
        self.token = token

    def request(
        self, method: str, endpoint: str, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        global _last_request_at
        body = None
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        for attempt in range(8):
            with _request_lock:
                delay = 0.34 - (time.monotonic() - _last_request_at)
                if delay > 0:
                    time.sleep(delay)
                _last_request_at = time.monotonic()

            request = urllib.request.Request(
                f"{NOTION_API}{endpoint}",
                data=body,
                method=method,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Notion-Version": NOTION_VERSION,
                    "Content-Type": "application/json; charset=utf-8",
                },
            )
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as error:
                if error.code != 429 or attempt == 7:
                    detail = error.read().decode("utf-8", errors="replace")
                    raise RuntimeError(
                        f"Notion API {method} {endpoint} failed: {error.code} {detail}"
                    ) from error
                retry_after = float(error.headers.get("Retry-After", "1"))
                time.sleep(max(retry_after, 1.0))
        raise RuntimeError("Notion API retry limit exceeded")

    def query_database(self, database_id: str) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            payload: dict[str, Any] = {"page_size": 100}
            if cursor:
                payload["start_cursor"] = cursor
            response = self.request(
                "POST", f"/databases/{database_id}/query", payload
            )
            results.extend(response.get("results", []))
            if not response.get("has_more"):
                return results
            cursor = response.get("next_cursor")

    def block_children(self, block_id: str) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            endpoint = f"/blocks/{block_id}/children?page_size=100"
            if cursor:
                endpoint += f"&start_cursor={urllib.parse.quote(cursor)}"
            response = self.request("GET", endpoint)
            results.extend(response.get("results", []))
            if not response.get("has_more"):
                return results
            cursor = response.get("next_cursor")

    def flattened_blocks(self, page_id: str) -> list[dict[str, Any]]:
        flattened: list[dict[str, Any]] = []

        def walk(block_id: str) -> None:
            for block in self.block_children(block_id):
                block_type = block.get("type", "")
                content = block.get(block_type, {})
                item: dict[str, Any] = {
                    "id": block.get("id"),
                    "type": block_type,
                    "text": "",
                }
                if block_type == "table_row":
                    item["cells"] = [
                        plain_text(cell) for cell in content.get("cells", [])
                    ]
                    item["text"] = " | ".join(item["cells"])
                else:
                    item["text"] = plain_text(content.get("rich_text"))
                flattened.append(item)
                if block.get("has_children"):
                    walk(block["id"])

        walk(page_id)
        return flattened


def parse_api_blocks(blocks: list[dict[str, Any]]) -> dict[str, Any]:
    section = ""
    response_status = ""
    request_parameters: list[dict[str, Any]] = []
    response_fields: list[dict[str, Any]] = []
    response_codes: list[str] = []
    request_example = ""
    response_example = ""

    for block in blocks:
        block_type = block.get("type")
        text = block.get("text", "").strip()
        if block_type == "heading_3":
            lowered = text.lower()
            if lowered == "request":
                section = "request"
            elif lowered == "response":
                section = "response"
            continue

        if block_type == "heading_4" and section == "response":
            code = text[:3] if len(text) >= 3 and text[:3].isdigit() else ""
            if code:
                response_status = code
                if code not in response_codes:
                    response_codes.append(code)
            continue

        if block_type == "table_row":
            cells = block.get("cells", [])
            if section == "request" and len(cells) >= 5:
                if cells[0].strip().lower() not in {"파라미터", "parameter"}:
                    request_parameters.append(
                        {
                            "name": cells[0].strip(),
                            "type": cells[1].strip(),
                            "in": cells[2].strip(),
                            "required": cells[3].strip().upper() == "Y",
                            "description": cells[4].strip(),
                        }
                    )
            elif section == "response" and len(cells) >= 3:
                if cells[0].strip().lower() not in {"필드", "field"}:
                    if not response_status or response_status.startswith("2"):
                        response_fields.append(
                            {
                                "name": cells[0].strip(),
                                "type": cells[1].strip(),
                                "description": cells[2].strip(),
                            }
                        )
            continue

        if block_type == "code":
            if section == "request" and not request_example:
                request_example = text
            elif (
                section == "response"
                and (not response_status or response_status.startswith("2"))
                and not response_example
            ):
                response_example = text

    return {
        "request_parameters": request_parameters,
        "response_fields": response_fields,
        "response_codes": response_codes,
        "request_example": request_example,
        "response_example": response_example,
    }


def api_record(client: NotionClient, page: dict[str, Any]) -> dict[str, Any]:
    properties = page.get("properties", {})
    blocks = client.flattened_blocks(page["id"])
    parsed = parse_api_blocks(blocks)
    return {
        "page_id": page["id"],
        "url": page.get("url", ""),
        "method": property_text(properties.get("메서드")).upper(),
        "path": property_text(properties.get("API 경로")),
        "domain": property_text(properties.get("도메인")),
        "request_summary": property_text(properties.get("요청값")),
        "response_summary": property_text(properties.get("응답값")),
        "note": property_text(properties.get("주석")),
        "feature_ids": [
            relation["id"]
            for relation in properties.get("기능", {}).get("relation", [])
        ],
        **parsed,
    }


def feature_record(page: dict[str, Any]) -> dict[str, Any]:
    properties = page.get("properties", {})
    return {
        "page_id": page["id"],
        "url": page.get("url", ""),
        "feature_id": property_text(properties.get("No")),
        "name": property_text(properties.get("기능")),
        "description": property_text(properties.get("기능 설명")),
        "api_page_ids": [
            relation["id"]
            for relation in properties.get("API", {}).get("relation", [])
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--token-file", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("contracts/notion/spec-snapshot.json"),
    )
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()

    token = args.token_file.read_text(encoding="utf-8").strip()
    if not token:
        raise RuntimeError("Notion token file is empty")

    client = NotionClient(token)
    api_pages = client.query_database(API_DATABASE_ID)
    feature_pages = client.query_database(FEATURE_DATABASE_ID)

    api_records: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(api_record, client, page): page["id"]
            for page in api_pages
        }
        for index, future in enumerate(as_completed(futures), start=1):
            api_records.append(future.result())
            if index % 10 == 0 or index == len(futures):
                print(f"Fetched API pages: {index}/{len(futures)}", flush=True)

    api_records.sort(key=lambda item: (item["path"], item["method"]))
    feature_records = sorted(
        (feature_record(page) for page in feature_pages),
        key=lambda item: (item["feature_id"], item["name"]),
    )

    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "notion_version": NOTION_VERSION,
        "sources": {
            "api_database_id": API_DATABASE_ID,
            "feature_database_id": FEATURE_DATABASE_ID,
        },
        "apis": api_records,
        "features": feature_records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {len(api_records)} APIs and {len(feature_records)} features "
        f"to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
