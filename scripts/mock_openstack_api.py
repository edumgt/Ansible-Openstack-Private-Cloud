#!/usr/bin/env python3
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


TOKEN_ID = "mock-token"


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
        if self.path in ["/healthz", "/"]:
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

        if self.path in ["/v2.1", "/v2.1/"]:
            self._send_json(200, nova_version_doc(self.host, self.nova_port))
            return

        if self.path in ["/v2.1/os-services", "/v2.1/os-services/"]:
            self._send_json(200, nova_services_doc())
            return

        if self.path in ["/v2.1/os-hypervisors/detail", "/v2.1/os-hypervisors/detail/", "/v2.1/os-hypervisors", "/v2.1/os-hypervisors/"]:
            self._send_json(200, nova_hypervisors_doc())
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
