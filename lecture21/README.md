# lecture21 - OpenStack/Nova 기본 점검

## 1. 강의 개요
- 강의 번호: `21`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `30분`

## 2. 상세 학습 내용
- `openstack` CLI 동작 여부를 빠르게 점검한다.
- `nova` 관련 서비스/하이퍼바이저 조회 흐름을 확인한다.
- 인증 정보가 없을 때와 있을 때의 출력 차이를 비교한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `OS_CLOUD` 또는 `OS_AUTH_URL` 등 OpenStack 인증 환경변수 확인

## 4. 실습 절차
1. 기본 실행으로 CLI 설치 여부와 인증 상태를 확인한다.
2. 필요하면 `install_enabled=true`로 `python3-openstackclient`를 설치한다.
3. `openstack token issue` 결과를 확인한다.
4. `openstack compute service list`와 `openstack hypervisor list` 결과를 기록한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=false

# CLI 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=true
```

## 6. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- `openstack --version` 출력 또는 미설치 상태 확인
- `token_rc`, `nova_service_rc`, `hypervisor_rc` 값 확인
- 인증이 정상인 경우 Nova 서비스/하이퍼바이저 목록 확인

## 7. 트러블슈팅 힌트
- `openstack` 명령 없음: `install_enabled=true`로 재실행
- 인증 실패: `OS_CLOUD` 또는 `OS_AUTH_URL`, `OS_USERNAME`, `OS_PASSWORD`, `OS_PROJECT_NAME` 확인
- Nova 조회 실패: Keystone 인증 성공 여부와 compute API 엔드포인트 상태 확인

## 8. 참고 파일
- `./lecture.yml`
- `./playbook.yml`
