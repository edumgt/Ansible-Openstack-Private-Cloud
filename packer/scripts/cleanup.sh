#!/usr/bin/env bash
# cleanup.sh – Minimize OVA disk footprint
# Runs as root via sudo
set -euo pipefail

echo "==> [cleanup] Remove apt caches"
apt-get clean
apt-get autoremove -y

echo "==> [cleanup] Remove temporary files"
rm -rf /tmp/* /var/tmp/*

echo "==> [cleanup] Truncate machine-id (re-generated on first boot)"
truncate -s 0 /etc/machine-id
rm -f /var/lib/dbus/machine-id
ln -s /etc/machine-id /var/lib/dbus/machine-id

echo "==> [cleanup] Remove SSH host keys (re-generated on first boot)"
rm -f /etc/ssh/ssh_host_*

echo "==> [cleanup] Remove cloud-init logs"
cloud-init clean --logs 2>/dev/null || true

echo "==> [cleanup] Zero out free space for better OVA compression"
dd if=/dev/zero of=/EMPTY bs=1M 2>/dev/null || true
rm -f /EMPTY
sync

echo "==> [cleanup] Done."
