#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements-codespaces.txt

if ! grep -q "source /workspaces/.*/.venv/bin/activate" ~/.bashrc 2>/dev/null; then
  printf '\nsource %s/.venv/bin/activate\n' "$(pwd)" >> ~/.bashrc
fi

mkdir -p .lab/openstack-mock

printf '\nCodespaces bootstrap complete.\n'
printf 'Next steps:\n'
printf '  ansible-playbook -i ansible/inventories/local/hosts.ini lecture22/playbook.yml -e install_enabled=true\n'
printf '  ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=false\n'
