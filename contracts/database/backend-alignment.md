---
type: Contract Alignment
title: "Backend 엔티티와 MySQL 계약 정합화"
description: "2026-07-28 확정 ERD와 Backend 엔티티의 차이, V1 적용 경계와 후속 정합화 범위를 정리합니다."
tags: [contracts, backend, mysql, migration, alignment, erd]
timestamp: 2026-07-27T00:00:00+09:00
---
# Backend 엔티티와 MySQL 계약 정합화

- 상태: active
- 비교 기준: 2026-07-28 확정 ERD, `contracts/database/schema.sql`, 현재 Backend 작업 트리
- 최종 검토일: 2026-07-28

## 결론

사용자가 확정한 25개 테이블 ERD를 현재 MySQL 계약으로 채택했다. 실행 가능한 DDL은 Flyway `V1__baseline_schema.sql`에 반영하고 `contracts/database/schema.sql`과 동일하게 유지한다.

Backend 엔티티를 현재 계약에 맞춰 정합화했고 공식 MySQL 8.4.10의 빈 데이터베이스에서 Flyway V1과 Hibernate schema validation을 완료했다.

## 확정된 물리 명칭

- `training_datas`
- `train_id`
- `test_datas`
- `tests`
- `story_lines.has_choices`
- `teachers.email`
- `auth_refresh_sessions`
- `training_templates.prompt`
- `reading_features`
- `student_feature_profiles.reading_features_id`
- `student_feature_profiles.avg_pronunciation_scor`

`training_contents`, `training_id`로의 물리 FK 변경, `test_questions`, `requires_branch_input`, `teachers.login_id`, `auth_revoked_access_tokens`는 사용하지 않는다.

## 이전 기준선에서 변경된 구조

| 영역 | 확정 계약 | Backend 정합화 방향 |
| --- | --- | --- |
| 이야기 계층 | `stories → story_scenes → story_lines → story_choices` | 장면과 선택지 엔티티·저장소·서비스 흐름을 복원하거나 추가 |
| 이야기 대사 FK | `story_lines.scene_id` | 기존 `story_id`, `previous_line_id`, 대사별 이미지 매핑 제거 |
| 캐릭터 | 학생과 이야기 FK, 이름·이미지 | `is_representative` 기반 구현과 대표 캐릭터 변경 API 제거 |
| 검사 커리큘럼 | `test_curriculums` 추가 | 학생별 검사 커리큘럼과 순서 기반 검사 엔티티 추가 |
| 검사 | `test_curriculum_id`, `training_template_id`, 세션 시각과 순서 | 기존 학생 직접 FK 기반 검사 엔티티 교체 |
| 검사 생성 데이터 | `id bigint`, `generated_data`, `created_at` | 기존 질문 ID·질문 JSON 매핑 교체 |
| 시선 세션 | 조건부 대상 FK와 `data` JSON | 원시 시선 데이터 컬럼 및 조건부 관계 반영 |
| 보고서 | 기간 `timestamp`, nullable `snapshot_data` | `LocalDate` 및 필수 snapshot 매핑 교체 |
| 누적 통계 | 별도 누적 통계 테이블 없음 | `student_word_stats`, `student_study_progresses` 매핑 제거 |
| 훈련 점수 | `accuracy` 0~1000 | 기존 0~100 소수 정밀도 매핑 교체 |
| 훈련 생성 프롬프트 | `training_templates.prompt` text | 기존 `form` JSON 컬럼을 최종 ERD 명칭으로 교체 |
| 읽기 특징 | `reading_features` 자기 참조 계층 | 자모·음절·음운·형태·단어·문장 특징 사전 추가 |
| 학생 특징 프로필 | `student_feature_profiles` | 학생·읽기 특징별 집계 지표와 취약도·신뢰도 저장 |

- 확정 ERD에 대표 캐릭터 상태가 없으므로 대표 캐릭터 변경 API를 제거하고 관련 표시 상태는 클라이언트 책임으로 변경했다.
- `story_choices.content`에는 음성 입력을 STT로 복원한 최종 텍스트를 저장한다. `story_line_id`를 UNIQUE로 보호하고 STT 중간 실패는 저장하지 않는다. 같은 분기 대사의 재시도는 최초 저장 결과를 반환한다.
- 성장 정보는 별도 컬럼 없이 완료된 `trainings` 행을 학생·훈련 템플릿별로 실시간 집계한다. 클라이언트는 `min(completedCount, 5)`로 성장 단계를 계산하며 5회에 만개 상태가 된다.

## V1 변환 규칙

- ERDCloud COMMENT의 `AUTO_INCREMENT`, `UNIQUE`, `DEFAULT`, `CHECK`는 실행 DDL의 실제 속성·제약조건으로 변환했다.
- 관계선은 34개 외래 키로 변환했다.
- FK에 복사된 `AUTO_INCREMENT` 메모는 적용하지 않았다.
- `test_curriculums.id`, `test_datas.id`는 확정 ERD에 자동 증가 표시가 없으므로 일반 `bigint` PK로 유지했다.
- `reading_features.id`, `student_feature_profiles.id`도 확정 ERD에 자동 증가 표시가 없으므로 일반 `bigint` PK로 유지했다.
- `gaze_analysis_results.gaze_session_id`는 시선 세션당 분석 결과 하나를 보장하도록 UNIQUE로 보호했다.
- `story_choices.story_line_id`는 분기 대사당 최종 선택 하나를 보장하도록 UNIQUE로 보호했다.

## 적용 경계

- 이번 V1은 신규·빈 데이터베이스 기준이다.
- 신규·빈 데이터베이스 기준선이므로 V2를 만들지 않고 V1을 유지한다.
- Backend 엔티티와 저장소 정합화를 완료했으며 Hibernate schema validation이 MySQL 8.4.10에서 통과한다.
- 다른 환경에 기존 스키마나 데이터가 있으면 V1을 직접 적용하지 않고 별도 baseline 및 데이터 변환 migration을 작성해야 한다.

## 인증 계약

- 교사 로그인 식별자는 `teachers.email` 하나다.
- `auth_refresh_sessions`만 사용하고 access token 폐기 테이블은 사용하지 않는다.
- Admin 세션은 `student_id`가 NULL이고 학습 세션은 학생에 연결한다.
- refresh token 원문은 저장하지 않고 SHA-256 해시만 저장한다.

## 후속 검증

- 기존 스키마나 데이터가 있는 환경에 적용할 때는 별도 baseline과 데이터 변환 migration을 검증한다.
- V1을 변경하면 빈 MySQL에서 통합 테스트를 다시 실행한다.

## 2026-07-27 검증 결과

- `python -m unittest tools.tests.test_validate_contracts`: 3개 성공
- `python tools/generate_erd.py --check`: 성공
- `python tools/validate_contracts.py`: 80 operations, 334 features, 23 MySQL tables, 31 foreign keys 검증 성공
- `python tools/validate_harness.py`: 82 Markdown files와 31 record documents 검증 성공
- 공식 MySQL 8.4.10 ZIP으로 일회성 서버를 시작하고 빈 테스트 DB에 Flyway V1 전체 적용 성공
- Hibernate `ddl-auto=validate`: MySQL 8.4.10에서 성공
- MySQL 제약 검증: 애플리케이션 테이블 23개, 외래 키 31개, UNIQUE 11개, CHECK 7개
- MySQL 통합 검증을 활성화한 `.\gradlew.bat test --rerun-tasks`: Java 21에서 119개 전체 성공, skip·실패 0개

## 2026-07-28 계약 갱신

- 확정 ERD의 `reading_features`, `student_feature_profiles`를 V1과 JPA 엔티티에 추가했다.
- `training_templates.form`을 최종 ERD 물리 명칭인 `prompt` text로 교체했다.
- 스키마 규모는 애플리케이션 테이블 25개, 외래 키 34개, UNIQUE 11개, CHECK 7개다.
