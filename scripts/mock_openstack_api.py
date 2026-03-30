#!/usr/bin/env python3
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


TOKEN_ID = "mock-token"
IMAGE_ID = "f4f7b26d-2be8-4f10-9c95-9c3a7f6f51bf"
SERVER_ID = "2f8cf7bb-1472-46f8-9f08-9f2a8d3e44cc"
SERVER2_ID = "7d7859f7-8f9e-4d64-bd8d-0e3bafe1f85f"
NETWORK1_ID = "a5f1b56f-9316-4b37-a89c-2e0e4b3e6cf7"
NETWORK2_ID = "b37a9f4c-6f0d-4d8f-9834-3bf21f99d365"
SUBNET1_ID = "c3a8d3e9-3d90-4a7a-9bc0-3df1739a6f4e"
SUBNET2_ID = "d4b0e7e3-bf26-4f6e-b0aa-8fbf1cd88b3a"
VOLUME1_ID = "8a40dcf7-4f14-4752-9f95-0a3f72fcde79"
VOLUME2_ID = "c9686048-2f6f-4e15-8ea4-95bcf65ba4d2"


def keystone_version_doc(host: str, keystone_port: int) -> dict:
    base = f"http://{host}:{keystone_port}/v3"
    return {
        "version": {
            "id": "v3.14",
            "status": "stable",
            "links": [{"rel": "self", "href": base}],
            "media-types": [
                {
                    "base": "application/json",
                    "type": "application/vnd.openstack.identity-v3+json",
                }
            ],
        }
    }


def token_doc(host: str, keystone_port: int, nova_port: int) -> dict:
    return {
        "token": {
            "methods": ["password"],
            "expires_at": "2030-01-01T00:00:00Z",
            "project": {"id": "project-admin", "name": "admin", "domain": {"id": "default", "name": "Default"}},
            "user": {"id": "user-admin", "name": "admin", "domain": {"id": "default", "name": "Default"}},
            "catalog": [
                {
                    "id": "service-keystone",
                    "type": "identity",
                    "name": "keystone",
                    "endpoints": [
                        {
                            "id": "endpoint-keystone-public",
                            "interface": "public",
                            "region": "RegionOne",
                            "url": f"http://{host}:{keystone_port}/v3",
                        }
                    ],
                },
                {
                    "id": "service-nova",
                    "type": "compute",
                    "name": "nova",
                    "endpoints": [
                        {
                            "id": "endpoint-nova-public",
                            "interface": "public",
                            "region": "RegionOne",
                            "url": f"http://{host}:{keystone_port}/v2.1",
                        }
                    ],
                },
                {
                    "id": "service-glance",
                    "type": "image",
                    "name": "glance",
                    "endpoints": [
                        {
                            "id": "endpoint-glance-public",
                            "interface": "public",
                            "region": "RegionOne",
                            "url": f"http://{host}:{keystone_port}/v2",
                        }
                    ],
                },
                {
                    "id": "service-neutron",
                    "type": "network",
                    "name": "neutron",
                    "endpoints": [
                        {
                            "id": "endpoint-neutron-public",
                            "interface": "public",
                            "region": "RegionOne",
                            "url": f"http://{host}:{keystone_port}/v2.0",
                        }
                    ],
                },
                {
                    "id": "service-cinder",
                    "type": "volumev3",
                    "name": "cinderv3",
                    "endpoints": [
                        {
                            "id": "endpoint-cinder-public",
                            "interface": "public",
                            "region": "RegionOne",
                            "url": f"http://{host}:{keystone_port}/v3",
                        }
                    ],
                },
            ],
        }
    }


def mock_server_doc(
    server_id: str,
    name: str,
    network_name: str,
    fixed_ip: str,
    volume_id: str,
    host: str,
) -> dict:
    return {
        "id": server_id,
        "name": name,
        "status": "ACTIVE",
        "created": "2026-03-30T12:00:00Z",
        "updated": "2026-03-30T12:05:00Z",
        "flavor": {"id": "m1.small", "links": []},
        "image": {"id": IMAGE_ID, "links": []},
        "OS-EXT-SRV-ATTR:host": host,
        "addresses": {
            network_name: [
                {
                    "OS-EXT-IPS:type": "fixed",
                    "addr": fixed_ip,
                    "version": 4,
                }
            ]
        },
        "os-extended-volumes:volumes_attached": [{"id": volume_id}],
    }


def nova_servers_doc(name: str | None = None) -> dict:
    servers = [
        mock_server_doc(
            server_id=SERVER_ID,
            name="compute1",
            network_name="net-compute1",
            fixed_ip="10.10.1.11",
            volume_id=VOLUME1_ID,
            host="compute1",
        ),
        mock_server_doc(
            server_id=SERVER2_ID,
            name="compute2",
            network_name="net-compute2",
            fixed_ip="10.20.1.11",
            volume_id=VOLUME2_ID,
            host="compute2",
        ),
    ]
    if name:
        servers = [server for server in servers if server["name"] == name]
    return {"servers": servers}


def glance_versions_doc(host: str, keystone_port: int) -> dict:
    return {
        "versions": [
            {
                "id": "v2.8",
                "status": "CURRENT",
                "links": [{"rel": "self", "href": f"http://{host}:{keystone_port}/v2"}],
            }
        ]
    }


def glance_images_doc() -> dict:
    return {
        "images": [
            {
                "id": IMAGE_ID,
                "name": "ubuntu-22.04",
                "status": "active",
                "disk_format": "qcow2",
                "container_format": "bare",
                "visibility": "public",
            }
        ]
    }


def glance_image_doc(image_id: str) -> tuple[int, dict]:
    if image_id != IMAGE_ID:
        return 404, {"error": {"message": f"Image not found: {image_id}"}}
    return 200, {
        "id": IMAGE_ID,
        "name": "ubuntu-22.04",
        "status": "active",
        "disk_format": "qcow2",
        "container_format": "bare",
        "visibility": "public",
    }


def neutron_networks_doc() -> dict:
    return {
        "networks": [
            {
                "id": NETWORK1_ID,
                "name": "net-compute1",
                "status": "ACTIVE",
                "admin_state_up": True,
                "subnets": [SUBNET1_ID],
            },
            {
                "id": NETWORK2_ID,
                "name": "net-compute2",
                "status": "ACTIVE",
                "admin_state_up": True,
                "subnets": [SUBNET2_ID],
            },
        ]
    }


def neutron_subnets_doc() -> dict:
    return {
        "subnets": [
            {
                "id": SUBNET1_ID,
                "network_id": NETWORK1_ID,
                "name": "subnet-compute1",
                "cidr": "10.10.1.0/24",
                "gateway_ip": "10.10.1.1",
                "ip_version": 4,
            },
            {
                "id": SUBNET2_ID,
                "network_id": NETWORK2_ID,
                "name": "subnet-compute2",
                "cidr": "10.20.1.0/24",
                "gateway_ip": "10.20.1.1",
                "ip_version": 4,
            },
        ]
    }


def cinder_volumes_doc() -> dict:
    return {
        "volumes": [
            {
                "id": VOLUME1_ID,
                "name": "vol-compute1",
                "size": 20,
                "status": "in-use",
                "attachments": [{"server_id": SERVER_ID, "attachment_id": "att-01"}],
            },
            {
                "id": VOLUME2_ID,
                "name": "vol-compute2",
                "size": 30,
                "status": "in-use",
                "attachments": [{"server_id": SERVER2_ID, "attachment_id": "att-02"}],
            },
        ]
    }


def cinder_volume_doc(volume_id: str) -> tuple[int, dict]:
    for volume in cinder_volumes_doc()["volumes"]:
        if volume["id"] == volume_id:
            return 200, {"volume": volume}
    return 404, {"error": {"message": f"Volume not found: {volume_id}"}}


def dashboard_html() -> str:
    return f"""<!doctype html>
<html lang=\"ko\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Mock Horizon Dashboard</title>
  <style>
    :root {{
      --bg: #f5f7fb;
      --card: #ffffff;
      --ink: #1a2733;
      --accent: #0a6ebd;
      --ok: #0f9d58;
      --line: #d9e2ec;
    }}
    body {{
      margin: 0;
      font-family: "Noto Sans KR", "Pretendard", sans-serif;
      color: var(--ink);
      background: radial-gradient(circle at 10% 10%, #dcecff, transparent 35%), var(--bg);
    }}
    .wrap {{ max-width: 980px; margin: 32px auto; padding: 0 16px; }}
    h1 {{ margin: 0 0 12px; font-size: 2rem; }}
    .meta {{ margin: 0 0 20px; color: #425466; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
    .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 16px; box-shadow: 0 8px 20px rgba(17, 24, 39, 0.06); }}
    .badge {{ display: inline-block; background: #e7f3ff; color: var(--accent); border-radius: 999px; padding: 3px 10px; font-size: 12px; font-weight: 700; }}
    .ok {{ color: var(--ok); font-weight: 700; }}
    ul {{ margin: 10px 0 0; padding-left: 18px; }}
    li {{ margin: 6px 0; }}
    code {{ background: #f0f4f8; padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <h1>OpenStack Horizon Mock</h1>
    <p class=\"meta\">강의 실습용 대시보드: Compute 2대, Neutron 분리 네트워크, Cinder 볼륨 연결 상태</p>
    <div class=\"grid\">
      <section class=\"card\">
        <span class=\"badge\">COMPUTE</span>
        <h2>compute1</h2>
        <p class=\"ok\">ACTIVE</p>
        <ul>
          <li>Neutron Network: <code>net-compute1 (10.10.1.0/24)</code></li>
          <li>Cinder Volume: <code>vol-compute1 (20GB)</code></li>
          <li>Fixed IP: <code>10.10.1.11</code></li>
        </ul>
      </section>
      <section class=\"card\">
        <span class=\"badge\">COMPUTE</span>
        <h2>compute2</h2>
        <p class=\"ok\">ACTIVE</p>
        <ul>
          <li>Neutron Network: <code>net-compute2 (10.20.1.0/24)</code></li>
          <li>Cinder Volume: <code>vol-compute2 (30GB)</code></li>
          <li>Fixed IP: <code>10.20.1.11</code></li>
        </ul>
      </section>
      <section class=\"card\">
        <span class=\"badge\">API</span>
        <h2>Endpoint</h2>
        <ul>
          <li>Keystone: <code>/v3</code></li>
          <li>Nova: <code>/v2.1/servers/detail</code></li>
          <li>Neutron: <code>/v2.0/networks</code></li>
          <li>Cinder: <code>/v3/project-admin/volumes/detail</code></li>
        </ul>
      </section>
    </div>
  </div>
</body>
</html>
"""


def nova_version_doc(host: str, nova_port: int) -> dict:
    base = f"http://{host}:{nova_port}/v2.1"
    return {
        "version": {
            "id": "v2.1",
            "status": "CURRENT",
            "links": [{"rel": "self", "href": base}],
        }
    }


def nova_services_doc() -> dict:
    return {
        "services": [
            {
                "id": 1,
                "binary": "nova-scheduler",
                "host": "controller",
                "zone": "internal",
                "status": "enabled",
                "state": "up",
                "updated_at": "2026-03-30T12:00:00.000000",
                "disabled_reason": None,
            },
            {
                "id": 2,
                "binary": "nova-conductor",
                "host": "controller",
                "zone": "internal",
                "status": "enabled",
                "state": "up",
                "updated_at": "2026-03-30T12:00:00.000000",
                "disabled_reason": None,
            },
            {
                "id": 3,
                "binary": "nova-compute",
                "host": "compute1",
                "zone": "nova",
                "status": "enabled",
                "state": "up",
                "updated_at": "2026-03-30T12:00:00.000000",
                "disabled_reason": None,
            },
        ]
    }


def nova_hypervisors_doc() -> dict:
    return {
        "hypervisors": [
            {
                "id": 1,
                "hypervisor_hostname": "compute1",
                "state": "up",
                "status": "enabled",
                "vcpus": 4,
                "memory_mb": 8192,
                "local_gb": 80,
                "service": {"host": "compute1", "id": 3, "disabled_reason": None},
            }
        ]
    }


class MockOpenStackHandler(BaseHTTPRequestHandler):
    host = "127.0.0.1"
    keystone_port = 5000
    nova_port = 8774

    def _send_json(self, status: int, payload: dict, headers: dict | None = None) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        if headers:
            for key, value in headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, status: int, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path in ["/healthz", "/"]:
            self._send_json(
                200,
                {
                    "status": "ok",
                    "services": {
                        "keystone": f"http://{self.host}:{self.keystone_port}/v3",
                        "nova": f"http://{self.host}:{self.keystone_port}/v2.1",
                    },
                },
            )
            return

        if self.path == "/v3":
            self._send_json(200, keystone_version_doc(self.host, self.keystone_port))
            return

        if path in ["/v2.1", "/v2.1/"]:
            self._send_json(200, nova_version_doc(self.host, self.nova_port))
            return

        if path in ["/v2.1/os-services", "/v2.1/os-services/"]:
            self._send_json(200, nova_services_doc())
            return

        if path in ["/v2.1/os-hypervisors/detail", "/v2.1/os-hypervisors/detail/", "/v2.1/os-hypervisors", "/v2.1/os-hypervisors/"]:
            self._send_json(200, nova_hypervisors_doc())
            return

        if path in ["/v2.1/servers", "/v2.1/servers/", "/v2.1/servers/detail", "/v2.1/servers/detail/"]:
            name = query.get("name", [None])[0]
            self._send_json(200, nova_servers_doc(name=name))
            return

        if path.startswith("/v2.1/servers/"):
            server_id = path.strip("/").split("/")[-1]
            for server in nova_servers_doc()["servers"]:
                if server_id == server["id"]:
                    self._send_json(200, {"server": server})
                    return
            self._send_json(404, {"error": {"message": f"Server not found: {server_id}"}})
            return

        if path in ["/v2.0/networks", "/v2.0/networks/"]:
            self._send_json(200, neutron_networks_doc())
            return

        if path in ["/v2.0/subnets", "/v2.0/subnets/"]:
            self._send_json(200, neutron_subnets_doc())
            return

        if path in ["/v2", "/v2/"]:
            self._send_json(200, glance_versions_doc(self.host, self.keystone_port))
            return

        if path in ["/v2/images", "/v2/images/"]:
            self._send_json(200, glance_images_doc())
            return

        if path.startswith("/v2/images/"):
            image_id = path.strip("/").split("/")[-1]
            status, payload = glance_image_doc(image_id)
            self._send_json(status, payload)
            return

        if path in ["/v3/project-admin/volumes", "/v3/project-admin/volumes/", "/v3/project-admin/volumes/detail", "/v3/project-admin/volumes/detail/"]:
            self._send_json(200, cinder_volumes_doc())
            return

        if path.startswith("/v3/project-admin/volumes/"):
            volume_id = path.strip("/").split("/")[-1]
            status, payload = cinder_volume_doc(volume_id)
            self._send_json(status, payload)
            return

        if path == "/dashboard":
            self._send_html(200, dashboard_html())
            return

        self._send_json(404, {"error": {"message": f"Path not found: {self.path}"}})

    def do_POST(self) -> None:
        if self.path == "/v3/auth/tokens":
            self._send_json(
                201,
                token_doc(self.host, self.keystone_port, self.nova_port),
                headers={"X-Subject-Token": TOKEN_ID},
            )
            return

        self._send_json(404, {"error": {"message": f"Path not found: {self.path}"}})


class ReusableThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--keystone-port", type=int, default=5000)
    parser.add_argument("--nova-port", type=int, default=8774)
    args = parser.parse_args()

    MockOpenStackHandler.host = args.host
    MockOpenStackHandler.keystone_port = args.keystone_port
    MockOpenStackHandler.nova_port = args.nova_port

    server = ReusableThreadingHTTPServer((args.host, args.keystone_port), MockOpenStackHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
