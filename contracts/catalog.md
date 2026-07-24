---
type: Contract Catalog
title: iRead 계약 카탈로그
description: 기능, API와 데이터베이스 명세의 기준 원본, 소유자와 이전 상태를 정리합니다.
tags: [contracts, features, openapi, mysql, traceability]
timestamp: 2026-07-24T00:00:00+09:00
---
# iRead 계약 카탈로그

## 계약 현황

| 계약 | 기준 원본 | 소유자 | 상태 | 파생 위치 |
| --- | --- | --- | --- | --- |
| 승인 기능 명세 | `docs/product/features/` | Orchestration | 전환 중 | Notion 기능 명세 |
| App–Backend API | `contracts/openapi/app-api.yaml` | Orchestration | 이전 완료, 일부 검토 필요 | Notion API 명세, Backend·App |
| Admin–Backend API | `contracts/openapi/admin-api.yaml` | Orchestration | 이전 완료, 일부 검토 필요 | Notion API 명세, Backend·Frontend |
| 공통 인증 API | `contracts/openapi/auth-api.yaml` | Orchestration | 이전 완료, 일부 검토 필요 | Notion API 명세, Backend·소비 앱 |
| Backend–AI API | `contracts/openapi/ai-api.yaml` | Orchestration | [TBD] OpenAPI 이전 | Notion API 명세, Backend·AI |
| MySQL 실행 스키마 | `services/backend` migration | Backend | [TBD] migration 도입 | `contracts/database/schema.sql`, ERD |

## 전환 원칙

- 생성된 OpenAPI는 계약 기준선이며 `x-review-status: needs-review`인 operation은 의미 검토가 끝날 때까지 변경 시 Notion 원본도 함께 확인한다.
- [API 계약 검토 목록](review-queue.md)의 항목을 완료하면 Notion의 검수 표시와 OpenAPI를 함께 갱신한다.
- Backend–AI API는 실제 경로와 인증 방식이 확정되기 전까지 빈 계약을 만들지 않는다.
- MySQL migration 도입 전에는 스키마 스냅샷의 변경 사유와 문법 검증 결과를 함께 기록한다.
- 세부 절차는 [명세 관리 워크플로](../docs/workflows/specification-management.md)를 따른다.
