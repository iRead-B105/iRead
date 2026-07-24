---
type: Contract Review Queue
title: "API 계약 검토 목록"
description: "Notion에서 OpenAPI로 이전했지만 추가 의미 검토가 필요한 API를 정리합니다."
tags: [contracts, openapi, review]
timestamp: 2026-07-25T01:00:44+09:00
---
# API 계약 검토 목록

활성 API 74건 가운데 0건에 추가 검토 표시가 남아 있다.

권장 처리는 기존 ERD와 정식 도메인 API를 우선하고, 화면 이동·선택·재생 상태는 클라이언트 책임으로 분리한 결과다.

| API | 분류 | 권장 처리 | 검토 사유 | Notion |
| --- | --- | --- | --- | --- |

## 별도 미결 사항

- Backend–AI 내부 계약은 `contracts/openapi/ai-api.yaml`에서 관리한다.
- Backend MySQL Flyway V1과 실행 검증 결과는 `contracts/database/backend-alignment.md`에서 관리한다.
- 기존 데이터가 있는 환경은 V1 직접 적용 전에 별도 baseline과 변환 migration이 필요하다.
