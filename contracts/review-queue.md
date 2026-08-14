---
type: Contract Review Queue
title: "API 계약 검토 목록"
description: "Notion에서 OpenAPI로 이전했지만 추가 의미 검토가 필요한 API를 정리합니다."
tags: [contracts, openapi, review]
timestamp: 2026-08-04T19:22:12+09:00
---
# API 계약 검토 목록

활성 API 90건 가운데 5건에 추가 검토 표시가 남아 있다.

권장 처리는 기존 ERD와 정식 도메인 API를 우선하고, 화면 이동·선택·재생 상태는 클라이언트 책임으로 분리한 결과다.

| API | 분류 | 권장 처리 | 검토 사유 | Notion |
| --- | --- | --- | --- | --- |
| `PUT /api/admin/student/{studentId}/story-history/{storyId}/pages/{storyLineId}` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | 요청 요약은 있으나 상세 요청 표가 없음, 응답 요약은 있으나 상세 응답 표가 없음 | `contracts/api-resolutions.json#admin-story-page-update` |
| `POST /api/admin/student/{studentId}/story-history/{storyId}/pages/{storyLineId}/image` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | 요청 요약은 있으나 상세 요청 표가 없음, 응답 요약은 있으나 상세 응답 표가 없음 | `contracts/api-resolutions.json#admin-story-page-image-upload` |
| `POST /api/admin/student/{studentId}/story-history/{storyId}/pages/{storyLineId}/image/regenerate` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | 요청 요약은 있으나 상세 요청 표가 없음, 응답 요약은 있으나 상세 응답 표가 없음 | `contracts/api-resolutions.json#admin-story-page-image-regenerate` |
| `DELETE /api/app/story/{studentId}/sessions/{storyId}` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | 요청 요약은 있으나 상세 요청 표가 없음 | `contracts/api-resolutions.json#app-story-session-delete` |
| `POST /api/app/story/{studentId}/{storyId}/lines/{lineId}/branches/transcribe` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | 요청 요약은 있으나 상세 요청 표가 없음, 응답 요약은 있으나 상세 응답 표가 없음 | `contracts/api-resolutions.json#app-story-branch-transcribe` |

## 별도 미결 사항

- Backend–AI 내부 계약은 `contracts/openapi/ai-api.yaml`에서 관리한다.
- Backend MySQL Flyway 누적 migration과 실행 검증 결과는 `contracts/database/backend-alignment.md`에서 관리한다.
- 기존 데이터가 있는 환경은 V1 직접 적용 전에 별도 baseline과 변환 migration이 필요하다.
