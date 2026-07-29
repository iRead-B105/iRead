# OpenAPI 계약

HTTP API 계약을 소비자 경계별로 관리한다.

* [App API](app-api.yaml) - 아동 앱과 Backend 계약
* [Admin API](admin-api.yaml) - 교수자 Frontend와 Backend 계약
* [Auth API](auth-api.yaml) - 공통 인증 계약, 10 operations
* [AI API](ai-api.yaml) - Backend와 AI server 내부 계약

OpenAPI 문서는 JSON 문법과 호환되는 YAML 1.2 형식으로 생성한다. `x-notion-*` 확장 필드로 원본 페이지와 기능 식별자를 추적한다. App·Admin·Auth 계약은 성공 응답, 오류 상세와 상태별 오류 응답을 `components`에서 공통 관리한다. 추가 의미 검토가 필요한 API는 [검토 목록](../review-queue.md)에서 관리한다.

Notion 이관 후 Git에서 새로 확정한 operation은 `x-contract-origin: repository`로 표시하며 `x-notion-page-id`를 사용하지 않는다. 별도 표시가 없는 기존 operation은 Notion 이관 계약으로 간주한다.
