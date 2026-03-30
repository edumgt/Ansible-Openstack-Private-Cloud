#!/usr/bin/env bash
set -euo pipefail

workspace_root="${1:-$(pwd)}"
output_path="${2:-${workspace_root}/.lab/real-openstack-openrc}"

: "${OS_AUTH_URL:?OS_AUTH_URL is required}"
: "${OS_USERNAME:?OS_USERNAME is required}"
: "${OS_PASSWORD:?OS_PASSWORD is required}"
: "${OS_PROJECT_NAME:?OS_PROJECT_NAME is required}"

os_user_domain_name="${OS_USER_DOMAIN_NAME:-Default}"
os_project_domain_name="${OS_PROJECT_DOMAIN_NAME:-Default}"
os_region_name="${OS_REGION_NAME:-RegionOne}"
os_interface="${OS_INTERFACE:-public}"
os_identity_api_version="${OS_IDENTITY_API_VERSION:-3}"

mkdir -p "$(dirname "${output_path}")"

cat > "${output_path}" <<EOF
export OS_AUTH_URL=${OS_AUTH_URL}
export OS_USERNAME=${OS_USERNAME}
export OS_PASSWORD=${OS_PASSWORD}
export OS_PROJECT_NAME=${OS_PROJECT_NAME}
export OS_USER_DOMAIN_NAME=${os_user_domain_name}
export OS_PROJECT_DOMAIN_NAME=${os_project_domain_name}
export OS_REGION_NAME=${os_region_name}
export OS_INTERFACE=${os_interface}
export OS_IDENTITY_API_VERSION=${os_identity_api_version}
EOF

chmod 600 "${output_path}"
echo "wrote ${output_path}"
