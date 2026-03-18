# 폐쇄망(Air-Gapped) 환경 배포 가이드

이 문서는 인터넷에 연결되지 않는 **폐쇄망(Air-Gapped/Isolated Network)** 환경에서
`ansible-openstack-lab` OVA 이미지를 사용할 때 필요한 구성 사항을 정리합니다.

---

## 1. 폐쇄망 환경의 주요 제약

| 항목 | 폐쇄망 영향 |
|---|---|
| Ubuntu APT 패키지 저장소 | 외부 접근 불가 → 로컬 미러 또는 오프라인 패키지 필요 |
| PyPI (pip) | 외부 접근 불가 → 오프라인 wheel 캐시 필요 |
| Ansible Galaxy | 외부 접근 불가 → 오프라인 컬렉션 tarball 필요 |
| Docker Hub / ghcr.io | 외부 접근 불가 → 로컬 레지스트리 필요 |
| DNS | 공용 DNS 사용 불가 → 내부 DNS 서버 설정 필요 |
| NTP | 외부 NTP 서버 접근 불가 → 내부 NTP 서버 설정 필요 |

---

## 2. OVA 이미지에 포함된 오프라인 리소스

Packer 빌드 과정(`packer/scripts/post_copy.sh`)에서 아래 리소스가
**OVA 내부에 미리 번들**됩니다.

```
/opt/ansible-openstack/
├── offline/
│   ├── pip-wheels/        ← pip 패키지 wheel (.whl) 파일
│   └── collections/       ← ansible-galaxy 컬렉션 (amazon.aws, community.docker, community.general)
```

---

## 3. 폐쇄망 구성 항목별 세부 설명

### 3.1 APT 패키지 저장소 (Ubuntu)

OVA 이미지에는 이미 필요한 시스템 패키지가 설치되어 있습니다.
추가 패키지 설치가 필요한 경우 내부 APT 미러를 구성하세요.

```bash
# /etc/apt/sources.list 예시 (내부 미러 사용)
deb http://<내부-미러-IP>/ubuntu jammy main restricted universe multiverse
deb http://<내부-미러-IP>/ubuntu jammy-updates main restricted universe multiverse
deb http://<내부-미러-IP>/ubuntu jammy-security main restricted universe multiverse
```

내부 APT 미러 구축 방법:
```bash
# apt-mirror 또는 aptly 활용
sudo apt-get install apt-mirror
# /etc/apt/mirror.list 설정 후
sudo apt-mirror
# nginx / apache로 /var/spool/apt-mirror/mirror/ 서비스
```

### 3.2 pip (Python 패키지)

OVA 내 번들된 wheel을 이용해 오프라인 설치:
```bash
# VM 내부에서 실행
WHEEL_DIR=/opt/ansible-openstack/offline/pip-wheels

pip install --no-index --find-links="${WHEEL_DIR}" ansible-core ansible-lint boto3 botocore openstacksdk
```

추가 패키지가 필요한 경우 인터넷이 연결된 머신에서 다운로드 후 전송:
```bash
# 인터넷 연결 머신에서
pip download <패키지명> -d /tmp/wheels/
# SCP, USB 등으로 VM에 전송
scp -r /tmp/wheels/ ansible@<VM-IP>:/opt/ansible-openstack/offline/pip-wheels/
```

내부 PyPI 미러 구축 (선택):
```bash
# pip install devpi-server 또는 pypiserver 활용
pip install pypiserver
pypi-server run -p 8080 /opt/ansible-openstack/offline/pip-wheels/

# 클라이언트 설정
pip install --index-url http://<내부-서버-IP>:8080/simple/ <패키지명>
```

### 3.3 Ansible Galaxy 컬렉션

OVA 내 번들된 컬렉션 사용:
```bash
# VM 내부에서 실행
COLLECTIONS_PATH=/opt/ansible-openstack/offline/collections
export ANSIBLE_COLLECTIONS_PATHS="${COLLECTIONS_PATH}:~/.ansible/collections"

# 또는 ansible.cfg에 설정
# [defaults]
# collections_path = /opt/ansible-openstack/offline/collections
```

추가 컬렉션이 필요한 경우:
```bash
# 인터넷 연결 머신에서 tarball 다운로드
ansible-galaxy collection download <namespace.name> -p /tmp/collections/
# 전송 후 오프라인 설치
ansible-galaxy collection install /tmp/collections/<namespace-name-version>.tar.gz \
    -p /opt/ansible-openstack/offline/collections/
```

### 3.4 Docker (컨테이너 이미지)

내부 레지스트리 구성:
```bash
# 내부 레지스트리 서버에서 (Docker 설치 후)
docker run -d -p 5000:5000 --restart always \
  -v /opt/registry:/var/lib/registry \
  --name registry registry:2

# 이미지 미러링 (인터넷 연결 머신에서)
docker pull nginx:latest
docker tag nginx:latest <내부-레지스트리-IP>:5000/nginx:latest
docker push <내부-레지스트리-IP>:5000/nginx:latest
```

Docker 데몬에 내부 레지스트리 설정 (`/etc/docker/daemon.json`):
```json
{
  "insecure-registries": ["<내부-레지스트리-IP>:5000"],
  "registry-mirrors": ["http://<내부-레지스트리-IP>:5000"]
}
```

Ansible playbook에서 내부 레지스트리 사용:
```yaml
# ansible/group_vars/all.yml 또는 해당 playbook vars
docker_registry: "<내부-레지스트리-IP>:5000"
```

### 3.5 DNS 설정

내부 DNS 서버를 사용하도록 `/etc/resolv.conf` 수정:
```bash
# /etc/resolv.conf
nameserver <내부-DNS-IP>
search <내부-도메인>
```

Netplan을 통한 영구 설정 (`/etc/netplan/00-installer-config.yaml`):
```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: false
      addresses: [<VM-IP>/24]
      gateway4: <게이트웨이-IP>
      nameservers:
        addresses: [<내부-DNS-IP>]
        search: [<내부-도메인>]
```

```bash
sudo netplan apply
```

### 3.6 NTP (시간 동기화)

내부 NTP 서버 설정 (`/etc/systemd/timesyncd.conf`):
```ini
[Time]
NTP=<내부-NTP-IP>
FallbackNTP=<백업-NTP-IP>
```

```bash
sudo systemctl restart systemd-timesyncd
timedatectl status
```

### 3.7 OpenStack 서비스 엔드포인트

Kolla-Ansible 또는 기존 OpenStack 클러스터가 폐쇄망에 있는 경우
`ansible/group_vars/` 또는 `clouds.yaml`에 내부 엔드포인트를 설정합니다.

```yaml
# ~/.config/openstack/clouds.yaml
clouds:
  mycloud:
    auth:
      auth_url: http://<내부-OpenStack-IP>:5000/v3
      username: admin
      password: <password>
      project_name: admin
      user_domain_name: Default
      project_domain_name: Default
    region_name: RegionOne
    interface: internal
    identity_api_version: 3
```

---

## 4. 폐쇄망 환경 점검 체크리스트

배포 전 아래 항목을 점검하세요.

| # | 항목 | 확인 방법 | 상태 |
|---|---|---|---|
| 1 | VM IP / 게이트웨이 설정 | `ip addr; ip route` | ☐ |
| 2 | 내부 DNS 응답 확인 | `nslookup <내부-호스트> <DNS-IP>` | ☐ |
| 3 | NTP 동기화 확인 | `timedatectl` | ☐ |
| 4 | pip 오프라인 설치 테스트 | `pip install --no-index --find-links=/opt/ansible-openstack/offline/pip-wheels ansible-core` | ☐ |
| 5 | Ansible Galaxy 컬렉션 경로 확인 | `ansible-galaxy collection list` | ☐ |
| 6 | Ansible ping 확인 | `ansible all -i ansible/inventories/local/hosts.ini -m ping` | ☐ |
| 7 | Docker 내부 레지스트리 pull 테스트 | `docker pull <내부-레지스트리-IP>:5000/nginx:latest` | ☐ |
| 8 | OpenStack API 엔드포인트 응답 | `openstack endpoint list` | ☐ |

---

## 5. 환경 변수 / 설정 파일 요약

| 파일 | 주요 설정 항목 |
|---|---|
| `/etc/apt/sources.list` | APT 저장소 → 내부 미러 URL |
| `/etc/resolv.conf` | nameserver → 내부 DNS IP |
| `/etc/systemd/timesyncd.conf` | NTP → 내부 NTP IP |
| `/etc/docker/daemon.json` | registry-mirrors, insecure-registries |
| `~/.config/openstack/clouds.yaml` | OpenStack 내부 엔드포인트 |
| `ansible/group_vars/all.yml` | docker_registry, openstack vars |
| `ansible.cfg` | collections_path (오프라인 경로) |

---

## 6. 참고 자료

- [Ubuntu APT Mirror 구성](https://help.ubuntu.com/community/AptGet/Offline/Repository)
- [pip 오프라인 설치](https://pip.pypa.io/en/stable/topics/repeatable-installs/)
- [Ansible Galaxy 오프라인](https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-collections-from-a-tar-gz-file)
- [Docker Private Registry](https://docs.docker.com/registry/deploying/)
- [Kolla-Ansible Air-Gapped](https://docs.openstack.org/kolla-ansible/latest/admin/advanced-configuration.html)
