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
| Frontend | `services/frontend-web` | `develop` |
| AI server | `services/ai` | `develop` |
| 아동 앱 | `services/frontend-app` | `develop` |
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

서비스 저장소의 작업 브랜치를 `develop`에 병합한 담당자가 orchestration
포인터 갱신 PR까지 생성한다. 다음은 Frontend 갱신 예시다.

```bash
git switch develop
git pull --ff-only origin develop
git submodule update --init --recursive

git switch -c chore/update-frontend-pointer
git -C services/frontend-web fetch origin develop
git -C services/frontend-web switch --detach origin/develop

git add services/frontend-web
git diff --cached --submodule=log
git commit -m "chore(submodule): frontend develop 참조 갱신"
git push -u origin chore/update-frontend-pointer
```

GitHub에서 `chore/update-frontend-pointer`를 orchestration `develop`에
병합하는 PR을 생성한다. 필수 리뷰 인원은 0명이므로 변경 전후 commit과
서비스 조합을 확인한 뒤 병합할 수 있다. 포인터 PR이 병합되면
`Harness Validation`이 실행되고, 검증 성공 후 GitLab `main` 동기화가
자동으로 이어진다.

Backend, AI server, 아동 앱, 시선 추적도 각각 `services/backend`,
`services/ai`, `services/frontend-app`, `services/eyetracking` 경로와 서비스 이름에
맞는 브랜치·commit 메시지를 사용해 같은 방식으로 갱신한다.

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
