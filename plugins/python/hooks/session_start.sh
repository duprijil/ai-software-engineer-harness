#!/usr/bin/env bash
set -euo pipefail

project_dir="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ ! -f "$project_dir/pyproject.toml" ]; then
    exit 0
fi

cat "${CLAUDE_PLUGIN_ROOT}/hooks/core_rules.md"
