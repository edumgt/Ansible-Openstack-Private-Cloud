#!/usr/bin/env bash
# provision.sh – Core provisioning inside the VM
# Runs as root via sudo
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

ANSIBLE_USER="${ANSIBLE_USER:-ansible}"
WORKSPACE="/opt/ansible-openstack"

echo "==> [provision] Update & install system packages"
apt-get update -y
apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    ca-certificates \
    gnupg \
    lsb-release \
    apt-transport-https \
    software-properties-common \
    vim \
    net-tools \
    openssh-server \
    unzip \
    jq

echo "==> [provision] Upgrade pip"
python3 -m pip install --upgrade pip

echo "==> [provision] Install ansible-core and tooling"
python3 -m pip install \
    "ansible-core>=2.15" \
    ansible-lint \
    boto3 \
    botocore \
    openstacksdk \
    python-openstackclient

echo "==> [provision] Create workspace directory"
mkdir -p "${WORKSPACE}"
chown -R "${ANSIBLE_USER}:${ANSIBLE_USER}" "${WORKSPACE}"

echo "==> [provision] Create helper alias for ansible user"
cat >> /home/"${ANSIBLE_USER}"/.bashrc << 'EOF'

# Ansible OpenStack Lab
export WORKSPACE=/opt/ansible-openstack
alias cdlab='cd $WORKSPACE'
alias ap='ansible-playbook'
EOF

echo "==> [provision] Done."
