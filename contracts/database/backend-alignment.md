---
type: Contract Alignment
title: "Backend 엔티티와 MySQL 계약 정합화"
description: "Backend 최신 엔티티와 검토용 MySQL 스키마의 차이, migration 적용 순서와 결정 항목을 정리합니다."
tags: [contracts, backend, mysql, migration, alignment]
timestamp: 2026-07-24T00:00:00+09:00
---
# Backend 엔티티와 MySQL 계약 정합화

- 상태: active
- 비교 기준: Backend `origin/develop` `7d0e441`, `contracts/database/schema.sql`
- 최종 검토일: 2026-07-24

## 결론

[ADR-0007](../../docs/decisions/ADR-0007-okf-and-specification-sources.md)에 따라 승인된 계약을 기준으로 Backend 엔티티를 정합화하고, 동일 DDL을 Flyway `V1__baseline_schema.sql`로 관리한다. 계약 검증기는 두 파일이 다르면 실패한다.

## 확인된 차이

| 영역 | MySQL 계약 | Backend 최신 구현 | 처리 방향 |
| --- | --- | --- | --- |
| 기본 키 | `bigint` 기본 키 | `GenerationType.IDENTITY` | migration의 식별자 기본 키에 `AUTO_INCREMENT` 적용 |
| 검사 테이블 | `test` | `tests` | 예약어 충돌을 피하도록 `tests`로 통일 |
| 생성 콘텐츠 테이블 | `training_datas`, `test_datas` | 의미가 불명확한 복수형 | 실제 저장 내용에 맞춰 `training_contents`, `test_questions`로 통일 |
| 훈련 생성 데이터 FK | `training_id` | `train_id` | `training_id`로 통일 |
| 이야기 진행률 | `stories.progress` | 필드 없음 | Backend 엔티티에 0~100 진행률 추가 |
| 이야기 분기 표시 | `requires_branch_input` | `has_choices` | 음성 분기 의미인 `requires_branch_input`으로 통일 |
| 이야기 선택 저장 | 저장하지 않음 | `story_choices` 저장 | 로컬 데이터가 없음을 확인하고 엔티티와 저장소 제거 |
| 대표 캐릭터 | `is_representative` | 필드 없음 | Backend 엔티티와 대표 변경 로직 추가 |
| 단어 누적 통계 | `word_score`, `attempt_count` | 성공·실패·시도 횟수 | 점수 계산 기준과 보고서 소비 필드를 함께 정합화 |
| 단어 시도 로그 | 기본 시선·음성 필드 | `use_location`, 연결 자원, `total_score` 추가 | Backend가 사용하는 필드를 migration에 포함 |
| 보고서 기간 | `timestamp` | `LocalDate` | `DATE`로 통일 |

## 적용 결과

1. 식별자 기본 키를 `AUTO_INCREMENT PRIMARY KEY`로 정의하고 `tests`, `training_contents`, `test_questions`, `training_id`, `DATE` 등 물리 명칭과 타입을 Backend에 맞췄다.
2. `stories.progress`, `story_lines.requires_branch_input`, 대표 캐릭터와 단어 시도 로그 필드를 Backend에 반영했다.
3. Backend에 Flyway를 추가하고 `spring.jpa.hibernate.ddl-auto=validate`로 자동 DDL 생성을 막았다.
4. 빈 MySQL 8.4.10에서 V1을 실행해 테이블 24개, 외래 키 25개, UNIQUE 8개, CHECK 7개를 확인했다.
5. 이야기 분기 입력은 계약대로 저장하지 않으며 `story_choices` 엔티티와 저장소를 제거했다.

## 적용 경계

- 이번 V1은 신규·빈 데이터베이스 기준이다.
- 확인 당시 Docker의 `iread-mysql` 컨테이너와 관련 볼륨은 없었고, 호스트 MySQL에도 `iread` 스키마가 없어 변환할 로컬 개발 데이터가 없었다.
- 다른 환경에 기존 스키마나 `story_choices` 데이터가 있다면 V1을 직접 적용하지 않고 별도의 baseline 및 데이터 변환 migration을 먼저 작성해야 한다.
