---
type: Contract Catalog
title: iRead 계약 카탈로그
description: 기능, API와 데이터베이스 명세의 기준 원본, 소유자와 이전 상태를 정리합니다.
tags: [contracts, features, openapi, mysql, traceability]
timestamp: 2026-07-27T00:00:00+09:00
---
# iRead 계약 카탈로그

## 계약 현황

| 계약 | 기준 원본 | 소유자 | 상태 | 파생 위치 |
| --- | --- | --- | --- | --- |
| 승인 기능 명세 | `docs/product/features/` | Orchestration | 이전 완료 | Notion 이관 스냅샷 |
| App–Backend API | `contracts/openapi/app-api.yaml` | Orchestration | 이전·검토 완료 | Notion 이관 스냅샷, Backend·App |
| Admin–Backend API | `contracts/openapi/admin-api.yaml` | Orchestration | 이전·검토 완료 | Notion 이관 스냅샷, Backend·Frontend |
| 공통 인증 API | `contracts/openapi/auth-api.yaml` | Orchestration | 이전·검토 완료 | Notion 이관 스냅샷, Backend·소비 앱 |
| Backend–AI API | `contracts/openapi/ai-api.yaml` | Orchestration | 기준 계약 작성 및 이야기 계약 정합화 완료 | Backend·AI |
| Eye Tracker API 연동 초안 | `contracts/gaze/eyetracker-api-contract.md` | Orchestration | draft, 팀 합의 필요 | Backend·Frontend·Eyetracking |
| MySQL 실행 스키마 | `services/backend` Flyway migration | Backend | 2026-07-27 확정 ERD로 V1 교체, Backend 정합화·실행 검증 필요 | `contracts/database/schema.sql`, `contracts/database/erd.png`, `contracts/database/erd.md` |

## 전환 원칙

- 생성된 OpenAPI와 해소 규칙은 계약 기준선이며 Notion 스냅샷은 이관 당시 출처 확인에만 사용한다.
- Git 계약 변경은 외부 Notion에 자동 또는 필수 역동기화하지 않는다.
- Backend–AI API는 `X-API-Key`, `Idempotency-Key`와 계약별 처리 제한을 포함해 변경한다.
- Eye Tracker API 연동 초안은 OpenAPI 원본 변경 전 Backend·Frontend·Eyetracking 담당자 검토를 거친다.
- MySQL migration 변경 시 스키마 계약의 변경 사유와 MySQL 8.4 실행 결과를 함께 기록한다.
- 세부 절차는 [명세 관리 워크플로](../docs/workflows/specification-management.md)를 따른다.
