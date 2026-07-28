#!/usr/bin/env bash

set -euo pipefail

readonly GITLAB_REPOSITORY_URL="${GITLAB_REPOSITORY_URL:-https://lab.ssafy.com/s15-webmobile2-sub1/S15P11B105.git}"
readonly GITLAB_USERNAME="${GITLAB_USERNAME:-oauth2}"
readonly ORCHESTRATION_URL="https://github.com/iRead-B105/iRead.git"
readonly ORCHESTRATION_BRANCH="develop"
readonly REQUESTED_ORCHESTRATION_SHA="${SYNC_ORCHESTRATION_SHA:-}"
readonly REBUILD_HISTORY="${REBUILD_GITLAB_HISTORY:-false}"
readonly TARGET_BRANCH="main"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly GITLAB_ASKPASS="$SCRIPT_DIR/gitlab_askpass.sh"
readonly WORK_DIR="$(mktemp -d)"
readonly AGGREGATE_DIR="$WORK_DIR/aggregate"

declare -ar SERVICE_NAMES=(backend frontend ai app eyetracking)
declare -Ar SERVICE_URLS=(
  [backend]="https://github.com/iRead-B105/iRead-backend.git"
  [frontend]="https://github.com/iRead-B105/iRead-frontend-web.git"
  [ai]="https://github.com/iRead-B105/iRead-ai.git"
  [app]="https://github.com/iRead-B105/iRead-frontend-app.git"
  [eyetracking]="https://github.com/iRead-B105/iRead-eyetracking.git"
)
declare -Ar SERVICE_PATHS=(
  [backend]="services/backend"
  [frontend]="services/frontend-web"
  [ai]="services/ai"
  [app]="services/frontend-app"
  [eyetracking]="services/eyetracking"
)

if [[ -z "${GITLAB_PUSH_TOKEN:-}" ]]; then
  echo "GITLAB_PUSH_TOKEN is required" >&2
  exit 1
fi
export GITLAB_USERNAME GITLAB_PUSH_TOKEN

cleanup() {
  rm -rf -- "$WORK_DIR"
}
trap cleanup EXIT

git_auth() {
  GIT_ASKPASS="$GITLAB_ASKPASS" \
    GIT_TERMINAL_PROMPT=0 \
    git -c "credential.username=$GITLAB_USERNAME" "$@"
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
  git -C "$AGGREGATE_DIR" fetch --force --prune --no-tags "$name" \
    "+refs/heads/*:refs/remotes/source/$name/heads/*" \
    "+refs/tags/*:refs/tags/upstream/$name/*"
}

push_source_refs() {
  local name="$1"

  git_auth -C "$AGGREGATE_DIR" push --prune origin \
    "refs/remotes/source/$name/heads/*:refs/heads/upstream/$name/*"

  if git -C "$AGGREGATE_DIR" for-each-ref \
    --format='%(refname)' "refs/tags/upstream/$name/" | grep -q .; then
    git_auth -C "$AGGREGATE_DIR" push --prune origin \
      "refs/tags/upstream/$name/*:refs/tags/upstream/$name/*"
  fi
}

fetch_notes_if_present() {
  local ref="$1"

  if git_auth -C "$AGGREGATE_DIR" ls-remote \
    --exit-code origin "$ref" >/dev/null 2>&1; then
    git_auth -C "$AGGREGATE_DIR" fetch origin "+$ref:$ref"
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

git_auth clone \
  --branch "$TARGET_BRANCH" \
  --single-branch \
  "$GITLAB_REPOSITORY_URL" \
  "$AGGREGATE_DIR"
git -C "$AGGREGATE_DIR" remote set-url origin "$GITLAB_REPOSITORY_URL"
git -C "$AGGREGATE_DIR" config user.name "iRead GitLab Projection"
git -C "$AGGREGATE_DIR" config user.email \
  "iread-gitlab-projection@users.noreply.github.com"
readonly ORIGINAL_MAIN_SHA="$(
  git -C "$AGGREGATE_DIR" rev-parse "$TARGET_BRANCH"
)"

fetch_notes_if_present refs/notes/iread-source-state
fetch_notes_if_present refs/notes/iread-source-map

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

declare -a PROJECT_ARGS=(
  --repo "$AGGREGATE_DIR"
  --orchestration "$ORCHESTRATION_SHA"
)
for index in "${!SERVICE_NAMES[@]}"; do
  PROJECT_ARGS+=(
    "--${SERVICE_NAMES[$index]}"
    "${SERVICE_SHAS[$index]}"
  )
done
if [[ "$REBUILD_HISTORY" == "true" ]]; then
  PROJECT_ARGS+=(--rebuild)
fi

set +e
python3 "$SCRIPT_DIR/project_gitlab_history.py" "${PROJECT_ARGS[@]}"
readonly projection_status=$?
set -e
if [[ $projection_status -eq 3 ]]; then
  echo "Projection migration is pending; leaving GitLab main unchanged."
  exit 0
fi
if [[ $projection_status -ne 0 ]]; then
  exit "$projection_status"
fi

declare -a PUSH_ARGS=(
  --atomic
  origin
  "HEAD:refs/heads/$TARGET_BRANCH"
  "+refs/notes/iread-source-state:refs/notes/iread-source-state"
  "+refs/notes/iread-source-map:refs/notes/iread-source-map"
)
if [[ "$REBUILD_HISTORY" == "true" ]]; then
  PUSH_ARGS=(
    --atomic
    "--force-with-lease=refs/heads/$TARGET_BRANCH:$ORIGINAL_MAIN_SHA"
    origin
    "HEAD:refs/heads/$TARGET_BRANCH"
    "+refs/notes/iread-source-state:refs/notes/iread-source-state"
    "+refs/notes/iread-source-map:refs/notes/iread-source-map"
  )
fi

git_auth -C "$AGGREGATE_DIR" push "${PUSH_ARGS[@]}"
