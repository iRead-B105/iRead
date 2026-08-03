---
type: Execution Plan
---
# 교수자 이야기 이력·교안 편집 Backend API

- 상태: completed
- 수정일: 2026-07-31

- API delivery status: completed
## 범위

- 교수자용 이야기 이력 목록·상세·시선 분석 조회 API를 추가한다.
- 교안 편집 전용 조회·전체 저장 API를 추가한다.
- 기존 Backend에만 있는 최근 학습 이벤트·커리큘럼 생성·교안 재생성 API를 공통 OpenAPI에 등록한다.
- 보고서 생성 조건과 검사 결과 지표 저장 계약을 Backend 기준으로 정합화한다.
- Frontend는 이번 범위에서 변경하지 않는다. AI server는 이야기 분기 응답 계약과 결정적 Mock 응답을 제공한다.
- 최종 스키마는 Flyway V1, 데모 데이터는 V2로 통합하고 다음 migration은 V3부터 기록한다.

## 작업

- [x] Admin OpenAPI에 신규·누락 API와 오류 계약을 등록한다.
- [x] 이야기 이력 목록·상세 조회와 소유권·날짜·페이지 검증을 구현한다.
- [x] 최신 STORY 시선 분석 결과를 페이지 단위 응답으로 변환한다.
- [x] 교안 편집 조회·전체 저장 DTO와 revision 충돌 검증을 구현한다.
- [x] 34개 문항 유형에 기존 생성 검증·조립 정책을 재사용한다.
- [x] 보고서 생성의 완료 훈련일 2일 조건을 적용한다.
- [x] 검사 완료 결과에 계산 가능한 시간 지표를 저장하고 결측값을 보존한다.
- [x] 관련 Controller·Service·권한·계약 테스트를 추가한다.

## Current delivery

- [x] Admin OpenAPI registration for story, lesson material, and three existing backend-only routes
- [x] Story history, detail, and gaze analysis read APIs
- [x] Lesson material GET/PUT with 1-5 items, immutable type, revision conflict, and atomic validation
- [x] Backend unit tests and full regression suite
- [x] Report eligibility requires two distinct completed training days
- [x] Test result stores solvingTimeSeconds when calculable
- [x] Test gaze sessions store contiguous 500ms departure interval counts when calculable

## 검증

- `services/backend/gradlew.bat test`
- `python tools/generate_contracts.py`
- `python tools/validate_contracts.py`
- `python tools/validate_harness.py`

- Backend full regression suite: passed
- Contract validation: passed with consolidated Flyway V1 schema and V2 demo data
- MySQL 8.4.11 validation: passed all 8 Flyway, JPA mapping, constraint, concurrency, and demo seed tests before and after merging the latest `develop`

## 미결 사항

- [COMPLETED] 교수자 예상 단어 GET/POST/DELETE API를 폐기하고 교안 편집을 `lesson-material` GET/PUT으로 통합한다.

- [COMPLETED] AI 분기 응답은 질문 `content`와 버튼 선택지 3개인 `branchPrompt`를 분리하고 Backend가 저장·조회한다. 교수자는 예상 단어를 입력하지 않고 생성된 교안 내용을 편집한다.
- [COMPLETED] 이미지 생성은 현재 동기 호출이므로 성공한 `image_url`만 저장하고 별도 상태 컬럼은 추가하지 않는다. 비동기 생성 도입 시 V3 이후 migration으로 보강한다.
- [ASSUMPTION] 이번 API는 기존 `story_scenes.image_url`과 `training_datas.generated_data` JSON을 사용해 호환 가능한 응답을 제공한다.
