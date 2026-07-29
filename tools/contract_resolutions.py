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
    if not isinstance(document.get("feature_resolutions", []), list):
        raise ValueError("feature resolutions must be a list")
    if not isinstance(document.get("additional_apis", []), list):
        raise ValueError("additional apis must be a list")
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
        elif action == "deprecate":
            for feature in source_features:
                feature["api_page_ids"] = [
                    page_id
                    for page_id in feature["api_page_ids"]
                    if page_id != source_page_id
                ]
                feature["contract_domain"] = "deprecated"
                feature.pop("contract_responsibility", None)
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
            replacement_feature_ids = resolution.get("replace_feature_ids")
            if replacement_feature_ids is not None:
                if not isinstance(replacement_feature_ids, list):
                    raise ValueError(
                        f"api update feature ids must be a list: {source_key}"
                    )
                unknown_features = [
                    page_id
                    for page_id in replacement_feature_ids
                    if page_id not in feature_by_page
                ]
                if unknown_features:
                    raise ValueError(
                        f"api update has unknown features: {unknown_features}"
                    )
                for feature in source_features:
                    if feature["page_id"] not in replacement_feature_ids:
                        feature["api_page_ids"] = [
                            page_id
                            for page_id in feature["api_page_ids"]
                            if page_id != source_page_id
                        ]
                for feature_page_id in replacement_feature_ids:
                    feature = feature_by_page[feature_page_id]
                    feature["api_page_ids"] = list(
                        dict.fromkeys(
                            feature["api_page_ids"] + [source_page_id]
                        )
                    )
                source["feature_ids"] = list(replacement_feature_ids)
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

    for addition in resolution_document.get("additional_apis", []):
        required = {
            "page_id",
            "url",
            "method",
            "path",
            "domain",
            "feature_ids",
            "request_parameters",
            "response_fields",
            "response_codes",
        }
        missing = required.difference(addition)
        if missing:
            raise ValueError(
                f"additional api is missing fields: {sorted(missing)}"
            )
        addition_copy = copy.deepcopy(addition)
        addition_key = api_key(addition_copy)
        if addition_key in api_by_key:
            raise ValueError(f"additional api collides: {addition_key}")
        if addition_copy["page_id"] in {
            api["page_id"] for api in apis
        }:
            raise ValueError(
                f"additional api page_id collides: {addition_copy['page_id']}"
            )
        unknown_features = [
            page_id
            for page_id in addition_copy["feature_ids"]
            if page_id not in feature_by_page
        ]
        if unknown_features:
            raise ValueError(
                f"additional api has unknown features: {unknown_features}"
            )
        apis.append(addition_copy)
        api_by_key[addition_key] = addition_copy
        for feature_page_id in addition_copy["feature_ids"]:
            feature = feature_by_page[feature_page_id]
            feature["api_page_ids"] = list(
                dict.fromkeys(
                    feature["api_page_ids"] + [addition_copy["page_id"]]
                )
            )

    feature_by_id = {feature["feature_id"]: feature for feature in features}
    active_api_by_page = {api["page_id"]: api for api in apis}
    handled_features: set[str] = set()
    for resolution in resolution_document.get("feature_resolutions", []):
        feature_id = resolution.get("feature_id", "")
        if feature_id in handled_features:
            raise ValueError(f"duplicate feature resolution: {feature_id}")
        handled_features.add(feature_id)
        if feature_id not in feature_by_id:
            raise ValueError(
                f"feature resolution source does not exist: {feature_id}"
            )

        allowed = {
            "feature_id",
            "name",
            "description",
            "responsibility",
            "clear_api_links",
        }
        unsupported = set(resolution).difference(allowed)
        if unsupported:
            raise ValueError(
                f"feature resolution has unsupported fields: {sorted(unsupported)}"
            )

        feature = feature_by_id[feature_id]
        if "name" in resolution:
            feature["name"] = resolution["name"]
        if "description" in resolution:
            feature["description"] = resolution["description"]
        if "responsibility" in resolution:
            responsibility = resolution["responsibility"]
            if responsibility not in {"client", "server", "unmapped"}:
                raise ValueError(
                    f"unsupported feature responsibility: {responsibility}"
                )
            feature["contract_responsibility"] = responsibility
        if resolution.get("clear_api_links"):
            if "contract_domain" not in feature:
                linked_api = next(
                    (
                        active_api_by_page[page_id]
                        for page_id in feature["api_page_ids"]
                        if page_id in active_api_by_page
                    ),
                    None,
                )
                if linked_api is not None:
                    feature["contract_domain"] = linked_api["domain"]
            feature["api_page_ids"] = []

    return resolved
