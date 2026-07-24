#!/usr/bin/env bash

set -euo pipefail

readonly GITLAB_REPOSITORY_URL="${GITLAB_REPOSITORY_URL:-https://lab.ssafy.com/s15-webmobile2-sub1/S15P11B105.git}"
readonly GITLAB_USERNAME="${GITLAB_USERNAME:-oauth2}"
readonly ORCHESTRATION_URL="https://github.com/iRead-B105/iRead.git"
readonly ORCHESTRATION_BRANCH="develop"
readonly REQUESTED_ORCHESTRATION_SHA="${SYNC_ORCHESTRATION_SHA:-}"
readonly TARGET_BRANCH="main"
readonly WORK_DIR="$(mktemp -d)"
readonly AGGREGATE_DIR="$WORK_DIR/aggregate"
readonly SNAPSHOT_DIR="$WORK_DIR/orchestration-snapshot"
readonly MANIFEST=".gitlab-source-revisions.json"

declare -ar SERVICE_NAMES=(backend frontend ai app eyetracking)
declare -Ar SERVICE_URLS=(
  [backend]="https://github.com/iRead-B105/iRead-backend.git"
  [frontend]="https://github.com/iRead-B105/iRead-frontend.git"
  [ai]="https://github.com/iRead-B105/iRead-ai.git"
  [app]="https://github.com/iRead-B105/iRead-app.git"
  [eyetracking]="https://github.com/iRead-B105/iRead-eyetracking.git"
)
declare -Ar SERVICE_PATHS=(
  [backend]="services/backend"
  [frontend]="services/frontend"
  [ai]="services/ai"
  [app]="services/app"
  [eyetracking]="services/eyetracking"
)

if [[ -z "${GITLAB_PUSH_TOKEN:-}" ]]; then
  echo "GITLAB_PUSH_TOKEN is required" >&2
  exit 1
fi

readonly AUTH_HEADER="AUTHORIZATION: Basic $(printf '%s:%s' "$GITLAB_USERNAME" "$GITLAB_PUSH_TOKEN" | base64 | tr -d '\n')"

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

  if git -C "$AGGREGATE_DIR" for-each-ref \
    --format='%(refname)' "refs/tags/upstream/$name/" | grep -q .; then
    git_auth -C "$AGGREGATE_DIR" push origin \
      "refs/tags/upstream/$name/*:refs/tags/upstream/$name/*"
  fi
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

manifest_value() {
  local key="$1"

  python3 - "$AGGREGATE_DIR/$MANIFEST" "$key" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
parts = sys.argv[2].split(".")
data = json.loads(path.read_text(encoding="utf-8"))
for part in parts:
    data = data[part]
print(data)
PY
}

write_manifest() {
  local orchestration_sha="$1"
  local backend_sha="$2"
  local frontend_sha="$3"
  local ai_sha="$4"
  local app_sha="$5"
  local eyetracking_sha="$6"

  python3 - "$AGGREGATE_DIR/$MANIFEST" \
    "$orchestration_sha" \
    "$backend_sha" \
    "$frontend_sha" \
    "$ai_sha" \
    "$app_sha" \
    "$eyetracking_sha" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
names = ("backend", "frontend", "ai", "app", "eyetracking")
commits = sys.argv[3:8]
data = {
    "schemaVersion": 1,
    "orchestration": {
        "repository": "https://github.com/iRead-B105/iRead.git",
        "ref": "develop",
        "commit": sys.argv[2],
    },
    "services": {
        name: {
            "repository": f"https://github.com/iRead-B105/iRead-{name}.git",
            "path": f"services/{name}",
            "commit": commit,
        }
        for name, commit in zip(names, commits, strict=True)
    },
}
path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY
}

commit_if_needed() {
  local message="$1"

  git -C "$AGGREGATE_DIR" add --all
  if ! git -C "$AGGREGATE_DIR" diff --cached --quiet; then
    git -C "$AGGREGATE_DIR" commit -m "$message"
  fi
}

sync_orchestration_snapshot() {
  local orchestration_sha="$1"

  rm -rf -- "$SNAPSHOT_DIR"
  mkdir -p "$SNAPSHOT_DIR"
  git -C "$AGGREGATE_DIR" archive "$orchestration_sha" \
    | tar -x -C "$SNAPSHOT_DIR"
  rsync -a --delete \
    --exclude='/.git/' \
    --exclude='/.gitmodules' \
    --exclude="/$MANIFEST" \
    --exclude='/services/' \
    "$SNAPSHOT_DIR/" "$AGGREGATE_DIR/"
}

assert_fast_forward() {
  local name="$1"
  local previous_sha="$2"
  local next_sha="$3"

  if ! git -C "$AGGREGATE_DIR" merge-base \
    --is-ancestor "$previous_sha" "$next_sha"; then
    echo "$name moved non-fast-forward: $previous_sha -> $next_sha" >&2
    exit 1
  fi
}

merge_subtree() {
  local name="$1"
  local path="$2"
  local previous_sha="$3"
  local next_sha="$4"

  if [[ "$previous_sha" == "$next_sha" ]]; then
    return
  fi
  assert_fast_forward "$name" "$previous_sha" "$next_sha"
  git -C "$AGGREGATE_DIR" subtree merge \
    --prefix="$path" \
    "$next_sha" \
    -m "chore(mirror): $name $next_sha 반영"
}

bootstrap_monorepo() {
  local orchestration_sha="$1"
  shift
  local service_shas=("$@")

  git -C "$AGGREGATE_DIR" merge \
    --strategy=ours \
    --allow-unrelated-histories \
    --no-ff \
    "$orchestration_sha" \
    -m "chore(mirror): orchestration 이력 연결"

  sync_orchestration_snapshot "$orchestration_sha"
  commit_if_needed "chore(mirror): orchestration 루트 구조 반영"

  local index
  for index in "${!SERVICE_NAMES[@]}"; do
    local name="${SERVICE_NAMES[$index]}"
    local path="${SERVICE_PATHS[$name]}"
    local sha="${service_shas[$index]}"
    git -C "$AGGREGATE_DIR" subtree add \
      --prefix="$path" \
      "$sha" \
      -m "chore(mirror): $name 이력 편입"
  done
}

git_auth clone \
  --branch "$TARGET_BRANCH" \
  --single-branch \
  "$GITLAB_REPOSITORY_URL" \
  "$AGGREGATE_DIR"
git -C "$AGGREGATE_DIR" remote set-url origin "$GITLAB_REPOSITORY_URL"
git -C "$AGGREGATE_DIR" config user.name "iRead GitLab Mirror"
git -C "$AGGREGATE_DIR" config user.email \
  "iread-gitlab-mirror@users.noreply.github.com"

fetch_source orchestration "$ORCHESTRATION_URL"
for name in "${SERVICE_NAMES[@]}"; do
  fetch_source "$name" "${SERVICE_URLS[$name]}"
done

push_source_refs orchestration
for name in "${SERVICE_NAMES[@]}"; do
  push_source_refs "$name"
done

readonly ORCHESTRATION_BRANCH_SHA="$(
  git -C "$AGGREGATE_DIR" rev-parse \
    "refs/remotes/source/orchestration/heads/$ORCHESTRATION_BRANCH"
)"
if [[ -n "$REQUESTED_ORCHESTRATION_SHA" ]]; then
  git -C "$AGGREGATE_DIR" cat-file \
    -e "$REQUESTED_ORCHESTRATION_SHA^{commit}"
  if ! git -C "$AGGREGATE_DIR" merge-base \
    --is-ancestor \
    "$REQUESTED_ORCHESTRATION_SHA" \
    "$ORCHESTRATION_BRANCH_SHA"; then
    echo "Requested orchestration commit is not on develop: $REQUESTED_ORCHESTRATION_SHA" >&2
    exit 1
  fi
  readonly ORCHESTRATION_SHA="$REQUESTED_ORCHESTRATION_SHA"
else
  readonly ORCHESTRATION_SHA="$ORCHESTRATION_BRANCH_SHA"
fi

declare -a SERVICE_SHAS=()
for name in "${SERVICE_NAMES[@]}"; do
  SERVICE_SHAS+=("$(
    gitlink_sha "$ORCHESTRATION_SHA" "${SERVICE_PATHS[$name]}"
  )")
done

if [[ ! -f "$AGGREGATE_DIR/$MANIFEST" ]]; then
  bootstrap_monorepo "$ORCHESTRATION_SHA" "${SERVICE_SHAS[@]}"
else
  readonly PREVIOUS_ORCHESTRATION_SHA="$(
    manifest_value orchestration.commit
  )"
  if [[ "$PREVIOUS_ORCHESTRATION_SHA" != "$ORCHESTRATION_SHA" ]]; then
    assert_fast_forward \
      orchestration \
      "$PREVIOUS_ORCHESTRATION_SHA" \
      "$ORCHESTRATION_SHA"
    git -C "$AGGREGATE_DIR" merge \
      --strategy=ours \
      --no-ff \
      "$ORCHESTRATION_SHA" \
      -m "chore(mirror): orchestration $ORCHESTRATION_SHA 이력 연결"
  fi

  for index in "${!SERVICE_NAMES[@]}"; do
    name="${SERVICE_NAMES[$index]}"
    merge_subtree \
      "$name" \
      "${SERVICE_PATHS[$name]}" \
      "$(manifest_value "services.$name.commit")" \
      "${SERVICE_SHAS[$index]}"
  done

  sync_orchestration_snapshot "$ORCHESTRATION_SHA"
fi

write_manifest "$ORCHESTRATION_SHA" "${SERVICE_SHAS[@]}"
commit_if_needed \
  "chore(mirror): orchestration 통합 상태 $ORCHESTRATION_SHA 반영"

git_auth -C "$AGGREGATE_DIR" push origin "$TARGET_BRANCH:$TARGET_BRANCH"
