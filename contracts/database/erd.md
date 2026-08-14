---
type: Contract Diagram
title: "MySQL ERD"
description: "Flyway와 동일한 MySQL 스키마 계약에서 자동 생성한 엔터티 관계도입니다."
tags: [contracts, database, mysql, erd, generated]
timestamp: 2026-07-25T00:00:00+09:00
---
# MySQL ERD

- 상태: generated
- 기준 원본: [Backend Flyway migrations](../../services/backend/src/main/resources/db/migration/)
- 검토용 미러: [schema.sql](schema.sql)
- 확정 설계 이미지: [erd.png](erd.png)
- 생성 명령: `python tools/generate_erd.py`

이 파일은 `contracts/database/schema.sql`의 테이블과 외래 키에서 자동 생성한다. 직접 수정하지 않고 스키마를 변경한 뒤 생성 명령을 다시 실행한다.

```mermaid
erDiagram
    training_templates {
        BIGINT id PK "required"
        BIGINT curriculum_unit_id FK "required"
        VARCHAR_100 name "required"
        TEXT prompt "required"
        INT sequence_no "required"
    }
    students {
        BIGINT id PK "required"
        BIGINT teacher_id FK "required"
        VARCHAR_10 name "required"
        DATE birthday "nullable"
        VARCHAR_10 gender "nullable"
        VARCHAR_20 school "nullable"
        VARCHAR_10 guardian "nullable"
        VARCHAR_20 guardian_contact "nullable"
        VARCHAR_50 guardian_email "nullable"
        VARCHAR_100 address "nullable"
        TIMESTAMP created_at "required"
        VARCHAR_255 image_url "nullable"
        TEXT teacher_memo "nullable"
    }
    reading_features {
        BIGINT id PK "required"
        BIGINT parent_feature_id FK "nullable"
        VARCHAR_150 feature_code "required"
        VARCHAR_150 feature_name "required"
        VARCHAR_30 category "required"
        VARCHAR_30 scope "required"
        TIMESTAMP created_at "nullable"
    }
    student_feature_profiles {
        BIGINT id PK "required"
        BIGINT student_id FK "required"
        BIGINT reading_features_id FK "required"
        DECIMAL_5_4 accuracy_rate "nullable"
        INT avg_pronunciation_scor "nullable"
        DECIMAL_8_2 pronunciation_error_rate "nullable"
        INT avg_fixation_duration_ms "nullable"
        DECIMAL_8_2 avg_fixation_count "nullable"
        DECIMAL_8_2 avg_regression_count "nullable"
        DECIMAL_5_2 skip_rate "nullable"
        INT avg_reading_time_ms "nullable"
        INT weakness_score "nullable"
        DECIMAL_5_4 confidence "required"
        INT evidence_count "nullable"
        TIMESTAMP last_evidence_at "nullable"
        TIMESTAMP analyzed_at "nullable"
    }
    auth_refresh_sessions {
        BIGINT id PK "required"
        BIGINT teacher_id FK "required"
        BIGINT student_id FK "nullable"
        VARCHAR_30 audience "required"
        CHAR_64 token_hash "required"
        TIMESTAMP expires_at "required"
        TIMESTAMP revoked_at "nullable"
        TIMESTAMP created_at "required"
    }
    password_reset_tokens {
        BIGINT id PK "required"
        BIGINT teacher_id FK "required"
        CHAR_64 token_hash "required"
        TIMESTAMP expires_at "required"
        TIMESTAMP used_at "nullable"
        TIMESTAMP created_at "required"
    }
    curriculum_units {
        BIGINT id PK "required"
        VARCHAR_50 unit_name "required"
        INT sequence_no "nullable"
    }
    story_templates {
        BIGINT id PK "required"
        VARCHAR_50 title "required"
        TEXT content "required"
        VARCHAR_255 image_url "nullable"
    }
    story_scenes {
        BIGINT scene_id PK "required"
        BIGINT story_id FK "required"
        VARCHAR_255 image_url "nullable"
        INT sequence_no "required"
        TIMESTAMP created_at "required"
    }
    word_categories {
        BIGINT id PK "required"
        BIGINT word_id FK "required"
        VARCHAR_50 category_name "required"
    }
    training_datas {
        BIGINT id PK "required"
        BIGINT train_id FK "required"
        JSON generated_data "nullable"
        TIMESTAMP created_at "nullable"
    }
    stories {
        BIGINT id PK "required"
        BIGINT student_id FK "required"
        BIGINT story_template_id FK "required"
        TIMESTAMP created_at "required"
        VARCHAR_30 status "required"
        TINYINT_UNSIGNED progress "required"
    }
    gaze_analysis_results {
        BIGINT id PK "required"
        BIGINT gaze_session_id FK "required"
        INT total_visited_duration "required"
        INT total_visited_count "required"
        INT reverse_read_count "required"
        INT avg_visited_duration "nullable"
        JSON sentence_metrics "nullable"
        JSON regressions "nullable"
        JSON analysis_meta "nullable"
        TIMESTAMP created_at "required"
    }
    gaze_sessions {
        BIGINT id PK "required"
        BIGINT student_id FK "required"
        BIGINT test_id FK "nullable"
        BIGINT training_id FK "nullable"
        BIGINT story_id FK "nullable"
        VARCHAR_20 content_type "required"
        TIMESTAMP started_at "required"
        TIMESTAMP ended_at "nullable"
        VARCHAR_255 data_url "nullable"
        VARCHAR_20 status "required"
        VARCHAR_20 calibration_status "required"
        TIMESTAMP created_at "required"
    }
    words {
        BIGINT id PK "required"
        VARCHAR_50 content "required"
        INT length "required"
    }
    reports {
        BIGINT id PK "required"
        BIGINT student_id FK "required"
        TIMESTAMP start_date "required"
        TIMESTAMP end_date "required"
        JSON snapshot_data "nullable"
        TEXT teacher_memo "nullable"
        TIMESTAMP created_at "required"
    }
    teachers {
        BIGINT id PK "required"
        VARCHAR_50 email "required"
        VARCHAR_100 password "required"
        VARCHAR_10 name "required"
        VARCHAR_100 organization "nullable"
        TIMESTAMP created_at "required"
        VARCHAR_10 gender "nullable"
        VARCHAR_255 image_url "nullable"
    }
    story_lines {
        BIGINT id PK "required"
        BIGINT scene_id FK "required"
        BOOLEAN has_choices "required"
        JSON content "required"
        JSON branch_prompt "nullable"
        INT sequence_no "required"
        TIMESTAMP created_at "required"
        TIMESTAMP read_at "nullable"
    }
    word_attempt_logs {
        BIGINT id PK "required"
        BIGINT student_id FK "required"
        BIGINT word_id FK "required"
        BIGINT story_line_id FK "nullable"
        BIGINT training_id FK "nullable"
        BIGINT test_id FK "nullable"
        VARCHAR_10 use_location "required"
        VARCHAR_50 surface_text "nullable"
        BOOLEAN has_gaze_data "required"
        BOOLEAN has_audio_data "required"
        INT fixation_duration_ms "nullable"
        INT fixation_count "nullable"
        INT gaze_start_offset_ms "nullable"
        INT gaze_end_offset_ms "nullable"
        BOOLEAN is_skipped "nullable"
        INT regression_count "nullable"
        INT pronunciation_accuracy_score "nullable"
        INT speech_start_offset_ms "nullable"
        INT speech_end_offset_ms "nullable"
        BOOLEAN is_correct "nullable"
        TIMESTAMP created_at "nullable"
        INT total_score "nullable"
        INT question_no "nullable"
        INT target_index "nullable"
        INT token_index "nullable"
        BOOLEAN is_final "required"
    }
    characters {
        BIGINT id PK "required"
        BIGINT student_id FK "required"
        BIGINT story_id FK "required"
        TEXT image_url "nullable"
        TIMESTAMP created_at "required"
        VARCHAR_50 name "nullable"
    }
    story_choices {
        BIGINT id PK "required"
        BIGINT story_line_id FK "required"
        TEXT content "required"
        TIMESTAMP created_at "required"
    }
    trainings {
        BIGINT id PK "required"
        BIGINT training_template_id FK "required"
        BIGINT daily_curriculum_id FK "required"
        INT sequence_no "required"
        TIMESTAMP created_at "required"
        TIMESTAMP started_at "nullable"
        TIMESTAMP finished_at "nullable"
        VARCHAR_20 status "required"
        JSON result "nullable"
        INT accuracy "nullable"
    }
    daily_curriculums {
        BIGINT id PK "required"
        BIGINT student_id FK "required"
        VARCHAR_20 status "required"
        TIMESTAMP created_at "required"
        TIMESTAMP completed_at "nullable"
    }
    tests {
        BIGINT id PK "required"
        BIGINT test_curriculum_id FK "required"
        BIGINT training_template_id FK "required"
        VARCHAR_20 status "nullable"
        JSON result "nullable"
        DECIMAL accuracy "nullable"
        TIMESTAMP created_at "required"
        TIMESTAMP started_at "nullable"
        TIMESTAMP finished_at "nullable"
        INT sequence_no "required"
    }
    test_curriculums {
        BIGINT id PK "required"
        BIGINT student_id FK "required"
        VARCHAR_20 status "required"
        TIMESTAMP created_at "nullable"
        TIMESTAMP completed_at "nullable"
    }
    test_datas {
        BIGINT id PK "required"
        BIGINT test_id FK "required"
        JSON generated_data "nullable"
        TIMESTAMP created_at "nullable"
    }
    teachers ||--o{ students : "teacher_id"
    reading_features o|--o{ reading_features : "parent_feature_id"
    students ||--o{ student_feature_profiles : "student_id"
    reading_features ||--o{ student_feature_profiles : "reading_features_id"
    teachers ||--o{ auth_refresh_sessions : "teacher_id"
    students o|--o{ auth_refresh_sessions : "student_id"
    teachers ||--o{ password_reset_tokens : "teacher_id"
    curriculum_units ||--o{ training_templates : "curriculum_unit_id"
    stories ||--o{ story_scenes : "story_id"
    words ||--o{ word_categories : "word_id"
    trainings ||--o{ training_datas : "train_id"
    students ||--o{ stories : "student_id"
    story_templates ||--o{ stories : "story_template_id"
    gaze_sessions ||--o{ gaze_analysis_results : "gaze_session_id"
    students ||--o{ gaze_sessions : "student_id"
    tests o|--o{ gaze_sessions : "test_id"
    trainings o|--o{ gaze_sessions : "training_id"
    stories o|--o{ gaze_sessions : "story_id"
    students ||--o{ reports : "student_id"
    story_scenes ||--o{ story_lines : "scene_id"
    students ||--o{ word_attempt_logs : "student_id"
    words ||--o{ word_attempt_logs : "word_id"
    story_lines o|--o{ word_attempt_logs : "story_line_id"
    trainings o|--o{ word_attempt_logs : "training_id"
    tests o|--o{ word_attempt_logs : "test_id"
    students ||--o{ characters : "student_id"
    stories ||--o{ characters : "story_id"
    story_lines ||--o{ story_choices : "story_line_id"
    training_templates ||--o{ trainings : "training_template_id"
    daily_curriculums ||--o{ trainings : "daily_curriculum_id"
    students ||--o{ daily_curriculums : "student_id"
    test_curriculums ||--o{ tests : "test_curriculum_id"
    training_templates ||--o{ tests : "training_template_id"
    students ||--o{ test_curriculums : "student_id"
    tests ||--o{ test_datas : "test_id"
```
