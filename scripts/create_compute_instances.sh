#!/usr/bin/env bash
# lecture21용 compute1, compute2 인스턴스 생성 스크립트
set -euo pipefail

WORKSPACE_ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
OPENRC_PATH="${WORKSPACE_ROOT}/.lab/real-openstack-openrc"
VENV_OPENSTACK="${WORKSPACE_ROOT}/.venv/bin/openstack"

if [ ! -f "$OPENRC_PATH" ]; then
  echo "[ERROR] $OPENRC_PATH not found"
  exit 1
fi

if [ ! -f "$VENV_OPENSTACK" ]; then
  echo "[ERROR] $VENV_OPENSTACK not found"
  exit 1
fi

source "$OPENRC_PATH"

echo "==> 1. Cinder 볼륨 생성"
$VENV_OPENSTACK volume create --size 1 vol-compute1 || echo "vol-compute1 already exists"
$VENV_OPENSTACK volume create --size 1 vol-compute2 || echo "vol-compute2 already exists"

echo ""
echo "==> 2. compute1 서버 생성 (net-compute1 네트워크)"
$VENV_OPENSTACK server create \
  --flavor cirros256 \
  --image cirros-0.6.2-x86_64-disk \
  --network net-compute1 \
  --key-name devstack-compute-key \
  compute1 || echo "compute1 already exists"

echo ""
echo "==> 3. compute2 서버 생성 (net-compute2 네트워크)"
$VENV_OPENSTACK server create \
  --flavor cirros256 \
  --image cirros-0.6.2-x86_64-disk \
  --network net-compute2 \
  --key-name devstack-compute-key \
  compute2 || echo "compute2 already exists"

echo ""
echo "==> 4. 서버 부팅 대기 (30초)"
sleep 30

echo ""
echo "==> 5. 볼륨 연결"
$VENV_OPENSTACK server add volume compute1 vol-compute1 || echo "vol-compute1 already attached"
$VENV_OPENSTACK server add volume compute2 vol-compute2 || echo "vol-compute2 already attached"

echo ""
echo "==> 6. Floating IP 생성 및 연결"
FLOATING_IP_1=$($VENV_OPENSTACK floating ip create public -f value -c floating_ip_address 2>/dev/null || echo "")
if [ -n "$FLOATING_IP_1" ]; then
  echo "compute1 Floating IP: $FLOATING_IP_1"
  $VENV_OPENSTACK server add floating ip compute1 "$FLOATING_IP_1" || true
fi

FLOATING_IP_2=$($VENV_OPENSTACK floating ip create public -f value -c floating_ip_address 2>/dev/null || echo "")
if [ -n "$FLOATING_IP_2" ]; then
  echo "compute2 Floating IP: $FLOATING_IP_2"
  $VENV_OPENSTACK server add floating ip compute2 "$FLOATING_IP_2" || true
fi

echo ""
echo "==> 7. 최종 서버 목록"
$VENV_OPENSTACK server list

echo ""
echo "==> 완료! lecture21을 다시 실행하세요:"
echo "cd $WORKSPACE_ROOT"
echo "$WORKSPACE_ROOT/.venv/bin/ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml \\"
echo "  -e install_enabled=false \\"
echo "  -e openrc_path=$OPENRC_PATH \\"
echo "  -e use_mock_openstack_auth=false \\"
echo "  -e compute_ssh_user=cirros \\"
echo "  -e compute_ssh_private_key_file=$WORKSPACE_ROOT/.lab/devstack_compute_key"
