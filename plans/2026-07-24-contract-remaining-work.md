---
type: Execution Plan
title: "기능·API·MySQL 계약 후속 작업"
description: "Notion에서 이전한 기능·API 계약과 MySQL 스키마를 구현 가능한 상태로 마무리하기 위한 남은 작업을 정리합니다."
tags: [plan, contracts, notion, openapi, mysql]
timestamp: 2026-07-24T00:00:00+09:00
---
# 기능·API·MySQL 계약 후속 작업

- 상태: completed
- 담당: Codex
- 작성일: 2026-07-24
- 수정일: 2026-07-25
- 완료 판정: 구현 전 계약과 데모 실행 정책 확정 완료. 실제 운영 준비는 현재 제품 범위에서 제외하고 선택 작업만 후속 개선 범위로 유지한다.

## 기대 결과

검수 대기 API가 서버 계약, 기존 API 통합 또는 클라이언트 책임으로 확정되고 Backend–AI 계약과 MySQL migration이 실행 가능한 기준 원본으로 관리된다.

## 현재 상태

- Notion 활성 API 115건과 기능 334건을 저장소로 이전했다.
- 계약 검증 기준으로 외부 API 74건 모두 검토 완료했다.
- Backend–AI 내부 API 7건을 별도 OpenAPI 계약으로 관리한다.
- MySQL 8.4.x LTS 스키마는 테이블 24개와 외래 키 25개를 포함한다.
- Backend는 계약 스키마와 동일한 Flyway V1을 사용하며 Hibernate는 스키마를 검증만 한다.
- 생성 콘텐츠 테이블은 기존 SQL 물리 명칭인 `training_datas`, `test_datas`를 사용한다.
- App·Admin·Auth OpenAPI의 성공·오류 응답은 공통 `components`를 사용한다.
- MySQL ERD는 스키마 계약에서 Mermaid 문서로 자동 생성한다.
- 별도 이야기 진행률·완료 API는 음성 분기 생성 API로 통합했다.
- `우선순위`와 `구현여부` Notion 속성은 이관 스냅샷 수집 범위에서 제외했다.

## 필수 작업

### 구현 전

- [x] 기존 API와 중복된 22건을 정식 도메인 API로 통합한다.
- [x] 화면 이동·선택·재생 상태 등 클라이언트 책임 API 11건을 활성 서버 계약에서 제거한다.
- [x] 서버 계약 상세화 대상 14건의 요청·응답, 타입, 필수 여부와 오류 코드를 확정한다.
- [x] 경로 정규화 대상 3건을 REST 명령 의미에 맞게 수정한다.
- [x] 검사·훈련의 초기화와 제출 계약 2건을 정리한다.
- [x] 변경한 OpenAPI, 기능 카탈로그와 추적 데이터를 다시 생성하고 검증한다.
- [x] Notion에서 Git으로 단방향 이전하며 확정 계약을 외부 Notion에 역동기화하지 않는다.
- [x] STT, 이야기 생성, 진행률 반환, TTS와 시선 분석을 포함하는 Backend–AI 내부 API를 정의한다.
- [x] 현재 스키마를 Backend의 Flyway migration으로 이전한다.
- [x] MySQL 8.4.x에서 migration과 제약조건을 실제 실행 검증한다.

### 데모 실행 전

- [x] 음성 파일과 보고서의 장기 보관을 별도 동의 범위로 제한하고 경로 접근 기준을 확정한다.
- [x] 동의서에 데이터셋별 보관 기간, 철회와 삭제 방법을 명시하도록 확정한다.
- [x] 로컬·Docker MySQL을 사용하고 운영 백업·복구와 고가용성 구성을 제외한다.
- [x] 기본 인증·역할·리소스 소유권 검증과 로그 개인정보 제거 기준을 확정한다.

## 선택 작업

- [x] SQL 생성 콘텐츠 테이블 명칭은 `training_datas`, `test_datas`로 유지한다.
- [x] OpenAPI 공통 성공·오류 스키마와 오류 응답을 `components`로 추출한다.
- [x] `schema.sql`에서 Mermaid ERD 문서를 자동 생성한다.
- [ ] 명시적으로 요청된 Notion 원본 변경의 재수집과 API 호환성 검사를 자동화한다.
- [ ] Redis 역할과 아동 앱 기술 스택을 확정한다.
- [ ] 음성 파일을 EC2 로컬 디스크에서 객체 스토리지로 이전하는 방안을 검토한다.

## 확인이 필요한 사항

- 33건의 API 통합·제거는 [API 검토 목록](../contracts/review-queue.md)의 권장안을 적용한다.
- 나머지 19건에서 ERD만으로 결정할 수 없는 제품 동작이 발견될 때만 사용자에게 질문한다.
- migration 도구는 Backend 초기 구조와 함께 Flyway와 Liquibase 중 하나를 선택한다.

## 예상 소요

- 기능·API·SQL 명세 완료: 6~10시간
- Backend migration 작성과 MySQL 실행 검증: 추가 1~2일
- 운영·보안 정책 문서화: 추가 0.5~1일

## 검증

- `python tools/validate_contracts.py`
- `python tools/validate_harness.py`
- `git diff --check`
- MySQL migration 도입 후 MySQL 8.4.x 임시 환경에서 전체 migration 실행

## 진행 기록

- 2026-07-24: 기능 334건, 활성 API 115건과 MySQL 스키마 기준선을 확립했다.
- 2026-07-24: 검수 대기 API 52건을 처리 성격별로 분류했다.
- 2026-07-24: Git 기반 `api-resolutions.json`을 도입해 중복 API 22건을 통합하고 클라이언트 책임 API 11건을 제거했다.
- 2026-07-24: 검사 비교, 성장 조회, 이야기 책장, 시선 분석과 훈련 완료 계약을 통합하고 외부 API를 74건으로 정리했다.
- 2026-07-24: `X-API-Key`, `Idempotency-Key`, 30초 처리 제한과 1회 조건부 재시도를 사용하는 Backend–AI 내부 API 7건을 정의했다.
- 2026-07-24: 계약 스키마와 동일한 Flyway V1을 추가하고 MySQL 8.4.10에서 테이블 24개, 외래 키 25개, UNIQUE 8개, CHECK 7개를 실행 검증했다.
- 2026-07-24: 로컬 기존 DB 데이터가 없음을 확인하고 이야기 선택 저장 모델을 제거했으며 진행률·음성 분기 필드를 Backend–AI 계약에 맞췄다.
- 2026-07-24: 기능 원문을 근거로 검사·훈련의 미완료 세션 초기화 계약을 확정하고 검수 대기 API를 2건으로 줄였다.
- 2026-07-24: 학생 요약을 전체 담당 아동 수와 오늘 학습 예정 수 집계로 정규화해 검수 대기 API를 1건으로 줄였다.
- 2026-07-24: 이전 계획·ADR·계약 카탈로그의 OpenAPI, Backend–AI와 Flyway 상태를 현재 기준선으로 갱신했다.
- 2026-07-24: 현재 Flyway V1을 빈 MySQL 8.4.10에 다시 적용해 테이블·제약조건과 핵심 컬럼 타입을 재검증했다.
- 2026-07-24: 승인된 고정 규칙으로 주의 필요·권장 훈련 계약을 확정해 외부 API 74건의 검토를 모두 완료했다.
- 2026-07-24: Notion은 이관 출처로만 보존하고 Git 계약을 외부 Notion에 역동기화하지 않기로 확정했다.
- 2026-07-24: 데모 전용 범위를 확정하고 별도 동의 데이터의 장기 보관, 로컬·Docker MySQL과 기본 API 보안 기준을 ADR-0008로 기록했다.
- 2026-07-25: 생성 콘텐츠 테이블을 `training_contents`, `test_questions`로 정리하고 Flyway·엔티티·계약 SQL을 동기화했다.
- 2026-07-27: 위 명칭 변경은 ADR-0011로 대체했으며 확정 ERD의 `training_datas`, `test_datas`, `train_id`를 다시 기준으로 채택했다.
- 2026-07-27: DB 적용 전 사용자 결정에 따라 생성 콘텐츠 테이블과 FK를 `training_datas`, `test_datas`, `train_id`로 되돌려 유지했다.
- 2026-07-27: 인증 스키마를 단일 V1에 통합하고 refresh session만 저장하며 access token 폐기 테이블은 사용하지 않기로 확정했다.
- 2026-07-27: 교수자 로그인 식별자를 별도 `login_id` 없이 `teachers.email` 하나로 통일했다.
- 2026-07-27: 이야기 분기 여부의 DB 물리 컬럼은 기존 SQL 명칭인 `story_lines.has_choices`를 유지하고 API 의미는 `requiresBranchInput`으로 분리했다.
- 2026-07-25: App·Admin·Auth OpenAPI의 성공·오류 응답을 공통 `components`로 추출했다.
- 2026-07-25: MySQL 스키마의 테이블 24개와 외래 키 25개를 Mermaid ERD로 자동 생성하는 도구와 문서를 추가했다.

## 결정 및 변경 사항

- [ADR-0006](../docs/decisions/ADR-0006-mysql-primary-database.md)에 따라 MySQL 8.4.x LTS를 사용한다.
- [ADR-0007](../docs/decisions/ADR-0007-okf-and-specification-sources.md)에 따라 저장소 계약을 구현 기준 원본으로 관리한다.
- [ADR-0008](../docs/decisions/ADR-0008-demo-data-and-runtime-policy.md)에 따라 데모 데이터 보관, MySQL 실행 환경과 API 보안 범위를 관리한다.
- Notion 스냅샷은 수정하지 않고 [API 해소 규칙](../contracts/api-resolutions.json)을 적용해 저장소 계약과 기능 추적을 재생성한다.
- Notion 페이지는 이관 출처 추적용이며 별도 요청이 없는 한 Git 변경을 역동기화하지 않는다.

## 남은 위험

- 다른 환경에 기존 스키마나 `story_choices` 데이터가 있으면 별도 baseline 및 변환 migration이 필요하다.
- 별도 동의서에 데이터셋별 보관 기간이 명시되지 않으면 해당 음성 원본과 보고서를 장기 보관할 수 없다.
- 실제 운영으로 전환하려면 MySQL 백업·복구, 고가용성, 수치화한 보관 기간과 감사 정책을 새로 결정해야 한다.
