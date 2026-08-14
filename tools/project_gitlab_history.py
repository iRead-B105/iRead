#!/usr/bin/env python3

from __future__ import annotations

import argparse
import heapq
import io
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path


STATE_NOTES_REF = "iread-source-state"
MAP_NOTES_REF = "iread-source-map"
SERVICE_ORDER = ("backend", "frontend", "ai", "app", "eyetracking")
AUTHOR_EMAIL_ALIASES = {
    "156529176+2hnk@users.noreply.github.com": "kimgh921@gmail.com",
}


@dataclass(frozen=True)
class Source:
    name: str
    target: str
    path: str | None
    previous: str | None


@dataclass(frozen=True)
class CommitMetadata:
    author_name: str
    author_email: str
    author_date: str
    committer_name: str
    committer_email: str
    committer_date: str
    message: str


def run(
    repo: Path,
    *args: str,
    check: bool = True,
    env: dict[str, str] | None = None,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        env=env,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def output(repo: Path, *args: str) -> str:
    return run(repo, *args).stdout.strip()


def notes_show(repo: Path, ref: str, target: str) -> str | None:
    result = run(repo, "notes", f"--ref={ref}", "show", target, check=False)
    if result.returncode == 0:
        return result.stdout
    if "no note found" in result.stderr.lower():
        return None
    raise RuntimeError(result.stderr.strip())


def read_state(repo: Path) -> dict[str, object] | None:
    raw = notes_show(repo, STATE_NOTES_REF, "HEAD")
    if raw is None:
        return None
    state = json.loads(raw)
    if state.get("schemaVersion") != 2:
        raise RuntimeError("Unsupported projection state schema")
    return state


def assert_fast_forward(
    repo: Path,
    name: str,
    previous: str,
    target: str,
) -> None:
    result = run(
        repo,
        "merge-base",
        "--is-ancestor",
        previous,
        target,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"{name} moved non-fast-forward: {previous} -> {target}"
        )


def commit_range(repo: Path, source: Source) -> list[str]:
    if source.previous == source.target:
        return []
    if source.previous is not None:
        assert_fast_forward(repo, source.name, source.previous, source.target)
        revision = f"{source.previous}..{source.target}"
    else:
        revision = source.target
    raw = output(repo, "rev-list", "--reverse", "--topo-order", revision)
    return raw.splitlines() if raw else []


def committer_timestamp(repo: Path, commit: str) -> int:
    return int(output(repo, "show", "-s", "--format=%ct", commit))


def ordered_commits(
    repo: Path,
    sources: list[Source],
) -> list[tuple[Source, str]]:
    queues = {source.name: commit_range(repo, source) for source in sources}
    by_name = {source.name: source for source in sources}
    positions = {source.name: 0 for source in sources}
    heap: list[tuple[int, str, str]] = []

    for source in sources:
        commits = queues[source.name]
        if commits:
            commit = commits[0]
            heapq.heappush(
                heap,
                (committer_timestamp(repo, commit), source.name, commit),
            )

    result: list[tuple[Source, str]] = []
    while heap:
        _, name, commit = heapq.heappop(heap)
        source = by_name[name]
        result.append((source, commit))
        positions[name] += 1
        commits = queues[name]
        if positions[name] < len(commits):
            next_commit = commits[positions[name]]
            heapq.heappush(
                heap,
                (
                    committer_timestamp(repo, next_commit),
                    name,
                    next_commit,
                ),
            )
    return result


def clear_directory(path: Path) -> None:
    if not path.exists():
        return
    for child in path.iterdir():
        if child.name == ".git":
            continue
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()


def extract_archive(repo: Path, commit: str, destination: Path) -> None:
    archive = subprocess.run(
        ["git", "-C", str(repo), "archive", commit],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        tar.extractall(destination, filter="data")


def replace_service_snapshot(
    repo: Path,
    commit: str,
    relative_path: str,
) -> None:
    destination = repo / relative_path
    if destination.exists():
        shutil.rmtree(destination)
    extract_archive(repo, commit, destination)


def replace_orchestration_snapshot(repo: Path, commit: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        snapshot = Path(temp_dir)
        extract_archive(repo, commit, snapshot)

        for child in repo.iterdir():
            if child.name in {".git", "services"}:
                continue
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child)
            else:
                child.unlink()

        for child in snapshot.iterdir():
            if child.name in {
                ".gitmodules",
                ".gitlab-source-revisions.json",
                "services",
            }:
                continue
            destination = repo / child.name
            if child.is_dir() and not child.is_symlink():
                shutil.copytree(child, destination, symlinks=True)
            elif child.is_symlink():
                destination.symlink_to(os.readlink(child))
            else:
                shutil.copy2(child, destination)


def metadata(repo: Path, commit: str) -> CommitMetadata:
    raw = run(
        repo,
        "show",
        "-s",
        "--format=%an%x00%ae%x00%aI%x00%cn%x00%ce%x00%cI%x00%B",
        commit,
    ).stdout
    parts = raw.split("\0", 6)
    if len(parts) != 7:
        raise RuntimeError(f"Unable to read commit metadata: {commit}")
    return CommitMetadata(*parts)


def projected_author_email(source_email: str) -> str:
    return AUTHOR_EMAIL_ALIASES.get(source_email.casefold(), source_email)


def commit_projection(
    repo: Path,
    source: Source,
    source_commit: str,
) -> str | None:
    if source.path is None:
        replace_orchestration_snapshot(repo, source_commit)
    else:
        replace_service_snapshot(repo, source_commit, source.path)

    run(repo, "add", "--all")

    source_metadata = metadata(repo, source_commit)
    commit_env = os.environ.copy()
    commit_env.update(
        {
            "GIT_AUTHOR_NAME": source_metadata.author_name,
            "GIT_AUTHOR_EMAIL": projected_author_email(
                source_metadata.author_email
            ),
            "GIT_AUTHOR_DATE": source_metadata.author_date,
            "GIT_COMMITTER_NAME": source_metadata.committer_name,
            "GIT_COMMITTER_EMAIL": source_metadata.committer_email,
            "GIT_COMMITTER_DATE": source_metadata.committer_date,
        }
    )
    run(
        repo,
        "commit",
        "--allow-empty",
        "--no-gpg-sign",
        "--cleanup=verbatim",
        "--file=-",
        env=commit_env,
        input_text=source_metadata.message,
    )
    projected_commit = output(repo, "rev-parse", "HEAD")
    mapping = json.dumps(
        {
            "schemaVersion": 1,
            "sourceRepository": source.name,
            "sourceCommit": source_commit,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    run(
        repo,
        "notes",
        f"--ref={MAP_NOTES_REF}",
        "add",
        "--force",
        "--message",
        mapping,
        projected_commit,
    )
    print(
        f"Projected {source.name} {source_commit} -> {projected_commit}",
        flush=True,
    )
    return projected_commit


def prepare_rebuild(repo: Path) -> None:
    run(repo, "checkout", "--orphan", "projection-main")
    run(repo, "rm", "-r", "--force", "--ignore-unmatch", ".", check=False)
    clear_directory(repo)


def state_for(sources: list[Source]) -> dict[str, object]:
    return {
        "schemaVersion": 2,
        "orchestration": next(
            source.target
            for source in sources
            if source.name == "orchestration"
        ),
        "services": {
            source.name: source.target
            for source in sources
            if source.name != "orchestration"
        },
    }


def write_state(repo: Path, sources: list[Source]) -> None:
    state = json.dumps(
        state_for(sources),
        ensure_ascii=False,
        sort_keys=True,
    )
    current_state = notes_show(repo, STATE_NOTES_REF, "HEAD")
    if current_state is not None and current_state.strip() == state:
        return
    run(
        repo,
        "notes",
        f"--ref={STATE_NOTES_REF}",
        "add",
        "--force",
        "--message",
        state,
        "HEAD",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--orchestration", required=True)
    for service in SERVICE_ORDER:
        parser.add_argument(f"--{service}", required=True)
    parser.add_argument("--rebuild", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    previous_state = read_state(repo)

    if previous_state is None and not args.rebuild:
        print(
            "Projection state is absent; run workflow_dispatch with "
            "rebuild_history=true.",
            flush=True,
        )
        return 3

    if args.rebuild:
        previous_state = None
        prepare_rebuild(repo)

    previous_services = (
        previous_state.get("services", {}) if previous_state else {}
    )
    sources = [
        Source(
            name="orchestration",
            target=args.orchestration,
            path=None,
            previous=(
                str(previous_state["orchestration"])
                if previous_state
                else None
            ),
        ),
        *[
            Source(
                name=service,
                target=getattr(args, service),
                path=f"services/{service}",
                previous=(
                    str(previous_services[service])
                    if service in previous_services
                    else None
                ),
            )
            for service in SERVICE_ORDER
        ],
    ]

    commits = ordered_commits(repo, sources)
    for source, commit in commits:
        commit_projection(repo, source, commit)

    if not output(repo, "rev-parse", "--verify", "HEAD"):
        raise RuntimeError("Projection produced no commits")

    write_state(repo, sources)
    print(
        f"Projection ready at {output(repo, 'rev-parse', 'HEAD')}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
