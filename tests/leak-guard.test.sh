#!/usr/bin/env bash
set -uo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
GUARD="$ROOT/.github/scripts/leak-guard.sh"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/pmagents-leak-guard.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
fail=0

expect_fail() {
  local name="$1"
  local text="$2"
  local file="$TMP/$name"
  printf '%s\n' "$text" > "$file"
  if "$GUARD" "$file" >/dev/null 2>&1; then
    echo "FAIL: $name did not trigger" >&2; fail=1
  fi
}

expect_pass() {
  local name="$1"
  local text="$2"
  local file="$TMP/$name"
  printf '%s\n' "$text" > "$file"
  if ! "$GUARD" "$file" >/dev/null 2>&1; then
    echo "FAIL: $name false-positive" >&2; fail=1
  fi
}

operator_path='/Users/david''hunter/private-runtime'
secret_shape='sk-ant-''abcdefghijklmnopqrstuvwxyz'
expect_fail operator-path "source=$operator_path"
expect_fail secret-shape "OPENAI_API_KEY=$secret_shape"
expect_pass clean 'AscendOps PMAgents uses fictional Ridgeline fixtures.'

if [ "$fail" -ne 0 ]; then
  echo 'leak-guard.test: FAIL' >&2
  exit 1
fi
echo 'leak-guard.test: PASS'
