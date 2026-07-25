---
type: Implementation Backlog
title: "Backend·Frontend 구현 백로그"
description: "AI server를 제외한 Backend와 교수자 Frontend·아동 App 구현 작업, 우선순위와 의존성을 관리합니다."
tags: [planning, implementation, backend, frontend, app, demo]
timestamp: 2026-07-25T00:00:00+09:00
---
# Backend·Frontend 구현 백로그

- 상태: active
- 최종 검토일: 2026-07-25
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
| BE-001 | P0 | Flyway V1과 엔티티 매핑 기준선 확정 | MySQL 24개 테이블, `training_contents`, `test_questions` | 없음 | done |
| BE-002 | P0 | Admin·App 인증 API를 Auth OpenAPI 10개 operation에 맞춤 | `auth-api.yaml` | BE-001 | in-progress |
| BE-003 | P0 | 역할과 리소스 소유권 검증 및 민감정보 로그 차단 | 인증, 학생·보고서·훈련 접근 | BE-002 | in-progress |
| BE-004 | P0 | 교수자·학생 관리 API 계약 정합화 | Admin `teacher`, `student` 12개 operation | BE-002, BE-003 | in-progress |
| BE-005 | P0 | 관리자 훈련·검사 API 계약 정합화 | Admin `training`, `test` 중 시선 조회를 제외한 13개 operation | BE-001, BE-004 | in-progress |
| BE-006 | P1 | 관리자 보고서·시선 결과 API 계약 정합화 | Admin `report` 4개, 검사·훈련 시선 조회 2개 operation | BE-004, BE-005 | in-progress |
| BE-007 | P0 | 아동 로그인·성장·마이페이지 API 구현 | App 인증, `student`, `mypage` | BE-002, BE-003 | in-progress |
| BE-008 | P0 | 아동 검사·훈련 세션 API 구현 | App `test` 8개, `training` 7개 operation | BE-001, BE-007 | todo |
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
- 작업별 테스트·빌드 실행은 사용자가 명시적으로 요청한 경우에만 수행하고 결과를 기록한다.

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
| FE-007 | `services/app` | P0 | 교수자·아동 로그인과 홈·성장·캐릭터 화면 구현 | Auth App, App `student`, `mypage` | FE-006, BE-007 | todo |
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
- 작업별 테스트·빌드 실행은 사용자가 명시적으로 요청한 경우에만 수행하고 결과를 기록한다.

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
- OpenAPI나 MySQL 계약 변경이 필요하면 구현에서 임의로 우회하지 않고 iRead 계약을 먼저 수정한다.
- 제품 탐색과 MVP 결정은 [제품 탐색 백로그](backlog.md)에서 별도로 관리한다.
