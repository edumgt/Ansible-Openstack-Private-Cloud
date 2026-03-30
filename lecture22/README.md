# lecture22 - Keystone 설치와 인증 환경 준비

## 1. 강의 개요
- 강의 번호: `22`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `45분`

## 2. 상세 학습 내용
- Keystone 관련 패키지와 CLI를 설치한다.
- Apache2 및 포트 5000 상태를 확인한다.
- `lecture21` 실행 전에 사용할 `openrc` 파일을 준비한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. 기본 실행으로 현재 Keystone 관련 바이너리 상태를 확인한다.
2. `install_enabled=true`로 Keystone, Apache2, OpenStack CLI를 설치한다.
3. `/root/keystone-admin-openrc` 파일이 생성되었는지 확인한다.
4. 포트 5000 리스닝 여부와 Apache2 상태를 확인한다.
5. `lecture21`을 실행해 인증 및 Nova 조회를 이어서 점검한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture22/playbook.yml -e install_enabled=false

# 패키지 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture22/playbook.yml -e install_enabled=true

# openrc 적용 후 lecture21 실행
source /root/keystone-admin-openrc
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=false
```

## 6. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- `keystone-manage` 명령 확인
- `/root/keystone-admin-openrc` 파일 생성 확인
- Apache2 상태와 포트 5000 리스닝 여부 확인

## 7. 트러블슈팅 힌트
- 패키지 설치 실패: OS 저장소 상태와 패키지명 확인
- 포트 5000 미리스닝: Keystone 설정/WSGI 연동/Apache2 서비스 상태 확인
- `lecture21` 인증 실패: `source /root/keystone-admin-openrc` 적용 여부 확인

## 8. 참고 파일
- `./lecture.yml`
- `./playbook.yml`
