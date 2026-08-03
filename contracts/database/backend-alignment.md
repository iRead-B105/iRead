---
type: Contract Alignment
title: "Backend 엔티티와 MySQL 계약 정합화"
description: "확정 ERD와 Backend 엔티티의 차이, Flyway 적용 경계와 후속 정합화 범위를 정리합니다."
tags: [contracts, backend, mysql, migration, alignment, erd]
timestamp: 2026-07-27T00:00:00+09:00
---
# Backend 엔티티와 MySQL 계약 정합화

- 상태: active
- 비교 기준: 2026-07-28 확정 ERD, `contracts/database/schema.sql`, 현재 Backend 작업 트리
- 최종 검토일: 2026-07-31

## 결론

사용자가 확정한 ERD를 현재 MySQL 계약으로 채택했다. 최종 스키마는 Flyway `V1__baseline_schema.sql`에 통합하고 `contracts/database/schema.sql`과 바이트 단위로 동일하게 유지한다.

Backend 엔티티를 현재 계약에 맞춰 정합화했다. 전체 데모 데이터는 `V2__demo_seed.sql`에 통합하며 다음 변경 migration은 V3부터 순서대로 추가한다.

## 확정된 물리 명칭

- `training_datas`
- `train_id`
- `test_datas`
- `tests`
- `story_lines.has_choices`
- `story_lines.branch_prompt`
- `teachers.email`
- `auth_refresh_sessions`
- `training_templates.prompt`
- `reading_features`
- `student_feature_profiles.reading_features_id`
- `student_feature_profiles.avg_pronunciation_scor`
- `characters`

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
| 시선 세션 | 조건부 대상 FK와 `data_url` | 원시 시선 JSON은 파일로 저장하고 DB에는 파일 URL과 조건부 관계를 반영 |
| 보고서 | 기간 `timestamp`, nullable `snapshot_data` | `LocalDate` 및 필수 snapshot 매핑 교체 |
| 누적 통계 | 별도 누적 통계 테이블 없음 | `student_word_stats`, `student_study_progresses` 매핑 제거 |
| 훈련 점수 | `accuracy` 0~1000 | 기존 0~100 소수 정밀도 매핑 교체 |
| 훈련 생성 프롬프트 | `training_templates.prompt` text | 기존 `form` JSON 컬럼을 최종 ERD 명칭으로 교체 |
| 읽기 특징 | `reading_features` 자기 참조 계층 | 자모·음절·음운·형태·단어·문장 특징 사전 추가 |
| 학생 특징 프로필 | `student_feature_profiles` | 학생·읽기 특징별 집계 지표와 취약도·신뢰도 저장 |
| 단어 수행 근거 | `word_attempt_logs` | 인식 문자열과 시선 존재 boolean 제거, 발음 정확도·문항 위치·최종 시도 컬럼 추가 |

- 확정 ERD에 대표 캐릭터 상태가 없으므로 대표 캐릭터 변경 API를 제거하고 관련 표시 상태는 클라이언트 책임으로 변경했다.
- `story_choices.content`에는 음성 입력을 STT로 복원한 최종 텍스트 또는 저장된 `branch_prompt`에서 선택한 버튼 문구를 저장한다. `story_line_id`를 UNIQUE로 보호하고 STT 중간 실패는 저장하지 않는다. 같은 분기 대사의 재시도는 최초 저장 결과를 반환한다.
- 성장 정보는 별도 컬럼 없이 완료된 `trainings` 행을 학생·훈련 템플릿별로 실시간 집계한다. 클라이언트는 `min(completedCount, 5)`로 성장 단계를 계산하며 5회에 만개 상태가 된다.

## V1 변환 규칙

- ERDCloud COMMENT의 `AUTO_INCREMENT`, `UNIQUE`, `DEFAULT`, `CHECK`는 실행 DDL의 실제 속성·제약조건으로 변환했다.
- 관계선은 34개 외래 키로 변환했다.
- FK에 복사된 `AUTO_INCREMENT` 메모는 적용하지 않았다.
- `test_curriculums.id`, `test_datas.id`는 확정 ERD에 자동 증가 표시가 없으므로 일반 `bigint` PK로 유지했다.
- `reading_features.id`, `student_feature_profiles.id`도 확정 ERD에 자동 증가 표시가 없으므로 일반 `bigint` PK로 유지했다.
- `gaze_analysis_results.gaze_session_id`는 시선 세션당 분석 결과 하나를 보장하도록 UNIQUE로 보호했다.
- `story_choices.story_line_id`는 분기 대사당 최종 선택 하나를 보장하도록 UNIQUE로 보호했다.
- `word_attempt_logs.pronunciation_accuracy_score`와 `total_score`는 각각 `0~1000` CHECK를 적용한다.
- `word_attempt_logs.question_no`는 1 이상, `target_index`와 `token_index`는 0 이상 CHECK를 적용한다.
- `daily_curriculums`는 생성 컬럼과 UNIQUE 제약으로 학생별 `NOT_STARTED` 최대 1건과 `IN_PROGRESS` 최대 1건을 각각 보장한다.

## 적용 경계

- V1 기준선은 신규·빈 데이터베이스 기준이다.
- 신규·빈 데이터베이스는 V1 하나로 최종 스키마를 구성한다.
- demo 프로필은 V1 적용 뒤 V2 하나로 최종 데모 데이터를 구성한다.
- Backend 엔티티와 저장소 정합화를 완료했으며 Hibernate schema validation이 MySQL 8.4.10에서 통과한다.
- 통합 전 V6·V7·V8 이력을 적용한 개발 DB는 초기화 후 V1→V2로 다시 구성한다. 운영 데이터가 생긴 이후에는 기준선을 다시 쓰지 않고 V3부터 누적 migration을 사용한다.

## 인증 계약

- 교사 로그인 식별자는 `teachers.email` 하나다.
- `auth_refresh_sessions`만 사용하고 access token 폐기 테이블은 사용하지 않는다.
- Admin 세션은 `student_id`가 NULL이고 학습 세션은 학생에 연결한다.
- refresh token 원문은 저장하지 않고 SHA-256 해시만 저장한다.

## 후속 검증

- 기존 스키마나 데이터가 있는 환경에 적용할 때는 별도 baseline과 데이터 변환 migration을 검증한다.
- V1·V2 또는 V3 이후 migration을 변경하면 빈 MySQL에서 전체 Flyway 순서와 demo 프로필을 다시 검증한다.

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
- 당시 갱신 ERD에 따라 `word_attempt_logs.has_gaze_data`, `recognized_text`를 제거했다.
- `pronunciation_accuracy_score`, `question_no`, `target_index`, `token_index`, `is_final`을 추가해 단어 발음 정확도와 최종 시도를 행 자체에서 식별한다.
- 점수·위치 CHECK를 추가했다.

## 2026-07-29 보고서 기간 중복 방지

- `reports(student_id, start_date, end_date)`에 `UQ_REPORTS_STUDENT_PERIOD` UNIQUE 제약을 추가해 동일 아동·동일 기간 보고서가 동시 요청에서도 한 건만 저장되도록 했다.
- 현재 스키마 규모는 애플리케이션 테이블 26개, 외래 키 35개, UNIQUE 15개, CHECK 11개다.

## 2026-07-31 Flyway 기준선과 활성 교육과정 정리

- `character`를 최종 물리 명칭 `characters`로 바꾸고 `image_url`을 `text`로 확장한 결과를 V1에 통합했다. 별도 V4·V5 migration은 제거했다.
- 모든 Flyway 데모 seed를 V2에 통합하고 V3 데모 migration은 제거했다.
- 학생별 `NOT_STARTED` 최대 1건과 `IN_PROGRESS` 최대 1건을 DB UNIQUE 제약으로 보장한다. 두 상태는 학생 한 명에게 각각 한 건씩 동시에 존재할 수 있다.
- 활성 교육과정 조회 우선순위는 `IN_PROGRESS` 다음 `NOT_STARTED`이며, 교수자 편집은 `NOT_STARTED` 교육과정에만 허용한다.
- 학생 행 잠금으로 교육과정 생성과 훈련 시작의 동시 요청을 직렬화해 애플리케이션 검증과 DB 제약이 같은 정책을 보장한다.
- 빈 MySQL에서 V1 단독과 V1+V2 적용, Hibernate 검증, 데모 초기화와 중복 제약 검증을 통과했다.
- 현재 스키마 규모는 애플리케이션 테이블 26개, 외래 키 35개, UNIQUE 15개, CHECK 11개다.
- 최신 Backend의 시선 원본 파일 저장 계약에 맞춰 `gaze_sessions.data` JSON을 `data_url`로 교체하고 `word_attempt_logs.has_gaze_data`를 명시적 저장 값으로 복원했다.
- 읽기 특징 분류는 현재 enum과 일치하도록 `MORPH`를 제외했다.

## 2026-07-31 이야기 대사·분기 선택지 기준선 통합

- `story_lines.content`는 V1부터 `{"text": ..., "analysis": ...}` 구조의 JSON으로 생성한다.
- `story_lines.branch_prompt`도 V1에 포함하며, 분기 대사는 AI가 생성한 서로 다른 선택지 3개를 저장하고 일반 대사는 NULL을 유지한다.
- V2 데모 대사는 최종 JSON 구조와 선택지를 직접 삽입한다.
- 기존 V6·V7·V8 파일은 V1·V2에 흡수했다. 다음 스키마 또는 데이터 변경은 V3부터 추가한다.
- 이미지 생성은 현재 동기 호출이므로 성공한 `image_url`만 트랜잭션에 저장한다. 비동기 작업 큐를 도입하기 전에는 별도 생성 상태 컬럼을 두지 않는다.
