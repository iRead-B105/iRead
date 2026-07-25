---
type: Data Model
title: MySQL 데이터 모델
description: iRead MySQL 스키마의 소유권, 기준 원본과 검토 규칙을 설명합니다.
tags: [architecture, data-model, mysql, schema]
timestamp: 2026-07-24T00:00:00+09:00
---
# MySQL 데이터 모델

- 상태: proposed
- 최종 검토일: 2026-07-24

## 결정

주 데이터베이스는 [ADR-0006](../decisions/ADR-0006-mysql-primary-database.md)에 따라 MySQL 8.4.x LTS를 사용한다. [ADR-0008](../decisions/ADR-0008-demo-data-and-runtime-policy.md)에 따라 데모에서는 로컬 또는 Docker MySQL을 사용하고 운영 토폴로지와 백업·복구 인프라는 구성하지 않는다.

## 기준 원본과 스냅샷

- Backend 구현 전: [`contracts/database/schema.sql`](../../contracts/database/schema.sql)을 검토용 스키마 기준선으로 사용한다.
- Backend 구현 후: `services/backend`의 migration이 실행 가능한 기준 원본이다.
- ERD와 `schema.sql`은 migration 결과에서 생성하거나 동일 변경에서 동기화한다.
- [MySQL ERD](../../contracts/database/erd.md)는 `python tools/generate_erd.py`로 `schema.sql`에서 생성한다.
- API를 맞추기 위해 불필요한 컬럼을 추가하지 않고 기존 데이터 모델로 충족 가능한지 먼저 확인한다.

## 현재 이야기 진행 모델

- `stories.progress`는 AI 이야기 생성 요청에 전달할 현재 진행률 `0~100`을 저장한다.
- AI가 반환한 다음 진행률은 현재값 이상 `100` 이하인지 검증한다.
- 진행률이 `100`이면 `stories.status`를 `COMPLETED`로 변경한다.
- 생성된 `story_lines` 저장과 `stories.progress` 갱신은 하나의 트랜잭션으로 처리한다.
- `story_lines.requires_branch_input`은 아동 음성으로 AI 분기 생성을 시작해야 하는 장면인지 나타낸다.
- 미리 정의한 선택지와 분기 선택 상태는 저장하지 않는다.

## 정합성 제약

- 모든 명시적 연관관계는 외래 키로 보호한다.
- 교사 이메일, 단어 원형과 도메인별 순번처럼 중복되면 안 되는 값은 `UNIQUE` 제약으로 보호한다.
- `student_word_stats`는 임시 컬럼 대신 `student_id`와 `word_id`를 사용하며 학생·단어 조합을 유일하게 유지한다.
- 성취도, 단어 점수, 훈련·검사 정확도는 `0~100` 범위를 검사한다.
- 시선 세션은 `content_type`에 해당하는 검사·훈련·이야기 식별자 하나만 가진다.
- 보고서 기간은 `start_date <= end_date`를 만족해야 한다.

## 기존 컬럼으로 충족하는 기능

- 학습자 내부 메모는 `students.teacher_memo`를 사용한다.
- 보고서 교수자 의견은 `reports.teacher_memo`를 사용하고 생성 시각은 `reports.created_at`을 사용한다.
- 대표 캐릭터 선택을 위해 `character.is_representative`를 사용한다.

## 음성 데이터

음성 원본은 제한된 데모 환경의 `audio/{studentId}/{dataType}/` 구조에 저장한다. MySQL에는 내부 파일 경로를 API로 노출하지 않으며, 필요한 분석 결과와 메타데이터만 저장한다.

[ADR-0008](../decisions/ADR-0008-demo-data-and-runtime-policy.md)에 따라 음성 원본과 보고서의 장기 보관은 연구·분석 목적, 보관 기간, 접근 주체와 삭제 방법을 명시한 별도 동의를 받은 데이터에만 허용한다. 동의 철회 또는 명시한 기간 종료 시 원본과 연결 가능한 파생 데이터를 삭제한다.
