#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="${1:-$(pwd)}"
STATE_DIR="${WORKSPACE_ROOT}/.lab/openstack-mock"
PID_FILE="${STATE_DIR}/server.pid"
LOG_FILE="${STATE_DIR}/server.log"

mkdir -p "${STATE_DIR}"

if [[ -f "${PID_FILE}" ]] && kill -0 "$(cat "${PID_FILE}")" 2>/dev/null; then
  echo "mock-openstack already running"
  exit 0
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"
if [[ -x "${WORKSPACE_ROOT}/.venv/bin/python" ]]; then
  PYTHON_BIN="${WORKSPACE_ROOT}/.venv/bin/python"
fi

nohup "${PYTHON_BIN}" "${WORKSPACE_ROOT}/scripts/mock_openstack_api.py" \
  --host 127.0.0.1 \
  --keystone-port 5000 \
  --nova-port 8774 \
  >"${LOG_FILE}" 2>&1 &

echo "$!" > "${PID_FILE}"
sleep 1
echo "mock-openstack started"
