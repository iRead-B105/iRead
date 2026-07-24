# submodule 운영 가이드

- 상태: accepted
- 최종 검토일: 2026-07-24

## 구성

| 서비스 | 경로 | 추적 브랜치 |
| --- | --- | --- |
| Backend | `services/backend` | `develop` |
| Frontend | `services/frontend` | `develop` |
| AI server | `services/ai` | `develop` |
| 아동 앱 | `services/app` | `develop` |

오케스트레이션 저장소는 각 submodule의 특정 커밋을 기록한다. `develop` 추적 설정은 원격 변경을 조회할 기준이며, 참조 커밋은 자동으로 바뀌지 않는다.

## 저장소 받기

처음 clone할 때 submodule까지 함께 받는다.

```bash
git clone --recurse-submodules https://github.com/iRead-B105/iRead.git
```

이미 clone한 저장소라면 다음 명령으로 초기화한다.

```bash
git submodule update --init --recursive
```

## 참조 커밋 갱신

갱신할 서비스의 `develop`을 fast-forward한 뒤 오케스트레이션 저장소에서 변경된 참조를 커밋한다.

```bash
git -C services/backend switch develop
git -C services/backend pull --ff-only
git add services/backend
```

Frontend, AI server, 아동 앱도 각각 `services/frontend`, `services/ai`, `services/app` 경로에서 같은 방식으로 갱신한다.

submodule 커밋이 원격 저장소에 push되었는지 확인한 뒤 오케스트레이션 저장소의 참조를 push한다. 원격에 없는 커밋을 참조하면 다른 환경에서 clone할 수 없다.

## 기록된 상태로 복원

오케스트레이션 저장소가 기록한 커밋으로 submodule을 맞춘다.

```bash
git submodule update --init --recursive
```

이 명령은 submodule을 분리된 HEAD 상태로 둘 수 있다. 서비스 코드를 수정하려면 해당 submodule에서 작업 브랜치를 명시적으로 만든다.

## 작업 원칙

- 서비스 코드와 커밋은 해당 서비스 저장소에서 관리한다.
- 오케스트레이션 저장소에는 검토가 끝난 서비스 커밋의 참조만 반영한다.
- submodule 내부의 미커밋 변경을 둔 채 참조를 갱신하지 않는다.
- 서비스 저장소의 강제 push로 이미 기록된 커밋을 제거하지 않는다.
