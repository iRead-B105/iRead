---
type: Execution Plan
title: "GitLab 단일 저장소 동기화 도입"
description: "orchestration과 다섯 submodule의 실제 코드와 원본 Git 이력을 GitLab 단일 저장소에 동기화하는 계획입니다."
tags: [plan, git, github-actions, gitlab, submodule, subtree]
timestamp: 2026-07-25T00:00:00+09:00
---
# GitLab 단일 저장소 동기화 도입

- 상태: completed
- 작성일: 2026-07-25
- 수정일: 2026-07-25

## 목표

GitHub의 독립 저장소와 submodule 개발 방식을 유지하면서 GitLab `S15P11B105/main`에 orchestration 파일, 다섯 서비스의 실제 코드와 원본 Git 이력을 반영한다.

## 구현

- [x] `iRead-eyetracking`을 `services/eyetracking` submodule로 등록한다.
- [x] 서비스 원본 commit을 merge parent로 연결하고 파일 스냅샷을 동기화하는 스크립트를 작성한다.
- [x] 원본 branch와 tag를 `upstream/*`에 보존한다.
- [x] 기존 GitLab 구조를 일반 commit으로 전환하는 bootstrap을 제공한다.
- [x] `develop` push, 6시간 주기와 수동 실행 workflow를 추가한다.
- [x] 기존 `Harness Validation` 성공 commit을 자동 동기화의 시작 조건으로 연결한다.
- [x] 운영 절차와 실패 조건을 문서화한다.
- [x] GitHub Actions secret `GITLAB_PUSH_TOKEN`을 등록한다.
- [x] workflow를 실행하고 GitLab `main`, branch, tag와 manifest를 확인한다.

## 완료 조건

- GitLab 루트에 orchestration 파일이 존재한다.
- `services/backend`, `services/frontend-web`, `services/ai`, `services/frontend-app`, `services/eyetracking`에 실제 코드가 존재한다.
- 서비스 원본 commit과 branch가 `upstream/*`에서 조회된다.
- manifest commit이 orchestration gitlink와 일치한다.
- 후속 orchestration `develop` push가 fast-forward 증분 동기화된다.

## 완료 결과

Repository Secret과 GitLab push 권한을 확인했고, orchestration과 다섯 서비스의 초기 통합 동기화를 완료했다. 후속 서비스 갱신은 원본 commit을 merge parent로 연결한 뒤 파일 스냅샷을 갱신한다.
