---
type: Data Model
title: MySQL 데이터 모델
description: iRead MySQL 스키마의 확정 ERD, 실행 기준선과 도메인별 관계를 설명합니다.
tags: [architecture, data-model, mysql, schema, erd]
timestamp: 2026-07-28T00:00:00+09:00
---
# MySQL 데이터 모델

- 상태: accepted
- 최종 검토일: 2026-07-28

## 결정

주 데이터베이스는 [ADR-0006](../decisions/ADR-0006-mysql-primary-database.md)에 따라 MySQL 8.4.x LTS를 사용한다. [ADR-0011](../decisions/ADR-0011-adopt-approved-erd-baseline.md)에 따라 2026-07-28에 확정한 [ERD 이미지](../../contracts/database/erd.png)의 25개 테이블과 관계를 현재 데이터 모델로 채택한다.

ERDCloud가 COMMENT로 표현한 `AUTO_INCREMENT`, `UNIQUE`, `DEFAULT`, `CHECK` 메타데이터는 실행 스키마에서 실제 MySQL 제약조건으로 변환한다. 관계선은 외래 키로 변환하며 외래 키 컬럼에는 `AUTO_INCREMENT`를 적용하지 않는다.

## 기준 원본과 파생 파일

- 실행 기준 원본: `services/backend/src/main/resources/db/migration/V1__baseline_schema.sql`
- 계약 미러: [`contracts/database/schema.sql`](../../contracts/database/schema.sql)
- 확정 설계 이미지: [`contracts/database/erd.png`](../../contracts/database/erd.png)
- 생성 관계도: [`contracts/database/erd.md`](../../contracts/database/erd.md)

DB 적용 전이므로 별도 V2를 만들지 않고 V1을 교체한다. `schema.sql`은 V1과 바이트 단위로 동일하게 유지하고 `erd.md`는 `python tools/generate_erd.py`로 생성한다.

## 교사·학생·인증

- `teachers.email`을 유일한 교사 로그인 식별자로 사용한다.
- `teachers`와 `students`는 1:N 관계다.
- `auth_refresh_sessions`는 교사에 필수로 연결하고 학습자에는 선택적으로 연결한다.
- `audience = ADMIN`이면 `student_id`는 NULL이고 `audience = LEARNING`이면 학습자에 연결한다.
- refresh token 원문은 저장하지 않고 SHA-256 해시를 `token_hash`에 저장한다.

## 훈련과 검사

- `curriculum_units`는 여러 `training_templates`를 가진다.
- 학생은 `daily_curriculums`와 `test_curriculums`를 각각 가질 수 있다.
- `daily_curriculums`는 순서가 있는 `trainings`를 가진다.
- `test_curriculums`는 순서가 있는 `tests`를 가진다.
- `trainings`와 `tests`는 모두 `training_templates`를 참조한다.
- `training_templates.prompt` text에는 타입별 AI 생성 프롬프트와 출력 계약 JSON 문자열을 저장한다.
- AI 생성 데이터는 기존 물리 명칭인 `training_datas`, `test_datas`에 저장한다.
- 훈련 생성 데이터 FK는 기존 물리 명칭인 `train_id`를 유지한다.
- 훈련 정확도와 단어 시도 점수는 `0~1000` 범위로 관리한다.
- `word_attempt_logs.pronunciation_accuracy_score`는 Azure 단어별 `AccuracyScore × 10`, `total_score`는 발음·시선·읽기 수행을 결합한 종합 점수다.
- 성장 정보는 `daily_curriculums`와 `trainings`를 조인해 학생·훈련 템플릿별 `COMPLETED` 행을 실시간 집계한다.
- 완료된 훈련 한 건을 1회로 계산하며 동일 템플릿을 다시 완료하면 새로운 완료 건으로 포함한다.
- 성장 횟수 컬럼과 집계 테이블은 추가하지 않는다. API는 완료 횟수만 반환한다.
- 꽃은 훈련 템플릿별 완료 `0~5`회를 성장 `0~5`단계로 사용한다. 1회 완료할 때마다 한 단계 성장하고 5회에 만개하며, 5회 이후에는 만개 상태를 유지한다.
- 클라이언트는 `min(completedCount, 5)`로 꽃 성장 단계를 계산한다.

## 읽기 특징과 학생 프로필

- `reading_features`는 자모·음절·음운·형태·단어·문장 특징을 코드로 관리하며 `parent_feature_id`로 상하위 특징을 연결한다.
- `student_feature_profiles`는 학생과 읽기 특징별 정확도, 발음, 시선, 읽기 시간, 취약도와 신뢰도를 저장한다.
- 두 테이블의 PK는 확정 ERD에 자동 증가 표시가 없으므로 애플리케이션이 값을 부여한다.
- 확정 ERD의 물리 컬럼명 `reading_features_id`, `avg_pronunciation_scor`를 그대로 사용한다.

## 이야기

이야기 관계는 다음 계층을 사용한다.

```text
story_templates
  └─ stories
      └─ story_scenes
          └─ story_lines
              └─ story_choices
```

- `stories.progress`는 이야기 진행률 `0~100`을 저장한다.
- `story_scenes`는 이야기별 장면 이미지와 순서를 저장한다.
- `story_lines.has_choices`는 해당 대사에 분기 선택이 있는지 나타낸다.
- `story_choices`는 분기 대사에서 음성 입력을 STT로 복원한 최종 선택 텍스트를 저장한다.
- `story_choices.story_line_id`는 UNIQUE이며 한 분기 대사에는 최종 선택 한 건만 저장한다.
- STT 중간 실패와 재시도는 저장하지 않고, AI 생성 성공 후 선택 텍스트·다음 장면·대사·진행률을 하나의 DB 트랜잭션으로 저장한다.
- 같은 `story_line_id`의 네트워크 재시도는 AI를 다시 호출하거나 결과를 덮어쓰지 않고 최초 저장 결과를 반환한다.
- 동시 요청이 UNIQUE 제약에서 경합하면 저장에 성공한 최초 결과를 다시 조회해 반환한다.
- 생성된 장면·대사·선택지 저장과 `stories.progress` 갱신은 하나의 트랜잭션으로 처리한다.
- `characters`는 학생과 이야기에 연결하며 캐릭터 이름과 이미지 URL을 `text`로 저장한다.
- 확정 ERD에는 대표 캐릭터 상태가 없으므로 대표 캐릭터 서버 API를 사용하지 않는다.

## 시선·단어 시도·보고서

- `gaze_sessions`는 검사·훈련·이야기 중 `content_type`에 해당하는 식별자 하나만 가진다.
- 세션에서 초당 5~10프레임으로 수집한 시선 데이터는 파일로 저장하고 `gaze_sessions.data_url`에 파일 URL을 기록한다.
- `gaze_analysis_results`는 시선 세션당 하나의 분석 결과를 가진다.
- `word_attempt_logs`는 `use_location`에 해당하는 검사·훈련·이야기 대사 식별자 하나만 가진다.
- `word_attempt_logs`는 문항 번호와 분석 대상·토큰 위치를 저장하며 같은 위치의 마지막 성공 시도만 `is_final=true`다.
- `word_attempt_logs.has_gaze_data`는 해당 시도에 시선 데이터가 있었는지 명시하고 fixation·gaze offset·skip·regression 필드에는 상세 지표를 저장한다.
- 음성 분석 결과는 인식 문자열을 저장하지 않고 `pronunciation_accuracy_score`, 음성 offset과 정오 여부로 저장한다.
- 보고서 기간은 `start_date <= end_date`를 만족해야 한다.
- 보고서 기간은 확정 ERD에 따라 `timestamp`로 저장하고 `snapshot_data`는 NULL을 허용한다.

## 정합성 제약

- 모든 명시적 연관관계는 외래 키로 보호한다.
- 교사 이메일, refresh token 해시, 단어 원형과 도메인별 순번은 `UNIQUE`로 보호한다.
- 이야기 진행률은 `0~100`, 훈련 정확도·단어 발음 정확도·단어 종합 점수는 `0~1000` 범위를 검사한다.
- `question_no`는 1 이상, `target_index`와 `token_index`는 0 이상이어야 한다.
- 조건부 관계인 인증 audience, 시선 content type과 단어 사용 위치는 `CHECK`로 보호한다.

## 구현 정합화

확정 ERD는 기존 Backend 엔티티보다 우선한다. `story_scenes`, `story_choices`, `test_curriculums`와 변경된 검사·캐릭터·보고서 매핑은 [Backend 정합화 문서](../../contracts/database/backend-alignment.md)에 따라 후속 구현한다.

## 음성 데이터

검사·훈련 발음 평가용 음성은 요청 처리 중에만 보유하고 분석 성공·실패 후 저장하지 않는다. App은 Backend에만 음성을 전송하고 AI server가 Azure Speech를 호출하며 자격증명은 [ADR-0013](../decisions/ADR-0013-azure-speech-pronunciation-assessment.md)에 따라 AI server에 한정한다.

이야기 분기처럼 제품 기능상 재사용이 필요한 음성의 별도 보관 정책은 `audio/{studentId}/{dataType}/` 구조를 사용하되 발음 평가 음성과 혼합하지 않는다. MySQL에는 내부 파일 경로를 API로 노출하지 않으며 필요한 분석 결과와 메타데이터만 저장한다.

[ADR-0008](../decisions/ADR-0008-demo-data-and-runtime-policy.md)에 따라 음성 원본과 보고서의 장기 보관은 연구·분석 목적, 보관 기간, 접근 주체와 삭제 방법을 명시한 별도 동의를 받은 데이터에만 허용한다. 동의 철회 또는 명시한 기간 종료 시 원본과 연결 가능한 파생 데이터를 삭제한다.
