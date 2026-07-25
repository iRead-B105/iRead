from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


def api_key(api: dict[str, Any]) -> str:
    return f"{api['method'].upper()} {api['path']}"


def load_resolutions(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("version") != 1:
        raise ValueError("api resolution version must be 1")
    if not isinstance(document.get("resolutions"), list):
        raise ValueError("api resolutions must be a list")
    return document


def resolve_snapshot(
    snapshot: dict[str, Any],
    resolution_document: dict[str, Any],
) -> dict[str, Any]:
    resolved = copy.deepcopy(snapshot)
    apis = resolved["apis"]
    features = resolved["features"]
    api_by_key = {api_key(api): api for api in apis}
    feature_by_page = {feature["page_id"]: feature for feature in features}
    handled_sources: set[str] = set()

    for resolution in resolution_document["resolutions"]:
        source_key = resolution.get("source", "")
        action = resolution.get("action", "")
        if source_key in handled_sources:
            raise ValueError(f"duplicate api resolution: {source_key}")
        handled_sources.add(source_key)
        if source_key not in api_by_key:
            raise ValueError(f"api resolution source does not exist: {source_key}")

        source = api_by_key[source_key]
        source_page_id = source["page_id"]
        source_features = [
            feature_by_page[page_id]
            for page_id in source["feature_ids"]
            if page_id in feature_by_page
        ]

        if action == "client":
            for feature in source_features:
                feature["api_page_ids"] = [
                    page_id
                    for page_id in feature["api_page_ids"]
                    if page_id != source_page_id
                ]
                feature["contract_domain"] = source["domain"]
                feature["contract_responsibility"] = "client"
        elif action == "merge":
            target_key = resolution.get("target", "")
            if target_key not in api_by_key:
                raise ValueError(
                    f"api resolution target does not exist: {target_key}"
                )
            target = api_by_key[target_key]
            target_page_id = target["page_id"]
            target["feature_ids"] = list(
                dict.fromkeys(target["feature_ids"] + source["feature_ids"])
            )
            for feature in source_features:
                feature["api_page_ids"] = list(
                    dict.fromkeys(
                        [
                            target_page_id if page_id == source_page_id else page_id
                            for page_id in feature["api_page_ids"]
                        ]
                    )
                )
        elif action == "update":
            changes = resolution.get("changes")
            if not isinstance(changes, dict) or not changes:
                raise ValueError(
                    f"api update has no changes: {source_key}"
                )
            forbidden = {"page_id", "feature_ids", "url"}
            present = forbidden.intersection(changes)
            if present:
                raise ValueError(
                    f"api update changes immutable fields: {sorted(present)}"
                )
            source.update(copy.deepcopy(changes))
            updated_key = api_key(source)
            if updated_key != source_key:
                if updated_key in api_by_key:
                    raise ValueError(
                        f"api update collides with existing operation: {updated_key}"
                    )
                del api_by_key[source_key]
                api_by_key[updated_key] = source
            continue
        else:
            raise ValueError(
                f"unsupported api resolution action for {source_key}: {action}"
            )

        apis.remove(source)
        del api_by_key[source_key]

    return resolved
