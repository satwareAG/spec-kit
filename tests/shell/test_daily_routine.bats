#!/usr/bin/env bats
# tests/shell/test_daily_routine.bats — IPADP Phase 4.2 (issue #23)
# Covers scripts/daily-routine.sh dispatcher.

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    DISPATCHER="$REPO_ROOT/scripts/daily-routine.sh"
}

@test "daily-routine: help exits 0 and prints usage" {
    run "$DISPATCHER" help
    [ "$status" -eq 0 ]
    [[ "$output" == *"Usage:"* ]]
    [[ "$output" == *"sod"* ]]
    [[ "$output" == *"eod"* ]]
}

@test "daily-routine: no args prints help and exits 0" {
    run "$DISPATCHER"
    [ "$status" -eq 0 ]
    [[ "$output" == *"Usage:"* ]]
}

@test "daily-routine: unknown command exits 2" {
    run "$DISPATCHER" not-a-command
    [ "$status" -eq 2 ]
    [[ "$output" == *"unknown command"* ]]
}

@test "daily-routine: eod delegates to bash/eod.sh" {
    run "$DISPATCHER" eod
    # eod runs privacy check; on a clean tree it exits 0
    [ "$status" -eq 0 ]
    [[ "$output" == *"End-of-Day"* ]]
}
