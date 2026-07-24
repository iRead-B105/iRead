CREATE TABLE `training_templates` (
	`id`	long	NOT NULL,
	`curriculum_unit_id`	long	NOT NULL,
	`name`	varchar(100)	NOT NULL,
	`form`	json	NOT NULL,
	`sequence_no`	int	NOT NULL
);

CREATE TABLE `students` (
	`id`	long	NOT NULL,
	`teacher_id`	long	NOT NULL	COMMENT 'foreign key',
	`name`	varchar(10)	NOT NULL	COMMENT '실명',
	`birthday`	date	NULL,
	`gender`	varchar(10)	NULL	COMMENT 'Enum: boy, girl',
	`school`	varchar(20)	NULL,
	`guardian`	varchar(10)	NULL,
	`guardian_contact`	varchar(20)	NULL,
	`guardian_email`	varchar(50)	NULL,
	`address`	varchar(100)	NULL,
	`created_at`	timestamp	NOT NULL	COMMENT '생성일',
	`image_url`	varchar(255)	NULL,
	`teacher_memo`	text	NULL
);

CREATE TABLE `curriculum_units` (
	`id`	long	NOT NULL,
	`unit_name`	varchar(50)	NOT NULL	COMMENT '파닉스, 단어 etc',
	`sequence_no`	int	NULL
);

CREATE TABLE `sounds` (
	`id`	long	NOT NULL,
	`question_number`	int	NOT NULL,
	`original_file_name`	varchar(255)	NOT NULL,
	`file_size`	long	NOT NULL,
	`created_at`	timestamp	NOT NULL,
	`store_file_name`	varchar(255)	NOT NULL,
	`url`	varchar(255)	NOT NULL
);

CREATE TABLE `story_templates` (
	`id`	long	NOT NULL,
	`title`	varchar(50)	NOT NULL,
	`content`	text	NOT NULL	COMMENT 'ai에게 컨텍스트주는용도(ex: 백설공주의 줄거리)'
);

CREATE TABLE `images` (
	`id`	long	NOT NULL,
	`original_file_name`	varchar(255)	NOT NULL,
	`store_file_name`	varchar(255)	NOT NULL,
	`file_size`	long	NOT NULL,
	`url`	varchar(255)	NOT NULL,
	`created_at`	timestmap	NOT NULL
);

CREATE TABLE `word_categories` (
	`id`	long	NOT NULL,
	`word_id`	int	NOT NULL,
	`category_name`	int	NOT NULL	COMMENT 'Enum: 받침없는단어, ㅆ받침단어 etc // index'
);

CREATE TABLE `training_datas` (
	`id`	long	NOT NULL,
	`train_id`	long	NOT NULL,
	`generated_data`	json	NULL	COMMENT '훈련에서 쓰일 단어/문장(ai생성)',
	`created_at`	timestmap	NULL
);

CREATE TABLE `stories` (
	`id`	long	NOT NULL,
	`student_id`	long	NOT NULL,
	`story_templates_id`	long	NOT NULL,
	`created_at`	timestmap	NOT NULL,
	`status`	varchar(30)	NOT NULL	COMMENT 'Enum: IN_PROGRESS/COMPLETED/DELETED'
);

CREATE TABLE `test_datas` (
	`id`	VARCHAR(255)	NOT NULL,
	`test_id`	long	NOT NULL,
	`question`	json	NULL	COMMENT '문항문제'
);

CREATE TABLE `gaze_analysis_results` (
	`id`	long	NOT NULL,
	`gaze_session_id`	long	NOT NULL,
	`total_visited_duration`	int	NOT NULL,
	`total_visited_count`	int	NOT NULL,
	`reverse_read_count`	int	NOT NULL,
	`avg_visited_duration`	int	NULL,
	`created_at`	timestamp	NOT NULL
);

CREATE TABLE `gaze_sessions` (
	`id`	long	NOT NULL,
	`student_id`	long	NOT NULL,
	`test_id`	long	NULL,
	`training_id`	long	NULL,
	`story_id`	long	NULL,
	`content_type`	varchar(20)	NOT NULL	COMMENT 'TEST, TRAINING, STORY',
	`started_at`	timestamp	NOT NULL,
	`ended_at`	timestamp	NULL,
	`status`	varchar(20)	NOT NULL	COMMENT 'READY, RUNNING, COMPLETED, FAILED',
	`calibration_status`	varchar(20)	NOT NULL	COMMENT 'NOT_STARTED, SUCCESS, FAILED, SKIPPED',
	`created_at`	timestamp	NOT NULL
);

CREATE TABLE `student_study_progresses` (
	`id`	long	NOT NULL,
	`student_id`	long	NOT NULL,
	`training_template_id`	long	NOT NULL,
	`achivement`	int	NULL
);

CREATE TABLE `student_word_stats` (
	`id`	long	NOT NULL	COMMENT '훈련+테스트+스토리 통계테이블',
	`word_score`	decimal	NULL	COMMENT '0.0~100.0',
	`attempt_count`	int	NULL,
	`updated_at`	timestamp	NULL,
	`Field`	VARCHAR(255)	NULL,
	`Field2`	VARCHAR(255)	NULL
);

CREATE TABLE `words` (
	`id`	long	NOT NULL	COMMENT '단어는 기본형태',
	`content`	varchar(50)	NOT NULL	COMMENT 'UNIQUE',
	`length`	int	NOT NULL
);

CREATE TABLE `reports` (
	`id`	long	NOT NULL,
	`student_id`	long	NOT NULL,
	`start_date`	timestamp	NOT NULL	COMMENT '기간시작일~기간종료일 에 대한 리포트',
	`end_date`	timestmap	NOT NULL,
	`snapshot_data`	json	NULL,
	`teacher_memo`	text	NULL,
	`created_at`	timestamp	NOT NULL	COMMENT '생성일'
);

CREATE TABLE `videos` (
	`id`	long	NOT NULL,
	`question_number`	int	NOT NULL,
	`original_file_name`	varchar(255)	NOT NULL,
	`file_size`	long	NOT NULL,
	`created_at`	timestamp	NOT NULL,
	`store_file_name`	varchar(255)	NOT NULL,
	`url`	varchar(255)	NOT NULL
);

CREATE TABLE `teachers` (
	`id`	long	NOT NULL,
	`email`	varchar(50)	NOT NULL	COMMENT 'unique',
	`password`	varchar(100)	NOT NULL,
	`name`	varchar(10)	NULL	COMMENT '실명',
	`organization`	varchar(100)	NULL,
	`created_at`	timestamp	NOT NULL	COMMENT '생성일',
	`gender`	varchar(10)	NULL	COMMENT 'Enum',
	`image_url`	varchar(255)	NULL
);

CREATE TABLE `story_lines` (
	`id`	long	NOT NULL,
	`story_id`	long	NOT NULL,
	`image_url`	varchar(255)	NULL,
	`has_choices`	boolean	NOT NULL,
	`content`	text	NOT NULL,
	`sequence_no`	int	NOT NULL,
	`created_at`	timestamp	NOT NULL,
	`read_at`	timestmap	NULL
);

CREATE TABLE `word_attempt_logs` (
	`id`	long	NOT NULL,
	`student_id`	long	NOT NULL,
	`word_id`	long	NOT NULL	COMMENT '단어는 기본형태',
	`surface_text`	varchar(50)	NULL	COMMENT '단어의 문장내에서의 형태(ex: 먹었다)',
	`has_gaze_data`	boolean	NOT NULL,
	`has_audio_data`	boolean	NOT NULL,
	`fixation_duration_ms`	int	NULL,
	`fixation_count`	int	NULL,
	`gaze_start_offset_ms`	int	NULL,
	`gaze_end_offset_ms`	int	NULL,
	`is_skipped`	boolean	NULL,
	`regression_count`	int	NULL,
	`recognized_text`	varchar(255)	NULL	COMMENT 'stt가 인식한 결과',
	`speech_start_offset_ms`	int	NULL,
	`speech_end_offset_ms`	int	NULL,
	`is_correct`	boolean	NULL,
	`created__at`	timestamp	NULL
);

CREATE TABLE `character` (
	`id`	long	NOT NULL,
	`student_id`	long	NOT NULL,
	`image_url`	varchar(255)	NULL,
	`created_at`	timestamp	NOT NULL
);

CREATE TABLE `story_choices` (
	`id`	long	NOT NULL,
	`story_lines_id`	long	NOT NULL,
	`content`	text	NOT NULL,
	`created_at`	timestamp	NOT NULL
);

CREATE TABLE `trainings` (
	`id`	long	NOT NULL,
	`training_template_id`	long	NOT NULL,
	`daily_curriculum_id`	long	NOT NULL,
	`sequence_no`	int	NOT NULL	COMMENT '커리큘럼내에서의 순서, (id, 훈련순서) uniuque',
	`created_at`	timestamp	NOT NULL,
	`started_at`	timestmap	NULL,
	`finished_at`	timestmap	NULL,
	`status`	varchar(20)	NOT NULL	COMMENT 'Enum:    NOT_READY,  NOT_STARTED,  IN_PROGRESS,  COMPLETED',
	`result`	json	NULL	COMMENT '문항별 정답유무/틀린부분',
	`accuracy`	int	NULL	COMMENT '정답률'
);

CREATE TABLE `daily_curriculums` (
	`id`	long	NOT NULL,
	`student_id`	long	NOT NULL,
	`status`	varchar(20)	NOT NULL	COMMENT 'Enum:  NOT_STARTED,  IN_PROGRESS,  COMPLETED',
	`created_at`	timestmap	NOT NULL,
	`completed_at`	timestamp	NULL
);

CREATE TABLE `test` (
	`id`	long	NOT NULL,
	`student_id`	long	NOT NULL,
	`created_at`	timestamp	NOT NULL,
	`status`	varchar(20)	NULL	COMMENT 'Enum:    NOT_READY,  NOT_STARTED,  IN_PROGRESS,  COMPLETED',
	`result`	json	NULL	COMMENT '문항별 정답유무/틀린부분',
	`accuracy`	decimal	NULL	COMMENT '정답률'
);

ALTER TABLE `training_templates` ADD CONSTRAINT `PK_TRAINING_TEMPLATES` PRIMARY KEY (
	`id`
);

ALTER TABLE `students` ADD CONSTRAINT `PK_STUDENTS` PRIMARY KEY (
	`id`
);

ALTER TABLE `curriculum_units` ADD CONSTRAINT `PK_CURRICULUM_UNITS` PRIMARY KEY (
	`id`
);

ALTER TABLE `sounds` ADD CONSTRAINT `PK_SOUNDS` PRIMARY KEY (
	`id`
);

ALTER TABLE `story_templates` ADD CONSTRAINT `PK_STORY_TEMPLATES` PRIMARY KEY (
	`id`
);

ALTER TABLE `images` ADD CONSTRAINT `PK_IMAGES` PRIMARY KEY (
	`id`
);

ALTER TABLE `word_categories` ADD CONSTRAINT `PK_WORD_CATEGORIES` PRIMARY KEY (
	`id`
);

ALTER TABLE `training_datas` ADD CONSTRAINT `PK_TRAINING_DATAS` PRIMARY KEY (
	`id`
);

ALTER TABLE `stories` ADD CONSTRAINT `PK_STORIES` PRIMARY KEY (
	`id`
);

ALTER TABLE `test_datas` ADD CONSTRAINT `PK_TEST_DATAS` PRIMARY KEY (
	`id`
);

ALTER TABLE `gaze_analysis_results` ADD CONSTRAINT `PK_GAZE_ANALYSIS_RESULTS` PRIMARY KEY (
	`id`
);

ALTER TABLE `gaze_sessions` ADD CONSTRAINT `PK_GAZE_SESSIONS` PRIMARY KEY (
	`id`
);

ALTER TABLE `student_study_progresses` ADD CONSTRAINT `PK_STUDENT_STUDY_PROGRESSES` PRIMARY KEY (
	`id`
);

ALTER TABLE `student_word_stats` ADD CONSTRAINT `PK_STUDENT_WORD_STATS` PRIMARY KEY (
	`id`
);

ALTER TABLE `words` ADD CONSTRAINT `PK_WORDS` PRIMARY KEY (
	`id`
);

ALTER TABLE `reports` ADD CONSTRAINT `PK_REPORTS` PRIMARY KEY (
	`id`
);

ALTER TABLE `videos` ADD CONSTRAINT `PK_VIDEOS` PRIMARY KEY (
	`id`
);

ALTER TABLE `teachers` ADD CONSTRAINT `PK_TEACHERS` PRIMARY KEY (
	`id`
);

ALTER TABLE `story_lines` ADD CONSTRAINT `PK_STORY_LINES` PRIMARY KEY (
	`id`
);

ALTER TABLE `word_attempt_logs` ADD CONSTRAINT `PK_WORD_ATTEMPT_LOGS` PRIMARY KEY (
	`id`
);

ALTER TABLE `character` ADD CONSTRAINT `PK_CHARACTER` PRIMARY KEY (
	`id`
);

ALTER TABLE `story_choices` ADD CONSTRAINT `PK_STORY_CHOICES` PRIMARY KEY (
	`id`
);

ALTER TABLE `trainings` ADD CONSTRAINT `PK_TRAININGS` PRIMARY KEY (
	`id`
);

ALTER TABLE `daily_curriculums` ADD CONSTRAINT `PK_DAILY_CURRICULUMS` PRIMARY KEY (
	`id`
);

ALTER TABLE `test` ADD CONSTRAINT `PK_TEST` PRIMARY KEY (
	`id`
);

