---
type: Execution Plan
---
# 교수자 주요 화면 API 계약 정합화

- 상태: completed
- 수정일: 2026-08-04

## 목표

교수자 Frontend API-only 정적 감사에서 확인한 훈련 이력, 검사 이력, 학습 현황, 이야기 이력과 보고서의 식별자·응답·집계 계약을 Git 기준 원본으로 확정한다. 서비스 구현은 이 계약을 승인 기준으로 후속 PR에서 수행한다.

## 범위

포함:

- 훈련 이력 전체 문항 결과 DTO
- 검사 `testId + questionNo` 복합 식별자와 문항별 gaze 조회
- 정확도·읽기 속도 source record endpoint와 공통 지표 metadata
- 이야기 `wordMetrics`, 판정 기준·설명과 `calculationVersion`
- 보고서 최소 1학습일 생성, 공통 지표, snapshot version과 비교 부족 상태
- Admin OpenAPI, 기능 명세, 해소 규칙, fixture, 추적 데이터와 계약 카탈로그 동기화

제외:

- Backend·Frontend·AI·App·Eye Tracking 구현 코드 변경
- 구형 Frontend `adminApi.ts` 삭제
- 실제 DB·Backend·브라우저 E2E
- 보고서 영역별 자동 분석 임계값의 제품 결정

## 승인 결정

- 검사 문항별 gaze는 `GET /api/admin/test/{studentId}/{testId}/questions/{questionNo}/gaze-analysis`로 정의한다.
- 학습 현황 source record는 기존 trend 응답에 혼합하지 않고 정확도·속도별 endpoint로 분리한다.
- 이야기의 권위 있는 판정 결과는 Backend `wordMetrics`이며 Frontend raw replay는 재생에만 사용한다.
- 보고서 자동 분석은 재현 가능한 증감과 데이터 부족 상태부터 계약으로 확정하고 제품 임계값은 `[TBD]`로 유지한다.

## 작업

- [x] 기존 Admin OpenAPI, 기능 명세와 구현 해소 규칙의 관련 operation을 대조한다.
- [x] 훈련 전체 문항과 검사 복합 식별·문항별 gaze 계약을 반영한다.
- [x] 정확도·읽기 속도 source record와 공통 지표 metadata 계약을 반영한다.
- [x] 이야기 word metric·판정 meta·버전 계약을 반영한다.
- [x] 보고서 1학습일·snapshot version·분석 상태 계약을 반영한다.
- [x] fixture, `api-resolutions.json`, `traceability.json`과 계약 카탈로그를 동기화한다.
- [x] 계약·하네스 검증과 변경 누락 검색을 수행한다.

## 검증

- `python tools/validate_contracts.py`
- `python tools/validate_harness.py`
- 관련 operationId, schema, fixture와 traceability 정적 검색
- 변경된 YAML·JSON parse 검증

검증 결과:

- 계약 검증 통과: 109 operations, 339 features, 99 reviewed, 0 needs-review
- 하네스 검증 통과: 126 Markdown files, 60 record documents
- 생성기 선택 교체 테스트 통과
- 전체 도구 테스트의 기존 DB 개수 검사는 사용자 소유 Backend submodule 변경으로 unique constraint 기대값 15와 실제 16이 달라 실패했으며 이번 범위에서는 수정하지 않는다.

## 미결 사항

- `[TBD]` 보고서 자동 분석의 영역별 임계값과 증가·유지·감소 제품 경계값
- `[BLOCKED]` 실제 HTTP·인증·브라우저 smoke는 로컬 MySQL과 Backend 실행 환경을 준비한 뒤 수행한다.
