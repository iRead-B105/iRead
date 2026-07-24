---
type: Execution Plan
title: Notion 명세 계약 이전
description: Notion 기능·API 명세를 OpenAPI, OKF 기능 카탈로그와 추적 데이터로 이전하는 실행 계획입니다.
tags: [plan, notion, openapi, feature-spec, contracts]
timestamp: 2026-07-24T00:00:00+09:00
---
# Notion 명세 계약 이전

- 상태: completed
- 담당: Codex
- 작성일: 2026-07-24
- 수정일: 2026-07-24

## 기대 결과

활성 API와 기능 식별자가 저장소에서 기계 검증 가능한 계약으로 관리되고 Notion 원본까지 추적된다.

## 작업 단계

- [x] Notion API·기능 스냅샷 수집
- [x] API 요청·응답 표 정규화
- [x] App·Admin·Auth OpenAPI 생성
- [x] 도메인별 OKF 기능 카탈로그 생성
- [x] 기능–API 추적 데이터 생성
- [x] Notion 변경 재수집
- [x] 계약·하네스 검증

## 검증

- `python tools/validate_contracts.py`
- `python tools/validate_harness.py`
- `git diff --check`

## 진행 기록

- 2026-07-24: 활성 API 117건과 기능 334건을 수집했다.
- 2026-07-24: 폐기 기능 30건이 모두 활성 API와 연결 해제된 것을 확인했다.
- 2026-07-24: App 57건, Admin 50건, Auth 10건을 OpenAPI로 생성했다.
- 2026-07-24: 이야기 진행률·완료 중복 API 2건을 음성 분기 API로 통합해 활성 API를 115건으로 정리했다.
- 2026-07-24: 계약 검증과 OKF 하네스 검증을 통과했다.

## 남은 위험

- Notion 주석에 `검수 필요`가 남은 API는 의미 검토가 추가로 필요하다.
- Backend–AI 내부 API의 실제 경로와 인증 방식은 `[TBD]`다.
