---
type: Architecture Decision
title: "ADR-0005: 아동 앱 저장소 추가"
description: "아동용 애플리케이션 저장소와 submodule 경로를 추가한 결정입니다."
tags: [architecture, child-app, repository, adr]
timestamp: 2026-07-24T00:00:00+09:00
---
# ADR-0005: 아동 앱 저장소 추가

- 상태: accepted
- 결정일: 2026-07-24
- 결정자: 사용자
- 대체 대상: 없음

## 배경

아동이 직접 사용하는 애플리케이션을 기존 Backend, Frontend, AI server와 독립적으로 관리하고 오케스트레이션 저장소에서 일관되게 조율해야 한다.

## 결정 기준

- 서비스 구현은 오케스트레이션 저장소와 분리한다.
- 기존 서비스 저장소와 같은 Git Flow 및 공개 범위 정책을 적용한다.
- `services/` 아래의 짧고 일관된 경로를 사용한다.
- 기술 스택과 구체적인 책임은 제품 및 아키텍처 결정 전까지 확정하지 않는다.

## 검토한 대안

1. 기존 Frontend 저장소에 아동 앱을 포함하면 배포 단위와 사용자별 책임 경계를 독립적으로 관리하기 어렵다.
2. `services/child-app` 경로는 저장소명 `iRead-frontend-app`과 경로명이 달라 일관성이 낮다.

## 결정

- 아동 앱 저장소는 공개 저장소 `iRead-B105/iRead-frontend-app`으로 관리한다.
- 오케스트레이션 저장소의 `services/app` 경로에 Git submodule로 연결한다.
- submodule의 갱신 기준 브랜치는 `develop`이다.
- 저장소는 `main`, `develop` 브랜치를 사용하며 기본 브랜치는 `develop`이다.
- `main`은 PR과 승인 1명을 요구한다.
- `develop`은 직접 push를 허용하며 두 브랜치 모두 force push와 삭제를 금지한다.
- 아동 앱의 기술 스택과 Frontend와의 책임 경계는 `[TBD]`로 유지한다.

## 영향

### 긍정적 영향

- 아동 앱의 구현 이력과 배포 주기를 다른 서비스와 독립적으로 관리할 수 있다.
- 오케스트레이션 저장소에서 모든 서비스 저장소의 검토된 커밋을 함께 조율할 수 있다.

### 부정적 영향과 트레이드오프

- clone과 참조 갱신 시 관리할 submodule이 하나 늘어난다.
- Frontend와 아동 앱의 책임 경계를 별도로 결정해야 한다.

## 검증 및 재검토 조건

- `iRead-frontend-app`의 `main`, `develop` 브랜치와 보호 정책을 확인한다.
- `services/app`이 `develop`의 원격 커밋을 가리키는지 확인한다.
- 아동 앱 기술 스택 또는 Frontend와의 책임 경계가 확정되면 관련 기준 문서와 새 ADR 필요 여부를 검토한다.
