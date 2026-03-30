#!/usr/bin/env python3
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


TOKEN_ID = "mock-token"
IMAGE_ID = "f4f7b26d-2be8-4f10-9c95-9c3a7f6f51bf"
SERVER_ID = "2f8cf7bb-1472-46f8-9f08-9f2a8d3e44cc"


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
            ],
        }
    }


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


def mock_server_doc() -> dict:
    return {
        "id": SERVER_ID,
        "name": "vm-demo-01",
        "status": "ACTIVE",
        "tenant_id": "project-admin",
        "user_id": "user-admin",
        "hostId": "mock-host-id",
        "created": "2026-03-30T12:00:00Z",
        "updated": "2026-03-30T12:00:00Z",
        "OS-EXT-STS:vm_state": "active",
        "OS-EXT-STS:power_state": 1,
        "OS-EXT-STS:task_state": None,
        "OS-EXT-SRV-ATTR:host": "compute1",
        "OS-EXT-SRV-ATTR:hypervisor_hostname": "compute1",
        "addresses": {
            "private": [
                {
                    "OS-EXT-IPS:type": "fixed",
                    "addr": "10.0.0.21",
                    "version": 4,
                }
            ]
        },
        "image": {"id": IMAGE_ID},
        "flavor": {"id": "m1.small"},
        "metadata": {},
    }


def nova_servers_doc(name: str | None = None) -> dict:
    server = mock_server_doc()
    if name and server["name"] != name:
        return {"servers": []}
    return {"servers": [server]}


def glance_versions_doc(host: str, keystone_port: int) -> dict:
    base = f"http://{host}:{keystone_port}/v2"
    return {
        "versions": [
            {
                "id": "v2.15",
                "status": "CURRENT",
                "links": [{"rel": "self", "href": base}],
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
                "visibility": "public",
                "disk_format": "qcow2",
                "container_format": "bare",
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
        "visibility": "public",
        "disk_format": "qcow2",
        "container_format": "bare",
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

        if path == "/v3":
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
            if server_id == SERVER_ID:
                self._send_json(200, {"server": mock_server_doc()})
                return
            self._send_json(404, {"error": {"message": f"Server not found: {server_id}"}})
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--keystone-port", type=int, default=5000)
    parser.add_argument("--nova-port", type=int, default=8774)
    args = parser.parse_args()

    MockOpenStackHandler.host = args.host
    MockOpenStackHandler.keystone_port = args.keystone_port
    MockOpenStackHandler.nova_port = args.nova_port

    server = ThreadingHTTPServer((args.host, args.keystone_port), MockOpenStackHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
