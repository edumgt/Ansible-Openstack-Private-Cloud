#!/usr/bin/env bash
set -euo pipefail

if [ -z "${IMAGE:-}" ]; then
  echo "[ERROR] IMAGE is required. Example: IMAGE=docker.io/user/repo:latest" >&2
  exit 1
fi

CONTAINER_NAME="${CONTAINER_NAME:-python-ansible-playbook}"
RUN_CMD="${RUN_CMD:-tail -f /dev/null}"

if ! docker pull "${IMAGE}"; then
  if ! docker image inspect "${IMAGE}" >/dev/null 2>&1; then
    echo "[ERROR] Failed to pull image and local image not found: ${IMAGE}" >&2
    exit 1
  fi
  echo "[WARN] Pull failed. Using local image: ${IMAGE}" >&2
fi

docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
docker run -d --name "${CONTAINER_NAME}" --restart unless-stopped "${IMAGE}" sh -c "${RUN_CMD}"

docker ps --filter "name=${CONTAINER_NAME}" --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
