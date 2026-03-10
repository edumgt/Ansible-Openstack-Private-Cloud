# Python Ansible Playbook: Ansible-First 45 Lecture Curriculum

이 저장소는 **Ansible를 먼저 익히고**, 이후 Docker, k3s, AWS/OpenStack 개념으로 확장하는 실습형 학습 저장소입니다.

핵심은 다음 3가지입니다.

- `lecture01~lecture45`까지 단계형 커리큘럼
- 각 강의 폴더에 `lecture.yml` + `playbook.yml` 제공
- AI 보조 프롬프트를 활용한 실습/회고 루프

## 1. 학습 목표

- 반복되는 서버 작업을 Ansible Playbook으로 자동화한다.
- Docker/k3s/AWS 실습을 Ansible 기반 운영 관점으로 연결한다.
- YAML 문서 중심으로 설치/검증/회고를 일관되게 진행한다.

## 2. 저장소 구조

```text
Python_Ansible-Playbook/
├── README.md
├── ansible.cfg
├── requirements.txt
├── requirements.yml
├── inventories/
│   ├── local/
│   ├── dev/
│   ├── stage/
│   ├── prod/
│   └── aws/
├── group_vars/
├── playbooks/
│   ├── 00_ping.yml
│   ├── 00_bootstrap.yml
│   ├── 01_users.yml
│   ├── 02_nginx.yml
│   ├── 03_role_web.yml
│   ├── 10_docker_install.yml
│   ├── 10_docker_engine_install.yml
│   ├── 11_docker_run_nginx.yml
│   ├── 11_deploy_stack.yml
│   ├── 12_deploy_stack_rolling.yml
│   ├── 13_blue_green_switch.yml
│   ├── 20_aws_provision_ssm_no_ssh.yml
│   ├── 20_aws_create_vpc.yml
│   ├── 21_aws_create_ec2.yml
│   ├── 21_post_provision_via_ssm.yml
│   ├── 22_aws_s3_bucket.yml
│   ├── 23_aws_cleanup.yml
│   ├── 91_trivy_scan.yml
│   ├── 92_docker_bench.yml
│   ├── 93_crowdsec_nginx_lab.yml
│   └── learning/
├── roles/
├── stacks/
├── docs/
└── curriculum/
    ├── learning_path.yml
    ├── lecture01/
    │   ├── lecture.yml
    │   └── playbook.yml
    ├── ...
    └── lecture45/
        ├── lecture.yml
        └── playbook.yml
```

## 3. 커리큘럼 운영 원칙

- **Ansible 선행**: lecture01~25를 Ansible 중심으로 먼저 배치
- **YAML 중심**: 강의 정의/설치/실습은 `lecture.yml`에 명시
- **실행 파일 분리**: 강의 실행용 `playbook.yml`과 기존 레퍼런스 플레이북을 병행
- **AI 페어링**: 모든 강의에 `ai_pairing` 프롬프트 포함

## 4. 45강 모듈 구성

| Lecture Range | Module | Outcome |
|---|---|---|
| lecture01-lecture10 | Ansible Foundation | 인벤토리/변수/템플릿/Role 기반 자동화 기초 완성 |
| lecture11-lecture18 | Ansible Operations | 웹/컨테이너/보안 자동화 운영 패턴 습득 |
| lecture19-lecture25 | AWS Automation with Ansible | SSM/VPC/EC2/S3 생성과 정리 자동화 |
| lecture26-lecture32 | Infra & Docker Fundamentals | Linux/VirtualBox/Docker 실행 기반 이해 |
| lecture33-lecture38 | k3s & Kubernetes Operations | k3s 구조와 배포/관측 패턴 이해 |
| lecture39-lecture42 | Cloud Mapping | OpenStack/AWS 개념 매핑 |
| lecture43-lecture45 | Capstone | 통합 배포 리허설 + 운영 Runbook 완성 |

## 5. 강의별 파일 규칙

각 `curriculum/lectureNN/` 폴더는 아래 파일로 구성됩니다.

- `lecture.yml`: 학습 목표, 기술 스택, 설치 방안, AI 프롬프트, 참조 플레이북
- `playbook.yml`: 강의 실습용 Ansible Playbook

예시: `curriculum/lecture12/`

- `lecture.yml` → Docker Engine 설치 자동화 학습 설계
- `playbook.yml` → 강의용 설치/검증 태스크

## 6. 빠른 시작

### 6.1 의존성 설치

```bash
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
```

### 6.2 첫 강의 실행

```bash
ansible-playbook -i inventories/local/hosts.ini curriculum/lecture01/playbook.yml
```

실제 설치까지 수행하려면:

```bash
ansible-playbook -i inventories/local/hosts.ini curriculum/lecture01/playbook.yml -e install_enabled=true
```

### 6.3 강의 레퍼런스 플레이북 실행

각 강의의 `lecture.yml -> ansible_lab.reference_playbook` 경로를 사용합니다.

```bash
ansible-playbook -i inventories/local/hosts.ini playbooks/00_ping.yml
```

## 7. 전체 학습 진행 방법

1. `curriculum/learning_path.yml`에서 강의 순서 확인
2. `curriculum/lectureNN/lecture.yml`로 목표/설치/검증 기준 확인
3. `curriculum/lectureNN/playbook.yml` 실행
4. `ai_pairing` 프롬프트로 트러블슈팅/회고 정리
5. 필요 시 `reference_playbook` 실행으로 실전 플레이북과 연결

## 8. 45개 Lecture 목록

### Module A: Ansible Foundation (01-10)

- lecture01: Ansible 학습환경 진단과 컨트롤 노드 준비
- lecture02: Inventory 구조와 host/group 변수 설계
- lecture03: Ad-hoc 명령과 연결 테스트 자동화
- lecture04: 변수, facts, register 실습
- lecture05: loop, when, block 제어문 실습
- lecture06: Jinja2 템플릿과 설정 파일 생성
- lecture07: handler와 idempotency 검증
- lecture08: Role 구조 분해와 재사용 설계
- lecture09: 공통 서버 부트스트랩 자동화
- lecture10: 사용자/권한/SSH 정책 자동화

### Module B: Ansible Operations (11-18)

- lecture11: Nginx 설치와 웹 서비스 배포 자동화
- lecture12: Docker Engine 설치 자동화
- lecture13: Compose 스택 배포 자동화
- lecture14: Rolling Update 배포 실습
- lecture15: Blue/Green 전환 자동화
- lecture16: Trivy 기반 컨테이너 취약점 점검
- lecture17: Docker Bench 점검과 보고서 자동화
- lecture18: CrowdSec + Nginx 보안 실습 자동화

### Module C: AWS Automation with Ansible (19-25)

- lecture19: AWS SSM 기반 무SSH 프로비저닝
- lecture20: AWS VPC 네트워크 생성 자동화
- lecture21: AWS EC2 인스턴스 생성 자동화
- lecture22: 생성 후 SSM 기반 후속 설정 자동화
- lecture23: S3 버킷 생성/정책 자동화
- lecture24: AWS 출력값 수집과 결과 정리
- lecture25: AWS 실습 자원 정리 자동화

### Module D: Infra & Docker Fundamentals (26-32)

- lecture26: Linux 운영 기본기: 프로세스/로그/서비스
- lecture27: VirtualBox 네트워크: NAT/Host-only/Bridged
- lecture28: Docker 기초: 이미지/컨테이너/레지스트리
- lecture29: 백엔드 컨테이너 실행 흐름 이해
- lecture30: 프론트엔드 정적 배포와 Nginx 연동
- lecture31: Docker 네트워크/볼륨/데이터 영속성
- lecture32: 멀티서비스 Compose 운영 패턴

### Module E: k3s & Kubernetes Operations (33-38)

- lecture33: k3s 아키텍처와 Kubernetes 핵심 리소스
- lecture34: k3s 서버 노드 준비 자동화 설계
- lecture35: k3s 에이전트 조인 자동화 설계
- lecture36: Deployment/Service 선언형 배포 실습
- lecture37: Ingress와 외부 트래픽 라우팅
- lecture38: 클러스터 로그/상태 관측 기초

### Module F: Cloud Mapping (39-42)

- lecture39: OpenStack Neutron 네트워크 개념 매핑
- lecture40: Horizon 콘솔 운영 흐름과 IAM 관점
- lecture41: 로컬 실습과 AWS EC2/VPC/SG 매핑
- lecture42: ECR/ECS/EKS/IaC 확장 전략 수립

### Module G: Capstone (43-45)

- lecture43: 통합 아키텍처 설계 워크숍
- lecture44: 통합 배포 리허설과 장애 대응
- lecture45: 최종 캡스톤: 운영 Runbook 완성

## 9. 검증 체크 명령

```bash
find curriculum -maxdepth 1 -type d -name 'lecture*' | wc -l
find curriculum -maxdepth 2 -type f -name 'lecture.yml' | wc -l
find curriculum -maxdepth 2 -type f -name 'playbook.yml' | wc -l
```

기대값은 각각 `45`, `45`, `45`입니다.

---

## 12. 추가 확장 학습 트랙 (45강 반영)

기본 45강 이후 실무형으로 확장하기 위한 선택 심화 트랙입니다.  
이번 개편에서는 아래 8개 트랙을 `curriculum/advanced_tracks.yml`로 정의했고, 모든 `lecture.yml`에 `advanced_integration` 필드를 추가해 각 강의와 연결했습니다.

### 12-1. Docker Compose 추가

#### 학습 목적
- 여러 컨테이너를 하나의 스택으로 실행
- backend/frontend/postgres/redis 통합 환경 구성
- ECS/Kubernetes 멀티서비스 배포 개념으로 확장

#### 학습 내용
- `docker compose` 구조
- `services`, `ports`, `volumes`, `environment`, `depends_on`
- 멀티컨테이너 애플리케이션 구성
- `.env` 기반 설정 분리

#### 실습 예시
- frontend + backend + postgres + redis 구성
- `docker-compose.yml` 작성, 일괄 기동/중지
- 서비스 간 네트워크/의존성 확인

#### 개발자 관점
- 백엔드: API + DB + Redis 통합 실행 구조 이해
- 프론트엔드: 정적 웹 + API + 인증/세션 백엔드 연결 구조 이해

#### AWS 연결 포인트
- Compose는 ECS Task 정의 또는 Kubernetes 다중 리소스 분리 전 단계
- Compose 네트워크는 서비스 내부 통신 모델 학습에 유효
- Compose 볼륨은 영속 저장소 개념 학습에 유효

#### 45강 연계
- `lecture02`, `lecture09`, `lecture12`, `lecture13`, `lecture14`, `lecture28`, `lecture32`

---

### 12-2. Helm Chart 추가

#### 학습 목적
- Kubernetes 리소스를 패키지처럼 배포
- 환경별 설정(dev/stage/prod)을 values 파일로 분리

#### 학습 내용
- Helm 개념
- Chart 구조
- `templates/`, `values.yaml`, `Chart.yaml`
- 반복 YAML 템플릿화 및 환경별 값 분리

#### 실습 예시
- backend/frontend Helm Chart 작성
- `values-dev.yaml`, `values-prod.yaml` 분리
- replica/image tag/environment 변경 실습

#### 개발자 관점
- 백엔드: DB 연결정보, replica, tag 버전 관리
- 프론트엔드: API endpoint, ingress host, static 설정 관리

#### AWS 연결 포인트
- Helm은 EKS 실무 운영에서 핵심 배포 도구
- GitOps/Argo CD/배포 표준화와 자연스럽게 연결 가능

#### 45강 연계
- `lecture06`, `lecture36`, `lecture37`, `lecture44`

---

### 12-3. GitHub Actions 기반 CI 추가

#### 학습 목적
- 코드 변경 후 테스트/이미지 빌드/배포 준비 자동화
- Git 기반 협업 + 배포 자동화 흐름 이해

#### 학습 내용
- GitHub Actions 구조(workflow/job/step)
- 테스트 자동화
- Docker image build 자동화
- artifact/registry push 개념

#### 실습 예시
- backend push 시 테스트 실행
- Docker image build + tag 자동화
- 추후 ECR push 확장 가능한 workflow 설계

#### 개발자 관점
- 백엔드: merge 시 자동 테스트/빌드 파이프라인 이해
- 프론트엔드: 빌드 결과물 생성/배포 자동화 이해

#### AWS 연결 포인트
- GitHub Actions -> ECR -> ECS/EKS 배포로 확장
- CodeBuild/CodePipeline/Argo CD와 비교 가능

#### 45강 연계
- `lecture01`, `lecture08`, `lecture19`, `lecture22`, `lecture24`, `lecture43`

---

### 12-4. Nginx reverse proxy 심화

#### 학습 목적
- reverse proxy 역할 이해
- frontend/backend/API 라우팅 구조를 실무 관점으로 학습

#### 학습 내용
- upstream 설정
- location 기반 라우팅
- 정적 파일/캐시/gzip/header 설정
- CORS/TLS 종료 기초

#### 실습 예시
- `/` -> frontend, `/api` -> backend
- 정적 리소스 캐싱
- 보안 헤더/에러 페이지 추가

#### 개발자 관점
- 백엔드: API 서버를 직접 노출하지 않는 운영 이유 이해
- 프론트엔드: SPA 라우팅/정적 캐싱/API 프록시 구조 이해

#### AWS 연결 포인트
- ALB + Nginx + Ingress Controller 구조 이해 기반
- Ingress/CloudFront/API Gateway 개념으로 확장

#### 45강 연계
- `lecture05`, `lecture10`, `lecture11`, `lecture15`, `lecture30`

---

### 12-5. PostgreSQL / Redis 추가

#### 학습 목적
- 상태 저장 계층 포함 서비스 아키텍처 이해
- DB/캐시가 컨테이너/쿠버네티스에서 연결되는 방식 체감

#### 학습 내용
- PostgreSQL 역할
- Redis 역할
- 영속/휘발 데이터 차이
- DB connection string, 세션/캐시/큐 기초

#### 실습 예시
- backend PostgreSQL 연동
- Redis 캐시 또는 rate limit 예제
- volume 영속화, 재시작 후 데이터 유지 확인

#### 개발자 관점
- 백엔드: ORM/SQL, 캐시 계층, 세션 저장 구조 이해
- 프론트엔드: 응답속도와 캐시 효과 차이 체감

#### AWS 연결 포인트
- PostgreSQL = RDS/Aurora 이해 기반
- Redis = ElastiCache 이해 기반
- Local volume = 영속 데이터 저장 개념 학습 기반

#### 45강 연계
- `lecture04`, `lecture23`, `lecture29`, `lecture31`

---

### 12-6. 모니터링(Prometheus/Grafana) 추가

#### 학습 목적
- 상태 관찰/문제 탐지 중심의 운영 관점 강화
- 메트릭/대시보드/알림 필요성 이해

#### 학습 내용
- Observability 기초
- Prometheus scrape 구조
- Grafana dashboard 기초
- CPU/Memory/Request/Error Rate 관찰

#### 실습 예시
- k3s에 Prometheus/Grafana 배포
- backend 메트릭 노출
- 응답시간/에러율/노드 리소스 시각화

#### 개발자 관점
- 백엔드: API 응답속도/에러율/리소스 사용률 분석
- 프론트엔드: 성능 저하 시 백엔드 상태 진단 흐름 이해

#### AWS 연결 포인트
- CloudWatch, Managed Prometheus, Managed Grafana로 연결 가능
- 운영 가시화/장애대응/알람 설계로 확장 가능

#### 45강 연계
- `lecture03`, `lecture07`, `lecture16`, `lecture17`, `lecture18`, `lecture25`, `lecture38`, `lecture45`

---

### 12-7. OpenStack DevStack 또는 MicroStack 연계

#### 학습 목적
- Docker/k3s/Ansible 실습에 OpenStack 체험을 결합
- AWS 입문 전 IaaS 계층 이해 강화

#### 학습 내용
- DevStack/MicroStack 개념
- VM/이미지/네트워크/프로젝트/콘솔
- Neutron/Horizon 실환경 매핑

#### 실습 예시
- 단일 노드 DevStack 또는 MicroStack
- 이미지 등록, 네트워크/인스턴스 생성, Floating IP 연결
- Horizon 로그인/리소스 확인

#### 개발자 관점
- 백엔드: VM/컨테이너 차이와 인프라 계층 이해
- 프론트엔드: 콘솔 기반 리소스 관리 흐름 시각적 이해

#### AWS 연결 포인트
- OpenStack은 EC2/VPC/EBS 개념 학습을 돕는 로컬 모델
- Horizon은 AWS Console 유사 운영 경험
- Neutron은 VPC/Subnet/Public IP/SG 이해 강화

#### 45강 연계
- `lecture20`, `lecture27`, `lecture39`, `lecture40`, `lecture41`

---

### 12-8. k3s 대신 kubeadm 또는 managed EKS 확장 비교

#### 학습 목적
- k3s/kubeadm/EKS 차이 이해
- 실습 환경과 운영 환경의 책임 경계 비교

#### 학습 내용
- k3s 장점/한계
- kubeadm 구조
- EKS 운영 모델
- control plane 관리 주체/난이도/비용 비교

#### 비교 포인트

| 구분 | k3s | kubeadm | Amazon EKS |
|---|---|---|---|
| 목적 | 경량 실습/엣지/소규모 | 표준 쿠버네티스 직접 구축 | 관리형 쿠버네티스 |
| 설치 난이도 | 낮음 | 높음 | 중간 |
| 운영 부담 | 낮음 | 높음 | control plane 부담 낮음 |
| 학습 적합성 | 매우 좋음 | 깊이 있는 학습에 좋음 | AWS 실무 연결에 좋음 |
| 관리 주체 | 사용자 | 사용자 | AWS + 사용자 |
| 비용 | 로컬 자원 중심 | 로컬/추가 인프라 필요 | AWS 비용 발생 |

#### 실습 예시
- 동일 앱 k3s 배포
- kubeadm 설치 흐름 비교
- EKS 전환 시 AWS 관리 영역/사용자 관리 영역 정리

#### 개발자 관점
- 백엔드: 내가 관리할 운영 범위 경계 이해
- 프론트엔드: 배포 대상 변화와 운영 책임 변화 이해

#### AWS 연결 포인트
- k3s: 쿠버네티스 개념 학습용
- kubeadm: 내부 구조 심화용
- EKS: AWS 실무 운영 연결용

#### 45강 연계
- `lecture21`, `lecture33`, `lecture34`, `lecture35`, `lecture42`

---

## 13. 심화 확장 추천 순서

기본 과정을 끝낸 뒤 권장 확장 순서는 아래와 같습니다.

1. Docker Compose
2. PostgreSQL / Redis
3. Nginx reverse proxy 심화
4. GitHub Actions 기반 CI
5. Helm Chart
6. Prometheus / Grafana
7. OpenStack DevStack 또는 MicroStack
8. kubeadm / EKS 비교

위 순서는 개발자가 빠르게 실무 감각을 얻는 흐름 기준이며, `curriculum/advanced_tracks.yml`의 `recommended_order`에도 반영되어 있습니다.

---

## 14. 최종 확장 목표

기본 45강 + 심화 확장을 완료하면 다음 수준까지 도달할 수 있습니다.

- 단일 서버를 넘어 멀티서비스 아키텍처를 설계/설명할 수 있다.
- 로컬 컨테이너 환경과 쿠버네티스 환경의 차이를 설명할 수 있다.
- 네트워크/프록시/DB/캐시/모니터링/자동화를 포함한 전체 서비스 구조를 이해한다.
- AWS EC2, RDS, ElastiCache, ALB, ECR, ECS, EKS, CloudWatch 역할을 연결해 설명할 수 있다.

즉, 이 과정은 단순 실습이 아니라 **개발자가 AWS를 기술적으로 이해하고 실무형 인프라 감각을 갖추기 위한 프로젝트형 브릿지 과정**을 목표로 합니다.
