# OpenAPI 계약

HTTP API 계약을 소비자 경계별로 관리한다.

* [App API](app-api.yaml) - 아동 앱과 Backend 계약, 57 operations
* [Admin API](admin-api.yaml) - 교수자 Frontend와 Backend 계약, 50 operations
* [Auth API](auth-api.yaml) - 공통 인증 계약, 10 operations
* `ai-api.yaml` - Backend와 AI server 계약 `[TBD]`

OpenAPI 문서는 JSON 문법과 호환되는 YAML 1.2 형식으로 생성한다. `x-notion-*` 확장 필드로 원본 페이지와 기능 식별자를 추적한다. 추가 의미 검토가 필요한 API는 [검토 목록](../review-queue.md)에서 관리한다.
