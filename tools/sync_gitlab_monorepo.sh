#!/usr/bin/env bash

set -euo pipefail

readonly GITLAB_REPOSITORY_URL="${GITLAB_REPOSITORY_URL:-https://lab.ssafy.com/s15-webmobile2-sub1/S15P11B105.git}"
readonly GITLAB_USERNAME="${GITLAB_USERNAME:-oauth2}"
readonly ORCHESTRATION_URL="https://github.com/iRead-B105/iRead.git"
readonly BACKEND_URL="https://github.com/iRead-B105/iRead-backend.git"
readonly FRONTEND_URL="https://github.com/iRead-B105/iRead-frontend.git"
readonly AI_URL="https://github.com/iRead-B105/iRead-ai.git"

if [[ -z "${GITLAB_PUSH_TOKEN:-}" ]]; then
  echo "GITLAB_PUSH_TOKEN is required" >&2
  exit 1
fi

readonly AUTH_HEADER="AUTHORIZATION: Basic $(printf '%s:%s' "$GITLAB_USERNAME" "$GITLAB_PUSH_TOKEN" | base64 | tr -d '\n')"
readonly WORK_DIR="$(mktemp -d)"
readonly AGGREGATE_DIR="$WORK_DIR/aggregate"
readonly SNAPSHOT_DIR="$WORK_DIR/orchestration-snapshot"

cleanup() {
  rm -rf -- "$WORK_DIR"
}
trap cleanup EXIT

git_auth() {
  git -c "http.extraheader=$AUTH_HEADER" "$@"
}

ensure_remote() {
  local name="$1"
  local url="$2"

  if git -C "$AGGREGATE_DIR" remote get-url "$name" >/dev/null 2>&1; then
    git -C "$AGGREGATE_DIR" remote set-url "$name" "$url"
  else
    git -C "$AGGREGATE_DIR" remote add "$name" "$url"
  fi
}

fetch_source() {
  local name="$1"
  local url="$2"

  ensure_remote "$name" "$url"
  git -C "$AGGREGATE_DIR" fetch --force --no-tags "$name" \
    "+refs/heads/*:refs/remotes/source/$name/heads/*" \
    "+refs/tags/*:refs/tags/upstream/$name/*"
}

push_source_refs() {
  local name="$1"

  git_auth -C "$AGGREGATE_DIR" push origin \
    "refs/remotes/source/$name/heads/*:refs/heads/upstream/$name/*"

  if git -C "$AGGREGATE_DIR" for-each-ref --format='%(refname)' "refs/tags/upstream/$name/" | grep -q .; then
    git_auth -C "$AGGREGATE_DIR" push origin \
      "refs/tags/upstream/$name/*:refs/tags/upstream/$name/*"
  fi
}

manifest_value() {
  local key="$1"

  python3 - "$AGGREGATE_DIR/.gitlab-source-revisions.json" "$key" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
key = sys.argv[2].split(".")
data = json.loads(path.read_text(encoding="utf-8"))
for part in key:
    data = data[part]
print(data)
PY
}

write_manifest() {
  local orchestration_sha="$1"
  local backend_sha="$2"
  local frontend_sha="$3"
  local ai_sha="$4"

  python3 - "$AGGREGATE_DIR/.gitlab-source-revisions.json" \
    "$orchestration_sha" "$backend_sha" "$frontend_sha" "$ai_sha" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
data = {
    "orchestration": {
        "repository": "https://github.com/iRead-B105/iRead.git",
        "ref": "develop",
        "commit": sys.argv[2],
    },
    "services": {
        "backend": {
            "repository": "https://github.com/iRead-B105/iRead-backend.git",
            "path": "services/backend",
            "commit": sys.argv[3],
        },
        "frontend": {
            "repository": "https://github.com/iRead-B105/iRead-frontend.git",
            "path": "services/frontend",
            "commit": sys.argv[4],
        },
        "ai": {
            "repository": "https://github.com/iRead-B105/iRead-ai.git",
            "path": "services/ai",
            "commit": sys.argv[5],
        },
    },
}
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
}

gitlink_sha() {
  local treeish="$1"
  local path="$2"
  local entry

  entry="$(git -C "$AGGREGATE_DIR" ls-tree "$treeish" -- "$path")"
  if [[ "$entry" != 160000\ commit\ * ]]; then
    echo "Expected submodule gitlink at $path" >&2
    exit 1
  fi
  awk '{print $3}' <<<"$entry"
}

merge_subtree() {
  local name="$1"
  local path="$2"
  local previous_sha="$3"
  local next_sha="$4"

  if [[ "$previous_sha" == "$next_sha" ]]; then
    return
  fi
  if ! git -C "$AGGREGATE_DIR" merge-base --is-ancestor "$previous_sha" "$next_sha"; then
    echo "$name moved to a non-fast-forward commit: $previous_sha -> $next_sha" >&2
    exit 1
  fi

  git -C "$AGGREGATE_DIR" subtree merge \
    --prefix="$path" \
    "$next_sha" \
    -m "chore(mirror): $name $next_sha 반영"
}

git_auth clone --branch main --single-branch "$GITLAB_REPOSITORY_URL" "$AGGREGATE_DIR"
git -C "$AGGREGATE_DIR" remote set-url origin "$GITLAB_REPOSITORY_URL"
git -C "$AGGREGATE_DIR" config user.name "iRead GitLab Mirror"
git -C "$AGGREGATE_DIR" config user.email "iread-gitlab-mirror@users.noreply.github.com"

fetch_source orchestration "$ORCHESTRATION_URL"
fetch_source backend "$BACKEND_URL"
fetch_source frontend "$FRONTEND_URL"
fetch_source ai "$AI_URL"

for source in orchestration backend frontend ai; do
  push_source_refs "$source"
done

readonly ORCHESTRATION_SHA="$(git -C "$AGGREGATE_DIR" rev-parse refs/remotes/source/orchestration/heads/develop)"
readonly BACKEND_SHA="$(gitlink_sha "$ORCHESTRATION_SHA" services/backend)"
readonly FRONTEND_SHA="$(gitlink_sha "$ORCHESTRATION_SHA" services/frontend)"
readonly AI_SHA="$(gitlink_sha "$ORCHESTRATION_SHA" services/ai)"

readonly PREVIOUS_ORCHESTRATION_SHA="$(manifest_value orchestration.commit)"
readonly PREVIOUS_BACKEND_SHA="$(manifest_value services.backend.commit)"
readonly PREVIOUS_FRONTEND_SHA="$(manifest_value services.frontend.commit)"
readonly PREVIOUS_AI_SHA="$(manifest_value services.ai.commit)"

if [[ "$PREVIOUS_ORCHESTRATION_SHA" != "$ORCHESTRATION_SHA" ]]; then
  if ! git -C "$AGGREGATE_DIR" merge-base --is-ancestor "$PREVIOUS_ORCHESTRATION_SHA" "$ORCHESTRATION_SHA"; then
    echo "orchestration/develop was not fast-forwarded" >&2
    exit 1
  fi
  git -C "$AGGREGATE_DIR" merge --strategy=ours --no-ff \
    "$ORCHESTRATION_SHA" \
    -m "chore(mirror): orchestration $ORCHESTRATION_SHA 이력 연결"
fi

merge_subtree backend services/backend "$PREVIOUS_BACKEND_SHA" "$BACKEND_SHA"
merge_subtree frontend services/frontend "$PREVIOUS_FRONTEND_SHA" "$FRONTEND_SHA"
merge_subtree ai services/ai "$PREVIOUS_AI_SHA" "$AI_SHA"

mkdir -p "$SNAPSHOT_DIR"
git -C "$AGGREGATE_DIR" archive "$ORCHESTRATION_SHA" | tar -x -C "$SNAPSHOT_DIR"
rsync -a --delete \
  --exclude='/.git/' \
  --exclude='/.gitmodules' \
  --exclude='/.gitlab-source-revisions.json' \
  --exclude='/services/backend/' \
  --exclude='/services/frontend/' \
  --exclude='/services/ai/' \
  "$SNAPSHOT_DIR/" "$AGGREGATE_DIR/"

write_manifest "$ORCHESTRATION_SHA" "$BACKEND_SHA" "$FRONTEND_SHA" "$AI_SHA"
git -C "$AGGREGATE_DIR" add --all

if ! git -C "$AGGREGATE_DIR" diff --cached --quiet; then
  git -C "$AGGREGATE_DIR" commit \
    -m "chore(mirror): orchestration 통합 상태 $ORCHESTRATION_SHA 반영"
fi

git_auth -C "$AGGREGATE_DIR" push origin main:main
