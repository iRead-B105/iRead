---
type: Implementation Backlog
title: "Backend·Frontend 구현 백로그"
description: "AI server를 제외한 Backend와 교수자 Frontend·아동 App 구현 작업, 우선순위와 의존성을 관리합니다."
tags: [planning, implementation, backend, frontend, app, demo]
timestamp: 2026-07-27T00:00:00+09:00
---
# Backend·Frontend 구현 백로그

- 상태: active
- 최종 검토일: 2026-07-26
- 적용 범위: `services/backend`, `services/frontend`, `services/app`
- 계약 기준: [OpenAPI](../../contracts/openapi/index.md), [MySQL 스키마](../../contracts/database/index.md), [기능 카탈로그](../product/features/catalog/index.md)

## 범위

이번 구현 주기는 `BE`와 `FE` 두 작업 영역만 사용한다.

- `BE`: Backend API, 인증·권한, MySQL, 파일과 데모 데이터
- `FE`: 교수자 Frontend와 아동 App. 대상 저장소는 각 작업의 `경로` 열로 구분한다.
- AI server 구현과 `services/ai` 연동은 현재 범위에서 제외한다.
- AI 처리가 필요한 데모 흐름은 Backend의 `demo` profile에서 결정적인 fixture 응답으로 대체한다.
- Redis, 객체 스토리지, 운영 배포·고가용성과 Notion 재수집 자동화는 현재 백로그에 포함하지 않는다.

상태는 `todo`, `in-progress`, `blocked`, `done`, `deferred`를 사용한다. 컨트롤러나 화면 파일이 존재하는 것만으로 `done`으로 처리하지 않고 계약과 수용 기준을 충족한 뒤 완료한다.

## Backend TODO

| ID | 우선순위 | 작업 | 계약·영역 | 선행 작업 | 상태 |
| --- | --- | --- | --- | --- | --- |
| BE-001 | P0 | 확정 ERD 기준 Flyway V1과 엔티티 재정합화 | MySQL 23개 테이블, `training_datas`, `test_datas`, `test_curriculums`, 이야기 장면·선택 | 없음 | done |
| BE-002 | P0 | Admin·App 인증 API를 Auth OpenAPI 10개 operation에 맞춤 | `auth-api.yaml` | BE-001 | done |
| BE-003 | P0 | 역할과 리소스 소유권 검증 및 민감정보 로그 차단 | 인증, 학생·보고서·훈련 접근 | BE-002 | done |
| BE-004 | P0 | 교수자·학생 관리 API 계약 정합화 | Admin `teacher`, `student` 12개 operation | BE-002, BE-003 | done |
| BE-005 | P0 | 관리자 훈련·검사 API 계약 정합화 | Admin `training`, `test` 중 시선 조회를 제외한 13개 operation | BE-001, BE-004 | done |
| BE-006 | P1 | 관리자 보고서·시선 결과 API 계약 정합화 | Admin `report` 4개, 검사·훈련 시선 조회 2개 operation | BE-004, BE-005 | done |
| BE-007 | P0 | 아동 로그인·성장·마이페이지 API 구현 | App 인증, `student`, `mypage` | BE-002, BE-003 | done |
| BE-008 | P0 | 아동 검사·훈련 세션 API 구현 | App `test` 8개, `training` 7개 operation | BE-001, BE-007 | in-progress |
| BE-009 | P1 | 이야기·시선 세션 API 구현 | App `story` 9개, `gaze` 6개 operation | BE-007, BE-010 | in-progress |
| BE-010 | P0 | AI 없는 데모용 결정적 fixture provider 구현 | 훈련 생성·평가, 이야기, STT·TTS 대체 결과 | BE-001 | in-progress |
| BE-011 | P1 | 비식별 데모 seed와 파일·DB 초기화 절차 작성 | Flyway, 데모 데이터, `audio/` | BE-001 | in-progress |
| BE-012 | P1 | OpenAPI 기준 오류 응답과 입력 검증 통일 | Auth·Admin·App 전체 | BE-002~BE-010 | in-progress |

### 2026-07-25 Backend 구현 검토

- 검토 기준: Backend `develop`의 `ea07f82`, OpenAPI 74개 operation, Flyway V1과 엔티티 매핑
- API 경로·HTTP method가 정확히 일치하는 컨트롤러 매핑: 38/74
  - Auth: 0/10. 기존 교수자 세션 인증이 있으나 Admin·App JWT 계약과 경로·요청 모델이 다르다.
  - Admin: 25/31. 교수자·학생 9/12, 훈련·검사 11/13, 보고서·시선 5/6이 일치한다.
  - App: 13/33. 이야기·시선 12/15와 마이페이지 캐릭터 조회 1개가 일치한다.
- `BE-001`은 Flyway V1과 계약 SQL의 일치, 24개 테이블·25개 외래 키 및 필수 엔티티 매핑을 확인해 완료로 변경했다.
- 기존 구현이 있으나 계약 전체를 충족하지 않는 작업은 `in-progress`로 변경했다. 파일이나 메서드의 존재만으로 완료 처리하지 않았다.
- 아동 검사·훈련 컨트롤러는 아직 없으므로 `BE-008`은 `todo`를 유지한다.
- 이번 정합화에서 공통 성공·오류 응답 envelope, 회원가입·보고서 생성·시선 세션·이야기 세션의 HTTP 상태, 보고서 메모 경로와 응답, 학생 수정의 교수자 메모, 이야기 장면 경로 변수를 계약에 맞췄다.
- 남은 주요 차이는 Admin·App JWT 인증, 오류별 HTTP 상태와 세부 코드, 기존 조회 API의 목록 wrapper·일부 응답 필드명, 학생 요약·학습 이벤트, 훈련 상세·내보내기, 보고서 시선 반영, 성장·대표 캐릭터, 이야기 분기·STT·TTS와 App 검사·훈련 API다.

### Backend 수용 기준

- 각 작업에 연결된 OpenAPI 경로, method, 요청·응답과 오류 상태가 구현과 일치한다.
- App·Admin 요청은 인증, 역할과 해당 학생·리소스 소유권을 검증한다.
- 토큰, 비밀번호, 이름, 연락처, 음성 파일 경로·URL과 요청 본문을 로그에 기록하지 않는다.
- 빈 MySQL에서 Flyway V1과 비식별 seed로 동일한 데모 상태를 만들 수 있다.
- `demo` profile은 `services/ai` 실행 없이 동일 입력에 동일한 결과를 반환한다.
- 작업별 관련 테스트 코드를 추가·수정하고 테스트 성공을 확인한 뒤 결과를 기록한다.

### 2026-07-26 BE-002 완료

- Auth OpenAPI의 Admin 6개·App 4개 operation을 구현하고 기존 HTTP session 인증을 audience 분리 JWT 인증으로 교체했다.
- Access token은 Admin 15분, 학습 App 15분, 아동 선택용 bootstrap token 5분으로 발급하며 refresh token은 14일 동안 유효하다.
- Refresh token 원문은 HttpOnly cookie로만 전달하고 MySQL에는 SHA-256 해시를 저장하며 rotation 시 이전 세션을 폐기한다.
- 로그아웃 시 refresh session을 폐기하며 이미 발급된 access token은 최대 15분의 남은 유효 시간까지 허용한다.
- MVP demo 비밀번호 재설정은 `AUTH_DEMO_VERIFICATION_CODE` 환경변수를 사용하며 외부 메일 발송은 범위에서 제외한다.
- `teachers.email`을 유일한 로그인 식별자로 사용하고 `auth_refresh_sessions`를 단일 Flyway V1과 계약 SQL·ERD에 동기화했다.
- 인증 서비스·JWT·refresh rotation 테스트 12개를 추가하고 Backend 전체 테스트를 실행했다.
- `.\gradlew.bat test --rerun-tasks`: 68개 중 일반 테스트 67개 성공, opt-in MySQL 통합 테스트 1개 skip, 실패 0개.
- DB 적용 전 인증 스키마를 단일 V1으로 통합했으며 MySQL 8.4와 JPA mapping validation 재검증이 필요하다.
- `python -m unittest tools.tests.test_validate_contracts`: 1개 성공.
- `python tools/validate_contracts.py`: 81 operations, 334 features, 25 MySQL tables, 27 foreign keys 검증 성공.
- `python tools/validate_harness.py`: 82 Markdown files, 63 OKF concepts, 92 explicit open markers 검증 성공.
- 별도 린트·정적 분석은 구성된 명령이 없어 실행하지 않았다.

### 2026-07-26 BE-003 완료

- JWT principal에서 `TEACHER` 역할은 Admin·bootstrap audience와 학생 식별자 없음, `STUDENT` 역할은 learning audience와 학생 식별자 있음을 불변식으로 검증한다.
- 학습 App의 마이페이지·이야기·시선 API에서 토큰의 `studentId`와 경로·쿼리·요청 본문의 `studentId`가 같은지 서비스 호출 전에 검사한다.
- Admin API는 Admin audience, 학습 App API는 learning audience로 분리하고 서로 다른 영역의 토큰 접근이 `403 Forbidden`인지 HTTP 통합 테스트로 확인했다.
- 학생·훈련·검사·보고서·이야기·시선 서비스가 교수자와 학생 또는 하위 리소스의 연결 관계를 제한하는 저장소 조회를 사용하는지 확인했다.
- 제품 범위에서 제거된 `/api/admin/report/shared/**` 익명 접근 허용 규칙을 삭제했다.
- 요청 상세 로그와 Tomcat access log를 명시적으로 비활성화하고 직접 콘솔 출력 금지 회귀 테스트를 추가했다.
- 역할·audience, 아동 리소스 접근, 보안 HTTP 응답과 로그 정책 테스트 17개를 추가했다.
- `.\gradlew.bat test --rerun-tasks`: 85개 중 일반 테스트 84개 성공, opt-in MySQL 통합 테스트 1개 skip, 실패 0개.
- 데이터베이스 스키마와 엔티티 매핑 변경이 없어 MySQL 통합 테스트는 별도로 실행하지 않았다.
- 별도 린트·정적 분석은 구성된 명령이 없어 실행하지 않았다.

### 2026-07-27 확정 ERD 교체

- 사용자가 ERDCloud에서 확정한 23개 테이블 설계로 MySQL 계약과 단일 Flyway V1을 교체했다.
- `story_scenes`, `story_choices`, `test_curriculums`를 포함하고 이전 초안의 누적 통계·학습 진도 테이블과 대표 캐릭터 플래그를 제거했다.
- 검사, 이야기, 시선, 보고서와 캐릭터 매핑이 현재 Backend 엔티티와 달라 `BE-001`을 `in-progress`로 되돌렸다.
- 대표 캐릭터 변경 API를 제거하고 관련 표시 상태를 클라이언트 책임으로 변경했다.
- 성장 API는 완료된 훈련을 학생·훈련 템플릿별로 실시간 집계한 `completedCount`를 반환하고, 클라이언트는 매회 한 단계씩 성장시켜 5회에 만개하도록 변경했다.
- 음성 분기 API는 최종 STT 텍스트를 `story_choices`에 한 건 저장하고 다음 장면·대사·진행률과 함께 반영한다. 같은 분기 대사의 재시도는 최초 결과를 `200 OK`로 반환한다.
- Backend 엔티티 정합화와 MySQL 8.4.10 실행 검증을 완료해 `BE-001`을 `done`으로 변경했다.
- 계약 검증은 23개 테이블·31개 외래 키 기준으로 성공했고 문서 하네스도 성공했다.
- 공식 MySQL 8.4.10 ZIP의 일회성 서버에서 빈 테스트 DB를 생성하고 Flyway V1 전체 적용과 Hibernate schema validation을 완료했다.
- MySQL 통합 테스트는 애플리케이션 테이블 23개, 외래 키 31개, UNIQUE 11개, CHECK 7개와 핵심 물리 명칭을 검증한다.

### 2026-07-27 교수자 앱 Backend 순차 구현

- `services/frontend` 변경은 롤백했고, 이후 작업은 Backend와 루트의 Backend submodule 포인터·현황 문서로 제한했다.
- `BE-004`: 교수자 정보와 학생 관리 12개 operation의 경로, 소유권, 목록 검색·나이·최근 학습 필터, 요약, 정확도·읽기 속도 추이, 훈련 이력 기간 필터, 학습 요약과 추천 규칙을 구현했다.
- 학생 등록·상세는 기존 `birthday`, `guardian`, `guardianContact`, `imageUrl`과 OpenAPI의 `birthDate`, `guardianName`, `guardianPhone`, `profileImage`를 함께 처리한다. 상세의 `studentCode`는 서버의 `studentId` 문자열로 반환하고 배열형 주소 입력도 기존 문자열 컬럼에 호환 저장한다.
- `get_admin_student_by_studentId_learning_events`는 필수 `eventType(test|training|story|gaze)`과 `eventId` 조합으로 원본 테이블을 구분하며 네 유형을 모두 조회한다.
- 최종 계약 감사에서 훈련 이력의 잘못된 필수 `trainingRecord`를 선택 `from`·`to` 날짜 query로 교체하고, 교수자 조회의 이미지 필드를 `profileImageUrl`로 통일했다.
- `BE-005`: 관리자 훈련·검사 목록 wrapper와 응답 필드, 커리큘럼 상세·수정, 훈련 상세, JSON·CSV 동기 다운로드, 검사 비교 계약을 구현했다.
- `BE-006`: 보고서 목록·생성·상세·메모·시선 분석 반영과 검사·훈련 시선 결과 조회 계약을 구현했다. 제거된 `student_word_stats` 대신 `word_attempt_logs`를 보고서 기간별로 집계한다.
- `BE-012`: 관리자 범위의 `400`, `401`, `403`, `404`, `409`, `500` 오류 응답과 입력 검증을 통일했다. Auth·App 전체 범위가 남아 있어 작업 상태는 `in-progress`를 유지한다.
- 확정 ERD의 검사 커리큘럼, 보고서 기간 timestamp, 시선 원시 데이터, 훈련 정확도, 캐릭터와 이야기 장면 관계를 Backend 엔티티에 반영했다. 엔티티가 생성하는 모든 테이블의 컬럼 집합을 Flyway V1과 비교하는 회귀 테스트를 추가했다.
- Admin OpenAPI 31개 operation의 경로·HTTP method 회귀 테스트를 추가했다.
- MySQL 통합 검증을 활성화한 `.\gradlew.bat test --rerun-tasks`: 119개 전체 성공, skip·실패 0개.
- `python tools/validate_contracts.py`: 80 operations, 334 features, 73 reviewed, 23 MySQL tables, 31 foreign keys 검증 성공.
- `python tools/validate_harness.py`: 82 Markdown files와 31 record docs 검증 성공.
- 공식 MySQL 8.4.10 ZIP을 임시 런타임으로 사용해 빈 DB Flyway 적용, 23개 애플리케이션 테이블·31개 외래 키와 Hibernate 엔티티 매핑을 검증했다.

### 2026-07-27 BE-007 완료

- App 인증 4개 operation은 `BE-002`에서 완료한 learning audience JWT와 refresh rotation을 사용한다.
- 캐릭터 목록은 query parameter 없이 학습 토큰의 `studentId`를 사용하며 `characterId`, `storyId`, `imageUrl`, `name`, `createdAt`을 `characters` 목록으로 반환한다.
- 잘못된 캐릭터 `EntityGraph("image")`를 실제 연관관계인 `story`로 수정하고 영속성 통합 테스트로 조회를 검증했다.
- 성장 조회는 완료된 `trainings`를 학생·훈련 템플릿별로 집계해 `trainingTemplateId`, `trainingTemplateName`, `completedCount`를 반환한다.
- 학습 토큰과 성장 조회 경로의 학생이 다르면 서비스 호출 전에 `403 Forbidden`으로 차단하며, 교수자 소유 관계가 없으면 `404 Not Found`로 처리한다.
- `.\gradlew.bat test --rerun-tasks`: 126개 중 일반 테스트 125개 성공, opt-in MySQL 통합 테스트 1개 skip, 실패 0개.
- `python tools/validate_contracts.py`: 80 operations, 334 features, 73 reviewed, 23 MySQL tables, 31 foreign keys 검증 성공.
- `python tools/validate_harness.py`: 82 Markdown files와 31 record docs 검증 성공.
- DB 스키마 변경이 없어 MySQL 통합 테스트는 다시 실행하지 않았다.

### 2026-07-27 BE-008 훈련 세션 구현

- App 훈련 7개 operation을 별도 이력 식별자 없이 `trainings.id`를 세션 식별자로 사용하는 ERD 중심 계약으로 정리했다.
- 안내·문항은 `training_datas.generated_data`를 조회하고, 선택·녹음 응답은 `word_attempt_logs.training_id`에 저장한다.
- 시작·초기화·완료는 `trainings.status`, `started_at`, `finished_at`, `result`, `accuracy`를 갱신하며 학습 토큰과 학생·훈련 소유권을 검증한다.
- 검사 세션 8개 operation이 남아 있으므로 `BE-008`은 `in-progress`를 유지한다.
- `.\gradlew.bat test --rerun-tasks`: 129개 중 일반 테스트 128개 성공, opt-in MySQL 통합 테스트 1개 skip, 실패 0개.
- `python tools/validate_contracts.py`: 80 operations, 334 features, 73 reviewed, 23 MySQL tables, 31 foreign keys 검증 성공.
- `python tools/validate_harness.py`: 82 Markdown files와 31 record docs 검증 성공.
- DB 스키마 변경은 없으며 기존 ERD의 `trainings`, `training_datas`, `word_attempt_logs`만 사용한다.

## Frontend TODO

`FE`는 하나의 관리 영역이며 교수자용 화면은 `services/frontend`, 아동용 화면은 `services/app`에서 구현한다.

| ID | 경로 | 우선순위 | 작업 | 계약·영역 | 선행 작업 | 상태 |
| --- | --- | --- | --- | --- | --- | --- |
| FE-001 | `services/frontend` | P0 | Vue 3·TypeScript·Vite·pnpm 애플리케이션 기반 구성 | 라우팅, 상태, API client, 환경변수 | 없음 | todo |
| FE-002 | `services/frontend` | P0 | 교수자 인증과 공통 레이아웃 구현 | Auth Admin operation | FE-001, BE-002 | todo |
| FE-003 | `services/frontend` | P0 | 학생 목록·요약·등록·상세·수정 화면 구현 | Admin `student`, `teacher` | FE-002, BE-004 | todo |
| FE-004 | `services/frontend` | P0 | 훈련 교안·이력·통계와 검사 비교 화면 구현 | Admin `training`, `test` | FE-003, BE-005 | todo |
| FE-005 | `services/frontend` | P1 | 보고서·시선 결과·교수자 프로필 화면 구현 | Admin `report`, gaze, `teacher` | FE-003, FE-004, BE-006 | todo |
| FE-006 | `services/app` | P0 | 아동 App 기술 스택 확정과 애플리케이션 기반 구성 | 라우팅, 상태, API client, 미디어 권한 | 없음 | todo |
| FE-007 | `services/app` | P0 | 교수자 로그인·연결 아동 프로필 선택과 홈·성장·캐릭터 화면 구현 | Auth App, App `student`, `mypage` | FE-006, BE-007 | todo |
| FE-008 | `services/app` | P0 | 검사·훈련 안내, 문항, 녹음·응답과 완료 흐름 구현 | App `test`, `training` | FE-007, BE-008 | todo |
| FE-009 | `services/app` | P1 | 이야기 책장·읽기·분기·음성 재생 흐름 구현 | App `story` | FE-007, BE-009, BE-010 | todo |
| FE-010 | `services/app` | P1 | 시선 장치 안내, 세션 시작·종료·실패 흐름 구현 | App `gaze` | FE-006, BE-009 | todo |
| FE-011 | 두 저장소 | P1 | 공통 로딩·빈 상태·오류·재인증 UX 정리 | 공통 오류 응답, 401·403·404·409 | FE-002, FE-007, BE-012 | todo |
| FE-012 | 두 저장소 | P1 | 핵심 데모 시나리오와 접근성·반응형 마무리 | 교수자 관리, 아동 검사·훈련·이야기 | FE-003~FE-011 | todo |

### Frontend 수용 기준

- 화면 요청은 해당 OpenAPI `operationId`와 추적할 수 있다.
- 로딩, 빈 결과, 검증 실패, 인증 만료와 서버 오류 상태를 처리한다.
- 교수자 Frontend와 아동 App의 토큰·환경변수·API URL을 소스에 하드코딩하지 않는다.
- 아동 App은 마이크·시선 장치 권한 거부와 장치 미지원 상태를 사용자에게 설명한다.
- `services/ai` 없이 Backend `demo` profile만으로 핵심 시나리오를 시연할 수 있다.
- 작업별 관련 테스트 코드를 추가·수정하고 테스트 성공을 확인한 뒤 결과를 기록한다.

## 구현 순서

1. `BE-001`, `BE-010`, `FE-001`, `FE-006`
2. `BE-002`, `BE-003`, `FE-002`
3. `BE-004`, `BE-007`, `FE-003`, `FE-007`
4. `BE-005`, `BE-008`, `FE-004`, `FE-008`
5. `BE-006`, `BE-009`, `BE-012`, `FE-005`, `FE-009`, `FE-010`
6. `BE-011`, `FE-011`, `FE-012`

## 관리 규칙

- 이 문서는 서비스 간 우선순위, 의존성과 상태의 기준 문서다.
- 세부 구현이 한 번에 검토하기 어려우면 [작업 템플릿](../templates/task.md)으로 별도 계획을 작성하거나 해당 서비스 저장소의 GitHub Issue에 연결한다.
- 상태를 변경할 때 구현 PR 또는 커밋, 검증 결과와 남은 차단 요인을 함께 기록한다.
- 구현과 필수 테스트가 모두 완료되고 테스트 결과가 기록된 뒤에만 상태를 `done`으로 변경한다.
- OpenAPI나 MySQL 계약 변경이 필요하면 구현에서 임의로 우회하지 않고 iRead 계약을 먼저 수정한다.
- 제품 탐색과 MVP 결정은 [제품 탐색 백로그](backlog.md)에서 별도로 관리한다.
