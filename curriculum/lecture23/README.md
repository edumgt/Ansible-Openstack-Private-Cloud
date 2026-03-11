# lecture23 - S3 버킷 생성/정책 자동화

## 1. 강의 개요
- 강의 번호: `23`
- 모듈: `Module C / AWS Automation with Ansible`
- 난이도: `intermediate`
- 권장 시간: `60분`
- 모듈 초점: Ansible로 AWS 리소스를 생성/검증/정리하는 흐름을 익힙니다.

## 2. 선수 조건
- lecture22 완료 또는 동등한 실무 경험
- Linux 기본 명령어(ls, cat, systemctl) 사용 가능

## 3. 학습 목표
- S3 버킷 생성/정책 자동화 주제를 Ansible 중심으로 설명할 수 있다.
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
- 레퍼런스 플레이북: `../../playbooks/22_aws_s3_bucket.yml`
### 실행 명령
- `ansible-playbook -i ../../inventories/local/hosts.ini ./playbook.yml`
- `ansible-playbook -i ../../inventories/local/hosts.ini ./playbook.yml -e install_enabled=true`
- `ansible-playbook -i ../../inventories/local/hosts.ini ../../playbooks/22_aws_s3_bucket.yml`

## 8. 산출물과 검증
### 산출물
- 강의 실행 로그 또는 스크린샷 1개 이상
- AI 회고 노트(markdown) 1개
### 검증 기준
- playbook syntax error 없음
- 핵심 태스크 결과를 debug 출력으로 확인

## 9. AI 페어링 가이드
- 사전 점검 프롬프트: S3 버킷 생성/정책 자동화 실습 전에 실패할 수 있는 지점 3개를 체크리스트로 만들어줘.
- 실습 중 프롬프트: 현재 실행 로그를 보고 원인-증상-조치 순서로 트러블슈팅 가이드를 작성해줘.
- 회고 프롬프트: 이번 강의에서 배운 자동화 패턴을 다음 강의에 재사용할 수 있게 YAML 템플릿으로 정리해줘.

## 10. 심화 연계 (선택)
- 연계 트랙: `PostgreSQL / Redis 추가`
- 연계 목표: S3 버킷 생성/정책 자동화 학습 결과를 PostgreSQL / Redis 추가 확장 시나리오와 연결한다.
### 추가 실습
- backend PostgreSQL 연동
- volume 기반 데이터 영속화 확인
- AWS/OpenStack 브릿지: PostgreSQL은 RDS/Aurora 이해 기반
- 확장 프롬프트: 현재 강의(S3 버킷 생성/정책 자동화) 결과를 PostgreSQL / Redis 추가 실습으로 확장하는 체크리스트를 YAML로 작성해줘.

## 11. 참고 파일
- `lecture.yml`: 강의 메타데이터
- `playbook.yml`: 강의 실행 플레이북

---
이 문서는 `lecture.yml`을 기준으로 생성된 강의 안내서입니다.
