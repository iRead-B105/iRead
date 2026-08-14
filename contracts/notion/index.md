# Notion 명세 스냅샷

* [API·기능 스냅샷](spec-snapshot.json) - 활성 API 115건과 기능 334건을 Git 계약으로 이관할 때 사용한 정규화 데이터

이 파일은 이관 출처와 `x-notion-*` 추적을 위해 보존한다. 현재 계약은 OpenAPI와 `contracts/api-resolutions.json`이며 외부 Notion에 역동기화하지 않는다. 명시적인 재수집 요청이 있을 때만 `tools/export_notion_specs.py`를 사용하고 토큰은 저장소에 포함하지 않는다. `우선순위`와 `구현여부` 속성은 수집하지 않는다.
