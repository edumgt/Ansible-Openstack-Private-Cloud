# lecture20 - AWS VPC 네트워크 생성 자동화

## 1. 강의 개요
- 강의 번호: `20`
- 모듈: `Module C / AWS Automation with Ansible`
- 난이도: `intermediate`
- 권장 시간: `60분`
- 모듈 초점: Ansible로 AWS 리소스를 생성/검증/정리하는 흐름을 익힙니다.

## 2. 선수 조건
- lecture19 완료 또는 동등한 실무 경험
- Linux 기본 명령어(ls, cat, systemctl) 사용 가능

## 3. 학습 목표
- AWS VPC 네트워크 생성 자동화 주제를 Ansible 중심으로 설명할 수 있다.
- 강의별 설치 및 점검 절차를 YAML 문서 기반으로 수행할 수 있다.
- 실습 결과를 AI 코치 프롬프트로 리뷰하고 개선할 수 있다.

## 4. 기술 스택 반영
### 핵심 스택 (Primary)
- `ansible-core`
- `awscli`
- `boto3`
- `ssm`

### 보조 스택 (Secondary)
- (해당 없음)

### 선택 스택
- `terraform`
- `session-manager-plugin`

### 적용 원칙
- 핵심 스택(Ansible/OpenStack/YAML) 중심으로 진행하며, 모든 작업은 재현 가능한 자동화 절차로 정리합니다.

## 5. 학습 흐름
- 오프닝 5분: 목표와 검증 기준 확인
- 핵심 작업 45분: 플레이북 실행, 결과 점검, 오류 수정
- 마무리 10분: 실행 로그 정리와 다음 강의 연결

## 6. 설치 계획
- 대상 인벤토리: `../../inventories/local/hosts.ini`
- 대상 호스트 그룹: `aws`
### 설치 접근
- 사전 점검: Python/SSH/권한 확인
- 필수 패키지 설치는 playbook.yml에서 install_enabled=true일 때 실행
- 강의 종료 후 상태 점검 태스크로 검증
### 패키지
- `python3`
- `python3-boto3`
- `python3-botocore`
- `awscli`
- `jq`

## 7. 실행 절차
- 강의 플레이북: `./playbook.yml`
- 레퍼런스 플레이북: `../../playbooks/20_aws_create_vpc.yml`
### 실행 명령
- `ansible-playbook -i ../../inventories/local/hosts.ini ./playbook.yml`
- `ansible-playbook -i ../../inventories/local/hosts.ini ./playbook.yml -e install_enabled=true`
- `ansible-playbook -i ../../inventories/local/hosts.ini ../../playbooks/20_aws_create_vpc.yml`

## 8. 산출물과 검증
### 산출물
- 강의 실행 로그 또는 스크린샷 1개 이상
- AI 회고 노트(markdown) 1개
### 검증 기준
- playbook syntax error 없음
- 핵심 태스크 결과를 debug 출력으로 확인

## 9. AI 페어링 가이드
- 사전 점검 프롬프트: AWS VPC 네트워크 생성 자동화 실습 전에 실패할 수 있는 지점 3개를 체크리스트로 만들어줘.
- 실습 중 프롬프트: 현재 실행 로그를 보고 원인-증상-조치 순서로 트러블슈팅 가이드를 작성해줘.
- 회고 프롬프트: 이번 강의에서 배운 자동화 패턴을 다음 강의에 재사용할 수 있게 YAML 템플릿으로 정리해줘.

## 10. 심화 연계 (선택)
- 연계 트랙: `OpenStack 입문 체험(MicroStack/DevStack/Kolla Ansible)`
- 연계 목표: AWS VPC 네트워크 생성 자동화 학습 결과를 OpenStack 입문 체험 순서(MicroStack -> DevStack -> Kolla Ansible)와 연결한다.
### 추가 실습
- MicroStack 단일 노드에서 Horizon에 접속해 Networks/Routers/Floating IPs를 확인
- DevStack과 Kolla Ansible에서 Neutron 네트워크 흐름을 비교하고 서비스 매핑
- AWS/OpenStack 브릿지: OpenStack Neutron 라우터/보안그룹/Floating IP 흐름을 AWS VPC/Route/SG/EIP와 비교한다.
- 확장 프롬프트: 현재 강의(AWS VPC 네트워크 생성 자동화) 결과를 MicroStack -> DevStack -> Kolla Ansible 순서로 확장하는 OpenStack 네트워크 실습 체크리스트를 YAML로 작성해줘.

## 11. 참고 파일
- `lecture.yml`: 강의 메타데이터
- `playbook.yml`: 강의 실행 플레이북


## 12. 실행 검증 결과 (자동 수집)
- 검증 일시: 자동 실행
- 실행 명령: `HOME=/home/Python_Ansible-Playbook ANSIBLE_LOCAL_TEMP=/home/Python_Ansible-Playbook/.ansible/tmp ANSIBLE_REMOTE_TEMP=/tmp/.ansible/tmp ANSIBLE_BECOME_ASK_PASS=False .venv/bin/ansible-playbook -i inventories/local/hosts.ini curriculum/lecture20/playbook.yml -e install_enabled=false`
- 검증 상태: `PASS` (exit_code=0)
- RECAP: `localhost : ok=4 changed=0 unreachable=0 failed=0 skipped=1 rescued=0 ignored=0`
- 올바른 예상 결과:
  - `Gathering Facts` 성공
  - `Show lecture context` 출력 확인
  - `Install lecture packages when enabled`는 `install_enabled=false` 기준으로 `skipped`
  - `Check Python3 availability`와 버전 출력 성공
- MCR 캡처 솔루션: `docker run --rm -v "$PWD":/work -w /work mcr.microsoft.com/devcontainers/python:3.12 bash -lc 'python3 -m pip install pillow && python3 scripts/render_captures.py'`
- 실행 로그: `results/lecture-verification/logs/lecture20.log`

![lecture20 실행 캡처](../../results/lecture-verification/captures/lecture20.png)


## 13. 실행 검증 결과 (install_enabled=true 자동 수집)
- 검증 일시: 자동 실행
- 실행 명령: `HOME=/home/Python_Ansible-Playbook ANSIBLE_LOCAL_TEMP=/home/Python_Ansible-Playbook/.ansible/tmp ANSIBLE_REMOTE_TEMP=/tmp/.ansible/tmp ANSIBLE_BECOME_ASK_PASS=False .venv/bin/ansible-playbook -i inventories/local/hosts.ini curriculum/lecture20/playbook.yml -e install_enabled=true`
- 검증 상태: `FAIL` (exit_code=2)
- RECAP: `localhost : ok=2 changed=0 unreachable=0 failed=1 skipped=0 rescued=0 ignored=0`
- 올바른 예상 결과:
  - `Gathering Facts` 성공
  - `Show lecture context` 출력 확인
  - `Install lecture packages when enabled` 단계에서 실패 확인 (패키지 미존재: `awscli`)
  - 설치 실패가 의도된 탐지 결과인지 저장소/OS 패키지 호환성을 점검
- MCR 캡처 솔루션: `docker run --rm -v "$PWD":/work -w /work mcr.microsoft.com/devcontainers/python:3.12 bash -lc 'python3 -m pip install pillow && python3 scripts/render_captures.py --summary results/lecture-verification-install/summary.tsv --logs results/lecture-verification-install/logs --out results/lecture-verification-install/captures --title-suffix install_enabled=true'`
- 실행 로그: `results/lecture-verification-install/logs/lecture20.log`

![lecture20 install_enabled=true 실행 캡처](../../results/lecture-verification-install/captures/lecture20.png)

---
이 문서는 `lecture.yml`을 기준으로 생성된 강의 안내서입니다.
