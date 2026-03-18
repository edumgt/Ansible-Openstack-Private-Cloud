#!/usr/bin/env bash
# build_ova.sh – Build the Ansible+OpenStack Lab OVA using Packer
#
# Prerequisites:
#   - VirtualBox >= 6.1  (https://www.virtualbox.org/wiki/Downloads)
#   - Packer   >= 1.10  (https://developer.hashicorp.com/packer/install)
#
# Usage:
#   ./scripts/build_ova.sh
#   ./scripts/build_ova.sh --only-validate   # syntax check only
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACKER_DIR="${REPO_ROOT}/packer"
OUTPUT_DIR="${PACKER_DIR}/output-ansible-openstack-lab"
OVA_NAME="ansible-openstack-lab.ova"

##############################################################################
# Helper
##############################################################################
info()  { echo "[INFO]  $*"; }
error() { echo "[ERROR] $*" >&2; exit 1; }

##############################################################################
# Dependency checks
##############################################################################
command -v packer     >/dev/null 2>&1 || error "packer not found. Install from https://developer.hashicorp.com/packer/install"
command -v VBoxManage >/dev/null 2>&1 || error "VBoxManage not found. Install VirtualBox from https://www.virtualbox.org/wiki/Downloads"

info "Packer:    $(packer version)"
info "VBoxManage: $(VBoxManage --version)"

##############################################################################
# Validate only
##############################################################################
if [[ "${1:-}" == "--only-validate" ]]; then
    info "Initialising Packer plugins..."
    packer init "${PACKER_DIR}"
    info "Validating Packer template..."
    packer validate "${PACKER_DIR}"
    info "Validation passed."
    exit 0
fi

##############################################################################
# Build
##############################################################################
info "Initialising Packer plugins..."
packer init "${PACKER_DIR}"

info "Starting OVA build (this takes ~30-60 min depending on internet speed and disk I/O)..."
packer build \
    -on-error=ask \
    "${PACKER_DIR}"

OVA_PATH="${OUTPUT_DIR}/${OVA_NAME}"
if [ ! -f "${OVA_PATH}" ]; then
    # Packer sometimes names the file differently – find it
    OVA_PATH="$(find "${OUTPUT_DIR}" -name "*.ova" | head -1)"
fi

if [ -z "${OVA_PATH}" ] || [ ! -f "${OVA_PATH}" ]; then
    error "OVA file not found under ${OUTPUT_DIR}"
fi

info "OVA built successfully: ${OVA_PATH}"
info ""
info "======================================================"
info " Import into VirtualBox:"
info "   VBoxManage import '${OVA_PATH}' --vsys 0 --vmname ansible-openstack-lab"
info " Or via GUI: File → Import Appliance..."
info "======================================================"
