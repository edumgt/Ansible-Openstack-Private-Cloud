# 45강 주차별 학습 체크리스트 (강의당 60분)

이 문서는 `README.md`의 전체 학습 로드맵을 실행용 체크리스트로 정리한 문서입니다.

## 1. 사용 방법

- 한 주에 5강씩 진행합니다. (`9주 x 5강 = 45강`)
- 각 강의는 60분 기준으로 진행합니다.
- `curriculum/lectureNN/README.md` 확인
- `curriculum/lectureNN/playbook.yml` 실행
- 실행 로그 1개 + 회고 노트 1개 저장

## 2. 공통 실행 루틴

```bash
# 강의 실행
ansible-playbook -i inventories/local/hosts.ini curriculum/lectureNN/playbook.yml

# 설치 태스크 포함 실행(필요 시)
ansible-playbook -i inventories/local/hosts.ini curriculum/lectureNN/playbook.yml -e install_enabled=true
```

## 3. 주차별 계획

## Week 1 (lecture01~lecture05)

- [ ] lecture01 Ansible 학습환경 진단과 컨트롤 노드 준비
- [ ] lecture02 Inventory 구조와 host/group 변수 설계
- [ ] lecture03 Ad-hoc 명령과 연결 테스트 자동화
- [ ] lecture04 변수, facts, register 실습
- [ ] lecture05 loop, when, block 제어문 실습
- [ ] 실행 로그 5개 이상 수집
- [ ] 회고 노트 5개 작성

## Week 2 (lecture06~lecture10)

- [ ] lecture06 Jinja2 템플릿과 설정 파일 생성
- [ ] lecture07 handler와 idempotency 검증
- [ ] lecture08 Role 구조 분해와 재사용 설계
- [ ] lecture09 공통 서버 부트스트랩 자동화
- [ ] lecture10 사용자/권한/SSH 정책 자동화
- [ ] 실행 로그 5개 이상 수집
- [ ] 회고 노트 5개 작성

## Week 3 (lecture11~lecture15)

- [ ] lecture11 Nginx 설치와 웹 서비스 배포 자동화
- [ ] lecture12 Docker Engine 설치 자동화
- [ ] lecture13 Compose 스택 배포 자동화
- [ ] lecture14 Rolling Update 배포 실습
- [ ] lecture15 Blue/Green 전환 자동화
- [ ] 자동화 태스크 재실행으로 idempotency 확인
- [ ] 회고 노트 5개 작성

## Week 4 (lecture16~lecture20)

- [ ] lecture16 Trivy 기반 컨테이너 취약점 점검
- [ ] lecture17 Docker Bench 점검과 보고서 자동화
- [ ] lecture18 CrowdSec + Nginx 보안 실습 자동화
- [ ] lecture19 AWS SSM 기반 무SSH 프로비저닝
- [ ] lecture20 AWS VPC 네트워크 생성 자동화
- [ ] 보안/클라우드 체크리스트 정리
- [ ] 회고 노트 5개 작성

## Week 5 (lecture21~lecture25)

- [ ] lecture21 AWS EC2 인스턴스 생성 자동화
- [ ] lecture22 생성 후 SSM 기반 후속 설정 자동화
- [ ] lecture23 S3 버킷 생성/정책 자동화
- [ ] lecture24 AWS 출력값 수집과 결과 정리
- [ ] lecture25 AWS 실습 자원 정리 자동화
- [ ] OpenStack 전환 준비 체크리스트 작성
- [ ] 회고 노트 5개 작성

## Week 6 (lecture26~lecture30)

- [ ] lecture26 OpenStack 개요와 아키텍처 서비스 맵
- [ ] lecture27 OpenStack 인증(Keystone)과 프로젝트 구조 자동화
- [ ] lecture28 OpenStack CLI 환경 구성과 리소스 조회 자동화
- [ ] lecture29 Glance 이미지 라이프사이클 자동화
- [ ] lecture30 Nova 인스턴스 생성/삭제 플레이북 작성
- [ ] OpenStack 기본 리소스 용어표 정리
- [ ] 회고 노트 5개 작성

## Week 7 (lecture31~lecture35)

- [ ] lecture31 Neutron 네트워크/서브넷 자동화
- [ ] lecture32 Neutron 라우터/Floating IP 운영 자동화
- [ ] lecture33 Security Group/Key Pair 표준화 자동화
- [ ] lecture34 Cinder 볼륨 생성/연결 자동화
- [ ] lecture35 OpenStack 자원 상태 점검 리포트 자동화
- [ ] 네트워크/보안/스토리지 운영 체크리스트 작성
- [ ] 회고 노트 5개 작성

## Week 8 (lecture36~lecture40)

- [ ] lecture36 Horizon 운영 점검 체크리스트 자동화
- [ ] lecture37 OpenStack 로그 수집과 장애 1차 진단
- [ ] lecture38 OpenStack 쿼터/리소스 한도 운영 자동화
- [ ] lecture39 OpenStack-AWS 네트워크 매핑 검증
- [ ] lecture40 OpenStack IAM(Keystone)과 AWS IAM 매핑
- [ ] OpenStack-AWS 매핑표 업데이트
- [ ] 회고 노트 5개 작성

## Week 9 (lecture41~lecture45)

- [ ] lecture41 Kolla Ansible 배포 아키텍처 이해
- [ ] lecture42 Kolla Ansible 사전점검/배포 자동화
- [ ] lecture43 OpenStack 입문 1: MicroStack 단일노드 실습
- [ ] lecture44 OpenStack 입문 2: DevStack API/CLI 실습
- [ ] lecture45 OpenStack 입문 3: Kolla Ansible 운영 점검 캡스톤
- [ ] 최종 운영 체크리스트 + 트러블슈팅 문서 정리
- [ ] 최종 회고 노트 작성

## 4. 최종 완료 체크

- [ ] 45개 강의 실행 완료
- [ ] 강의별 실행 로그 또는 스크린샷 확보
- [ ] 강의별 회고 노트 완료
- [ ] OpenStack 핵심 서비스(Keystone/Nova/Neutron/Cinder) 설명 가능
- [ ] Ansible 기반 OpenStack 운영 자동화 흐름 설명 가능
