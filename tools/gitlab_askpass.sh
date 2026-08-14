#!/usr/bin/env bash

set -euo pipefail

case "${1:-}" in
  *Username*)
    printf '%s' "${GITLAB_USERNAME:?GITLAB_USERNAME is required}"
    ;;
  *Password*)
    printf '%s' "${GITLAB_PUSH_TOKEN:?GITLAB_PUSH_TOKEN is required}"
    ;;
  *)
    echo "Unsupported Git credential prompt" >&2
    exit 1
    ;;
esac
