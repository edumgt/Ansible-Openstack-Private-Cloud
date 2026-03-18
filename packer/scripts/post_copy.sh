#!/usr/bin/env bash
# post_copy.sh – Post file-copy setup inside the VM
# Runs as root via sudo
set -euo pipefail

ANSIBLE_USER="${ANSIBLE_USER:-ansible}"
WORKSPACE="/opt/ansible-openstack"

echo "==> [post_copy] Fix ownership of workspace"
chown -R "${ANSIBLE_USER}:${ANSIBLE_USER}" "${WORKSPACE}"

echo "==> [post_copy] Remove packer/ output dirs to save space"
rm -rf "${WORKSPACE}/packer/output-*"

echo "==> [post_copy] Install Python requirements from requirements.txt"
if [ -f "${WORKSPACE}/requirements.txt" ]; then
    python3 -m pip install -r "${WORKSPACE}/requirements.txt"
fi

echo "==> [post_copy] Install Ansible Galaxy collections from requirements.yml"
if [ -f "${WORKSPACE}/requirements.yml" ]; then
    ansible-galaxy collection install \
        -r "${WORKSPACE}/requirements.yml" \
        -p /usr/share/ansible/collections
fi

echo "==> [post_copy] Pre-download pip wheels for offline (air-gapped) use"
WHEEL_DIR="${WORKSPACE}/offline/pip-wheels"
mkdir -p "${WHEEL_DIR}"
if python3 -m pip download \
    "ansible-core>=2.15" \
    ansible-lint \
    boto3 \
    botocore \
    openstacksdk \
    python-openstackclient \
    -d "${WHEEL_DIR}" \
    --quiet 2>/tmp/pip-download.log; then
    echo "==> [post_copy] pip wheel download complete ($(ls "${WHEEL_DIR}" | wc -l) files)"
else
    echo "[WARN] pip wheel download failed; offline pip cache may be incomplete" >&2
    cat /tmp/pip-download.log >&2
fi

echo "==> [post_copy] Bundle Ansible Galaxy collections for offline use"
COLLECTIONS_ARCHIVE="${WORKSPACE}/offline/collections"
mkdir -p "${COLLECTIONS_ARCHIVE}"
cp -r /usr/share/ansible/collections/. "${COLLECTIONS_ARCHIVE}/" 2>/dev/null || true

chown -R "${ANSIBLE_USER}:${ANSIBLE_USER}" "${WORKSPACE}"

echo "==> [post_copy] Done."
