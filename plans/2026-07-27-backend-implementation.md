---
type: Execution Plan
title: "Backend 미구현 계약 완료"
description: "Backend 구현 백로그의 미완료 항목을 계약과 테스트 기준으로 순차 완료합니다."
tags: [plan, backend, implementation, openapi, testing]
timestamp: 2026-07-27T10:13:10+09:00
---
# Backend 미구현 계약 완료

- 상태: active
- 담당: Codex
- 작성일: 2026-07-27
- 수정일: 2026-07-27

## 기대 결과

Backend 구현 백로그의 `BE-004`부터 `BE-012`까지 각 항목이 OpenAPI, MySQL 계약과 수용 기준을 충족하고 관련 테스트와 전체 Backend 테스트를 통과한다.

## 배경

- 서비스 우선순위와 상태는 [Backend·Frontend 구현 백로그](../docs/planning/implementation-backlog.md)를 따른다.
- HTTP 계약은 [OpenAPI 계약](../contracts/openapi/index.md), 데이터 계약은 [MySQL 스키마 계약](../contracts/database/index.md)을 따른다.
- `BE-001`~`BE-003`은 구현과 필수 검증이 완료되었다.
- 각 구현 단위는 Backend `develop`에서 분기한 `feature/*` 브랜치와 PR로 관리한다.
- 하나의 작업을 완료할 때마다 Backend 커밋·push·PR·squash merge 후 오케스트레이션의 submodule과 백로그를 동기화한다.

## 확인이 필요한 사항

- 계약과 기존 데이터 모델만으로 제품 동작을 하나로 결정할 수 없으면 구현 전에 사용자에게 질문한다.
- 새로운 외부 의존성, schema 변경, API 계약 변경 또는 서비스 책임 변경이 필요하면 적용 전에 사용자에게 질문한다.

## 작업 단계

- [ ] `BE-004` 교수자·학생 관리 API 계약 정합화
- [ ] `BE-005` 관리자 훈련·검사 API 계약 정합화
- [ ] `BE-006` 관리자 보고서·시선 결과 API 계약 정합화
- [ ] `BE-007` 아동 로그인·성장·마이페이지 API 구현
- [ ] `BE-008` 아동 검사·훈련 세션 API 구현
- [ ] `BE-009` 이야기·시선 세션 API 계약 정합화
- [ ] `BE-010` AI 없는 데모용 결정적 fixture provider 완료
- [ ] `BE-011` 비식별 데모 seed와 파일·DB 초기화 절차 완료
- [ ] `BE-012` OpenAPI 기준 오류 응답과 입력 검증 통일
- [ ] 전체 OpenAPI operation과 Backend controller 매핑 최종 대조

## 검증

- 작업별 관련 단위·HTTP 통합 테스트를 추가하거나 수정한다.
- 각 작업 브랜치에서 `.\gradlew.bat test --rerun-tasks`를 실행한다.
- migration 또는 JPA mapping 변경 시 MySQL 8.4.x에서 `MySqlFlywayIntegrationTest`를 실행한다.
- 계약 또는 오케스트레이션 문서 변경 시 다음 명령을 실행한다.
  - `python tools/validate_contracts.py`
  - `python tools/validate_harness.py`
  - `python tools/generate_erd.py --check`
  - `git diff --check`
- 테스트와 필수 검증이 성공한 뒤에만 백로그 상태를 `done`으로 변경한다.

## 진행 기록

- 2026-07-27: 사용자가 Backend 미구현 항목을 단위별로 구현하고 커밋·push·병합하도록 요청했다.
- 2026-07-27: 첫 작업을 P0 미완료 항목인 `BE-004`로 정했다.

## 결정 및 변경 사항

- 각 작업은 독립된 `feature/*` 브랜치와 `develop` 대상 PR로 관리한다.
- PR 검증 후 squash merge하고, 병합된 Backend 커밋을 오케스트레이션 submodule에 반영한다.

## 남은 위험

- 현재 구현에는 계약과 정확히 일치하지 않는 기존 endpoint가 남아 있어 호환성 영향을 작업별로 확인해야 한다.
- App 검사·훈련과 AI fixture의 구체적 동작에서 계약만으로 결정할 수 없는 제품 규칙이 발견될 수 있다.
- 실제 MySQL 통합 테스트는 로컬 MySQL 8.4.x 실행 환경이 필요하다.
