---
type: Workflow
title: "submodule 운영 가이드"
description: "서비스 저장소 submodule을 clone, 갱신하고 참조를 관리하는 절차입니다."
tags: [workflow, git, submodule, services]
timestamp: 2026-07-24T00:00:00+09:00
---
# submodule 운영 가이드

- 상태: accepted
- 최종 검토일: 2026-07-27

## 구성

| 서비스 | 경로 | 추적 브랜치 |
| --- | --- | --- |
| Backend | `services/backend` | `develop` |
| Frontend | `services/frontend` | `develop` |
| AI server | `services/ai` | `develop` |
| 아동 앱 | `services/app` | `develop` |
| 시선 추적 | `services/eyetracking` | `develop` |

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

`Submodule Pointer Update`는 5분 주기로 각 서비스의 `develop`과
orchestration의 gitlink를 비교한다. 새 fast-forward commit이 있으면
`automation/submodule-pointer-update` 브랜치에 포인터를 갱신하고
orchestration `develop` 대상 PR을 자동 생성한다.

포인터 PR에는 변경 전후 commit이 표시된다. 필수 리뷰 인원은 0명이므로
서비스 조합을 확인한 뒤 별도 승인 없이 병합할 수 있다. 포인터 PR을 병합하면
`Harness Validation`이 실행되고, 검증 성공 후 GitLab `main` 동기화가
자동으로 이어진다. 예약 실행이 지연될 수 있으므로 즉시 확인해야 할 때는
GitHub Actions에서 `Submodule Pointer Update`를 수동 실행한다.

자동화는 다음 조건에서 PR을 생성하지 않고 실패한다.

- 새 commit이 서비스 원격 저장소에 존재하지 않는다.
- 기존 포인터에서 새 `develop` commit으로의 이동이 fast-forward가 아니다.
- submodule이 초기화되지 않았거나 gitlink 형식이 아니다.

자동화가 실패했을 때만 갱신할 서비스의 `develop`을 fast-forward한 뒤
오케스트레이션 저장소에서 변경된 참조를 수동으로 커밋한다.

```bash
git -C services/backend switch develop
git -C services/backend pull --ff-only
git add services/backend
```

Frontend, AI server, 아동 앱, 시선 추적도 각각 `services/frontend`, `services/ai`, `services/app`, `services/eyetracking` 경로에서 같은 방식으로 갱신한다.

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
