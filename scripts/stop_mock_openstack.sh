#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="${1:-$(pwd)}"
STATE_DIR="${WORKSPACE_ROOT}/.lab/openstack-mock"
PID_FILE="${STATE_DIR}/server.pid"

if [[ ! -f "${PID_FILE}" ]]; then
  echo "mock-openstack not running"
  exit 0
fi

PID="$(cat "${PID_FILE}")"
if kill -0 "${PID}" 2>/dev/null; then
  kill "${PID}"
fi

rm -f "${PID_FILE}"
echo "mock-openstack stopped"
