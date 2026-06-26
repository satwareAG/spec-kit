#!/usr/bin/env bash
# daily-routine.sh — thin dispatcher for daily rituals.
#
# Usage:
#   scripts/daily-routine.sh sod     # Start-of-Day
#   scripts/daily-routine.sh eod     # End-of-Day
#   scripts/daily-routine.sh pre-pr  # Pre-PR health checks
#   scripts/daily-routine.sh help
#
# Part of IPADP Phase 3.2 (L3 upstream sync automation).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    cat <<EOF
Usage: $0 <command>

Commands:
  sod     Run Start-of-Day protocol (privacy + upstream-sync checks)
  eod     Run End-of-Day protocol (privacy check)
  pre-pr  Run pre-PR health checks (ruff, pytest, privacy, sync)
  help    Show this help
EOF
}

cmd="${1:-help}"
case "$cmd" in
    sod)  exec "$SCRIPT_DIR/bash/sod.sh" ;;
    eod)  exec "$SCRIPT_DIR/bash/eod.sh" ;;
    pre-pr) exec "$SCRIPT_DIR/bash/pre-pr.sh" ;;
    help|-h|--help) usage ;;
    *)
        echo "ERROR: unknown command '$cmd'" >&2
        usage
        exit 2
        ;;
esac
