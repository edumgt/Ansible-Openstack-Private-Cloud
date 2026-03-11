# Python Ansible Playbook: 20강 압축 커리큘럼

이 저장소는 Ansible 자동화 학습을 20개 강의로 압축해, 실습 중심으로 빠르게 완주할 수 있도록 재구성한 프로젝트입니다.

이번 개편에서 다음을 반영했습니다.
- 루트 문서(`study_plan.md`, `기술스택.md`)의 핵심 내용을 `README.md`로 병합
- 기존 45강 구조를 20강으로 함축
- 강의 폴더를 `curriculum/` 하위가 아닌 **프로젝트 메인 폴더**로 이동 (`lecture01~lecture20`)
- Ansible 기준 `Cloud Bridge` 구간을 메인 로드맵에서 제외하고 OpenStack 중심으로 재배치
- 강의별 실행 절차와 검증 기준을 표준화

## 1. 학습 목표
- Ansible 플레이북 작성/실행/검증 루틴을 익힌다.
- 인벤토리, 변수, 템플릿, Role을 재사용 가능한 형태로 설계한다.
- 서비스 운영 자동화(Nginx, Docker)를 안정적으로 수행한다.
- OpenStack 핵심 컴포넌트(Keystone/Glance/Nova/Neutron/Cinder) 운영 흐름을 Ansible 관점으로 이해한다.
- 마지막 강의에서 운영 Runbook을 완성해 재현 가능한 실습 체계를 만든다.

## 2. 통합 기술 스택 가이드
### 핵심 스택
- `ansible-core`, `yaml`, `python3`, `linux`, `openstack`

### 보조 스택
- `docker`, `nginx`, `awscli`, `az` (비교 학습 목적)

### OpenStack 컴포넌트 정리 (기술스택 문서 병합 요약)
- `Keystone`: 인증/권한/서비스 카탈로그 (Python)
- `Glance`: VM 이미지 관리 (Python)
- `Nova`: 인스턴스 생성/스케줄링/컴퓨트 제어 (Python)
- `Neutron`: 네트워크/서브넷/라우터/FIP 제어 (Python)
- `Cinder`: 블록 스토리지 볼륨/스냅샷 관리 (Python)
- `Horizon`: Django 기반 웹 대시보드 (Python + HTML/CSS/JS)

## 3. 20강 로드맵
| Lecture | 모듈 | 주제 |
|---|---|---|
| lecture01 | Ansible Foundation | Ansible 학습환경 점검과 실행 루틴 정립 |
| lecture02 | Ansible Foundation | Inventory/Variables 구조 설계 |
| lecture03 | Ansible Foundation | Ad-hoc 명령과 Facts 수집 자동화 |
| lecture04 | Ansible Foundation | Jinja2 템플릿과 Handler 실전 |
| lecture05 | Ansible Foundation | Role 분리와 재사용 설계 |
| lecture06 | Ansible Foundation | Idempotency와 검증 자동화 |
| lecture07 | Ansible Operations | 사용자/권한/SSH 정책 자동화 |
| lecture08 | Ansible Operations | Nginx 서비스 배포와 검증 |
| lecture09 | Ansible Operations | Docker Engine 설치 자동화 |
| lecture10 | Ansible Operations | Compose 배포와 업데이트 전략 |
| lecture11 | OpenStack Foundation | OpenStack CLI 환경 구성과 인증 토큰 흐름 |
| lecture12 | OpenStack Foundation | OpenStack 프로젝트/네트워크 리소스 자동화 기초 |
| lecture13 | OpenStack Foundation | OpenStack 아키텍처와 핵심 서비스 이해 |
| lecture14 | OpenStack Foundation | Keystone 인증/프로젝트/역할 모델 |
| lecture15 | OpenStack Foundation | Glance 이미지 관리 자동화 |
| lecture16 | OpenStack Foundation | Nova 인스턴스 라이프사이클 자동화 |
| lecture17 | OpenStack Foundation | Neutron/Cinder 리소스 자동화 |
| lecture18 | OpenStack Operations | Horizon 운영 점검과 로그 수집 |
| lecture19 | OpenStack Operations | Kolla Ansible 배포 준비와 검증 |
| lecture20 | OpenStack Operations | 종합 캡스톤: OpenStack 운영 Runbook 완성 |

## 4. 주차별 학습 계획 (압축판)
- Week 1: `lecture01~05` (기초 문법/구조)
- Week 2: `lecture06~10` (운영 자동화)
- Week 3: `lecture11~15` (OpenStack Foundation)
- Week 4: `lecture16~20` (OpenStack 운영/캡스톤)

권장 학습 시간: 강의당 60~90분

## 5. 실행 방법 (상세)
### 5.1 사전 준비
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install ansible-core
ansible --version
```

### 5.2 강의 실행 템플릿
```bash
# 기본 실행 (설치 태스크 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lectureNN/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lectureNN/playbook.yml -e install_enabled=true
```

### 5.3 예시 (lecture01)
```bash
ansible-playbook -i ansible/inventories/local/hosts.ini lecture01/playbook.yml -e install_enabled=false
ansible-playbook -i ansible/inventories/local/hosts.ini lecture01/playbook.yml -e install_enabled=true
```

### 5.4 레퍼런스 플레이북 실행
각 강의의 `lecture.yml`에 있는 `ansible_lab.reference_playbook`을 참고해 아래처럼 실행합니다.
```bash
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/00_ping.yml
```

## 6. 결과 검증 체크리스트
강의마다 아래 4가지를 남기면 재현성이 높아집니다.
- 실행 로그 1개
- 핵심 태스크 성공/실패 원인 정리 1개
- 개선 포인트 1개
- 다음 강의 연결 메모 1개

## 7. 프로젝트 구조 (개편 후)
```text
Python_Ansible-Playbook/
├── README.md
├── lecture01/
├── lecture02/
├── ...
├── lecture20/
├── ansible/
│   ├── inventories/
│   ├── playbooks/
│   ├── roles/
│   ├── group_vars/
│   ├── files/
│   └── stacks/
├── docs/
│   └── reference/
├── scripts/
└── archive/
    └── legacy/
```

## 8. 운영 메모
- `install_enabled=true` 검증 시 OS 저장소 패키지명 차이로 실패할 수 있습니다.
- 클라우드 실습(OpenStack/AWS/Azure 비교)은 로컬 패키지 설치와 별도로 자격증명/네트워크가 필요합니다.
- 실패 로그를 남기고 `README`의 트러블슈팅 섹션과 함께 비교하면 학습 속도가 빨라집니다.

## 9. 클라우드 자동화 조합 설명 및 비교
### 9.1 조합 설명
- `OpenStack + Ansible`: 운영자가 원하는 상태를 playbook으로 선언하고, 여러 OpenStack 리소스를 반복 가능하게 표준화할 때 유리합니다.
- `AWS + aws cli`: AWS 서비스별 API를 즉시 호출해 빠르게 스크립트화하거나 CI에서 단일 작업을 제어할 때 유리합니다.
- `Azure + az`: Azure 리소스 그룹/구독 단위 운영을 CLI 중심으로 자동화하고 파이프라인과 연동할 때 유리합니다.

### 9.2 비교표
| 조합 | 자동화 방식 | 강점 | 약점 | 적합한 상황 |
|---|---|---|---|---|
| OpenStack + Ansible | 선언형(playbook, role) | 일관성, 재실행 안정성, 팀 표준화 | 초기 구조 설계 비용 | 사내 프라이빗 클라우드 운영 표준화 |
| AWS + aws cli | 명령형(스크립트/파이프라인) | 빠른 실험, 서비스 기능 접근 속도 | 스크립트가 커지면 유지보수 부담 | AWS 관리 작업의 빠른 자동화 |
| Azure + az | 명령형(스크립트/파이프라인) | 구독/리소스그룹 단위 관리가 직관적 | 대규모 반복 작업은 구조화 필요 | Azure 운영팀의 일상 작업 자동화 |

### 9.3 최소 예시 명령
```bash
# OpenStack + Ansible
ansible-playbook -i ansible/inventories/local/hosts.ini lecture13/playbook.yml -e install_enabled=false

# AWS + aws cli
aws ec2 describe-instances --region ap-northeast-2

# Azure + az
az vm list -o table
```

## 10. GitHub Actions: Docker Hub Push + Local Docker Sync
### 10.1 추가된 파일
- `.github/workflows/docker-publish.yml`
- `Dockerfile`
- `.dockerignore`
- `scripts/sync_local_docker.sh`

### 10.2 GitHub Secrets (필수)
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` (Docker Hub Access Token)

### 10.3 GitHub Variables (선택)
- `DOCKERHUB_REPOSITORY`: 미설정 시 `python-ansible-playbook`
- `ENABLE_LOCAL_DOCKER_SYNC`: `true`일 때 self-hosted runner에서 local docker 반영
- `LOCAL_DOCKER_CONTAINER_NAME`: 미설정 시 `python-ansible-playbook`
- `LOCAL_DOCKER_RUN_CMD`: 미설정 시 `tail -f /dev/null`

### 10.4 동작 방식
1. `main` 브랜치 push(또는 수동 실행) 시 Docker 이미지를 빌드해 Docker Hub로 push
2. `ENABLE_LOCAL_DOCKER_SYNC=true`이고 self-hosted runner(`self-hosted`, `linux`, `docker`)가 있으면
   같은 워크플로우에서 최신 이미지를 pull하고 로컬 컨테이너를 재기동

### 10.5 수동 로컬 반영 (원할 때 직접 실행)
```bash
IMAGE=docker.io/<dockerhub-user>/<repo>:latest \
CONTAINER_NAME=python-ansible-playbook \
./scripts/sync_local_docker.sh
```
