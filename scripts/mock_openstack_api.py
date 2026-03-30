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


def dashboard_data(host: str, keystone_port: int) -> dict:
    return {
        "environment": "Codespaces Mock OpenStack",
        "keystone_url": f"http://{host}:{keystone_port}/v3",
        "nova_url": f"http://{host}:{keystone_port}/v2.1",
        "token_expires_at": "2030-01-01T00:00:00Z",
        "services": nova_services_doc()["services"],
        "hypervisors": nova_hypervisors_doc()["hypervisors"],
    }


def dashboard_html(host: str, keystone_port: int) -> str:
    dashboard_url = f"http://{host}:{keystone_port}/dashboard-data"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mock Horizon Dashboard</title>
  <style>
    :root {{
      --bg: #f2efe8;
      --panel: rgba(255,255,255,0.82);
      --ink: #1f2a37;
      --muted: #617080;
      --line: rgba(31,42,55,0.12);
      --accent: #d06b2f;
      --accent-soft: #f4d9c8;
      --ok: #1c7c54;
      --warn: #a16207;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", "Noto Sans KR", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(208,107,47,0.16), transparent 35%),
        radial-gradient(circle at bottom right, rgba(28,124,84,0.12), transparent 30%),
        linear-gradient(135deg, #f7f3ea, #ebe4d8);
      min-height: 100vh;
    }}
    .wrap {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    .hero {{
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 28px;
      background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(250,242,233,0.86));
      box-shadow: 0 20px 60px rgba(55, 44, 29, 0.08);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(2rem, 5vw, 3.6rem);
      line-height: 0.96;
      letter-spacing: -0.04em;
    }}
    .subtitle {{
      margin: 0;
      color: var(--muted);
      max-width: 780px;
      font-size: 1rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 22px;
      padding: 18px;
      backdrop-filter: blur(8px);
    }}
    .eyebrow {{
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--muted);
      margin-bottom: 10px;
    }}
    .value {{
      font-size: 1.4rem;
      font-weight: 700;
    }}
    .status {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 12px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--ink);
      font-weight: 600;
    }}
    .status::before {{
      content: "";
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: var(--ok);
      box-shadow: 0 0 0 6px rgba(28,124,84,0.12);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }}
    th, td {{
      text-align: left;
      padding: 10px 0;
      border-bottom: 1px solid var(--line);
      font-size: 0.95rem;
    }}
    th {{
      color: var(--muted);
      font-weight: 600;
    }}
    .footer {{
      margin-top: 18px;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    code {{
      background: rgba(31,42,55,0.06);
      padding: 2px 6px;
      border-radius: 6px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <p class="eyebrow">Horizon-style View</p>
      <h1>Mock OpenStack Dashboard</h1>
      <p class="subtitle">Codespaces practice dashboard for lecture21 and lecture22. It reads mock Keystone and Nova state from the local training API and renders a browser-friendly status page.</p>
      <div class="grid">
        <div class="card">
          <div class="eyebrow">Environment</div>
          <div class="value" id="env-name">Loading...</div>
        </div>
        <div class="card">
          <div class="eyebrow">Keystone</div>
          <div class="status">Healthy</div>
          <div class="footer"><code id="keystone-url"></code></div>
        </div>
        <div class="card">
          <div class="eyebrow">Nova</div>
          <div class="status">Healthy</div>
          <div class="footer"><code id="nova-url"></code></div>
        </div>
        <div class="card">
          <div class="eyebrow">Token Expires</div>
          <div class="value" id="token-expiry">Loading...</div>
        </div>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <div class="eyebrow">Nova Services</div>
        <table>
          <thead>
            <tr><th>Binary</th><th>Host</th><th>State</th><th>Status</th></tr>
          </thead>
          <tbody id="services-body"></tbody>
        </table>
      </div>
      <div class="card">
        <div class="eyebrow">Hypervisors</div>
        <table>
          <thead>
            <tr><th>Hostname</th><th>State</th><th>Status</th><th>vCPUs</th></tr>
          </thead>
          <tbody id="hypervisors-body"></tbody>
        </table>
      </div>
    </section>
  </div>
  <script>
    async function loadDashboard() {{
      const response = await fetch("{dashboard_url}");
      const data = await response.json();
      document.getElementById("env-name").textContent = data.environment;
      document.getElementById("keystone-url").textContent = data.keystone_url;
      document.getElementById("nova-url").textContent = data.nova_url;
      document.getElementById("token-expiry").textContent = data.token_expires_at;

      document.getElementById("services-body").innerHTML = data.services.map((item) => `
        <tr>
          <td>${{item.binary}}</td>
          <td>${{item.host}}</td>
          <td>${{item.state}}</td>
          <td>${{item.status}}</td>
        </tr>
      `).join("");

      document.getElementById("hypervisors-body").innerHTML = data.hypervisors.map((item) => `
        <tr>
          <td>${{item.hypervisor_hostname}}</td>
          <td>${{item.state}}</td>
          <td>${{item.status}}</td>
          <td>${{item.vcpus}}</td>
        </tr>
      `).join("");
    }}

    loadDashboard();
  </script>
</body>
</html>"""


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

        if self.path == "/dashboard-data":
            self._send_json(200, dashboard_data(self.host, self.keystone_port))
            return

        if self.path in ["/dashboard", "/horizon"]:
            self._send_html(200, dashboard_html(self.host, self.keystone_port))
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
