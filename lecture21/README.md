# lecture21 - OpenStack/Nova 기본 점검

## 1. 강의 개요
- 강의 번호: `21`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `30분`

## 2. 상세 학습 내용
- `openstack` CLI로 Keystone 인증이 되는지 확인한다.
- `nova service list`와 `hypervisor list`를 조회한다.
- Codespaces mock 환경과 실제 OpenStack 환경을 같은 플레이북으로 점검한다.

## 3. 실행 전 체크
- `lecture22`를 먼저 실행해 mock 환경 또는 인증 정보를 준비
- `.venv/bin/openstack` 설치 여부 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`

## 4. 실습 절차
1. Keystone 엔드포인트 응답을 확인한다.
2. `openstack token issue` 결과를 확인한다.
3. `openstack compute service list` 결과를 기록한다.
4. `openstack hypervisor list` 결과를 기록한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# lecture22 이후 실행
source .lab/keystone-admin-openrc
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=false

# lecture21에서 필요한 패키지까지 같이 준비
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=true
```

## 6. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- `token_rc=0`
- `nova_service_rc=0`
- `hypervisor_rc=0`
- 서비스/하이퍼바이저 목록이 출력됨

## 7. 트러블슈팅 힌트
- `openstack` 명령 없음: `lecture22`를 `install_enabled=true`로 다시 실행
- `keystone_http_status`가 `200`이 아님: mock 서버 또는 실제 Keystone 상태 확인
- Nova 조회 실패: 인증 정보 또는 compute endpoint 확인

## 8. 참고 파일
- `./lecture.yml`
- `./playbook.yml`
- `../lecture22/playbook.yml`
