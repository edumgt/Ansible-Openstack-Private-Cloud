#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="${1:-$(pwd)}"
KEYSTONE_PORT="${2:-15000}"
NOVA_PORT="${3:-18774}"
STATE_DIR="${WORKSPACE_ROOT}/.lab/openstack-mock"
PID_FILE="${STATE_DIR}/server.pid"
LOG_FILE="${STATE_DIR}/server.log"

mkdir -p "${STATE_DIR}"

if [[ -f "${PID_FILE}" ]] && kill -0 "$(cat "${PID_FILE}")" 2>/dev/null; then
  echo "mock-openstack already running"
  exit 0
fi

if [[ -f "${PID_FILE}" ]] && ! kill -0 "$(cat "${PID_FILE}")" 2>/dev/null; then
  rm -f "${PID_FILE}"
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"
if [[ -x "${WORKSPACE_ROOT}/.venv/bin/python" ]]; then
  PYTHON_BIN="${WORKSPACE_ROOT}/.venv/bin/python"
fi

nohup "${PYTHON_BIN}" "${WORKSPACE_ROOT}/scripts/mock_openstack_api.py" \
  --host 127.0.0.1 \
  --keystone-port "${KEYSTONE_PORT}" \
  --nova-port "${NOVA_PORT}" \
  >"${LOG_FILE}" 2>&1 &

PID="$!"
echo "${PID}" > "${PID_FILE}"
sleep 1

if ! kill -0 "${PID}" 2>/dev/null; then
  echo "mock-openstack failed to start" >&2
  if [[ -f "${LOG_FILE}" ]]; then
    tail -n 50 "${LOG_FILE}" >&2 || true
  fi
  rm -f "${PID_FILE}"
  exit 1
fi

echo "mock-openstack started pid=${PID} keystone_port=${KEYSTONE_PORT} nova_port=${NOVA_PORT}"
