---
type: Feature Specification
title: 교수자 학습 기록 조회
description: 훈련·검사·학습 현황·이야기 기록을 실제 원본 식별자와 동일한 계산 계약으로 조회하는 기능입니다.
tags: [feature, teacher, history, analytics, gaze]
timestamp: 2026-08-04T00:00:00+09:00
---
# 기능 명세: 교수자 학습 기록 조회

- 상태: accepted

## 기대 결과

교수자는 연결된 아동의 훈련·검사·정확도·읽기 속도·이야기 기록을 원본 실행과 문항 식별자별로 확인하고, 화면에 표시된 수치와 판정의 원본·단위·계산 버전을 구분할 수 있다.

## 공통 원칙

- Admin 요청의 학생은 access token의 교수자에게 연결된 학생이어야 한다.
- 식별자는 App 제출부터 Backend 저장, Admin 응답과 Frontend 선택까지 유지한다.
- 실제 `0`, 미측정 `null`, 빈 결과 `[]`, 원본 없음과 조회 실패를 구분한다.
- 구조화 답안은 `responseType`에 맞는 scalar, array 또는 object 형태를 보존한다.
- 정확도와 읽기 속도는 source record, trend와 보고서가 같은 `calculationVersion`을 사용한다.
- Frontend는 Backend가 반환한 판정과 지표를 표시하며 원시 replay로 운영 판정을 다시 계산하지 않는다.

## 훈련 이력

- `GET /api/admin/training/{studentId}/{curriculumId}/training-log`는 정답·오답 여부와 관계없이 완료 훈련의 모든 문항을 반환한다.
- 각 문항은 `questionNo`, `questionType`, `question`, `responseType`, `selectedAnswer`, `correctAnswer`, `correct`, `score`를 포함한다.
- 원본에 값이 존재하는데 오답이 아니라는 이유로 문항·답안을 `null`로 만들지 않는다.

## 검사 이력

- 검사 문항의 안정적인 복합 식별자는 `testId + questionNo`다.
- `sequenceNo`는 검사 커리큘럼 안의 표시 순서이며 영속 문항 식별자로 사용하지 않는다.
- 같은 `testId`에 3문항이 있으면 각 문항은 서로 다른 `questionNo`를 가진다.
- 문항별 시선 분석은 `GET /api/admin/test/{studentId}/{testId}/questions/{questionNo}/gaze-analysis`로 조회한다.
- 검사 이력은 검사 결과를 표시하며 추천 커리큘럼 생성·검수 상태는 커리큘럼 관리 화면에서 처리한다.

## 학습 현황

- 정확도 탭은 `GET /api/admin/student/{studentId}/accuracy-records`의 기록만 표시한다.
- 읽기 속도 탭은 `GET /api/admin/student/{studentId}/reading-speed-records`의 음성 기록만 표시한다.
- source record는 `sourceType`, `sourceId`, `measuredAt`, 원본 분자·분모, 값, 단위와 `calculationVersion`을 포함한다.
- 정확도 일별 값은 `correctAttemptCount` 합계 / `attemptCount` 합계 × 100으로 계산한다.
- 음성 읽기 속도는 `correctWordCount` 합계 × 60,000 / `measuredDurationMs` 합계로 계산하고 gaze 속도와 혼합하지 않는다.
- 선택 기록 상세는 데스크톱에서 핵심 필드를 한 행으로 표시하고 좁은 화면에서만 줄바꿈한다.

## 이야기 이력

- Backend가 `wordMetrics`와 `analysisMeta`를 계산해 권위 있는 판정 결과로 반환한다.
- `analysisMeta.calculationVersion`의 최초 값은 `story-gaze-word-v1`이다.
- 체류는 페이지 글자당 기대 시간보다 긴 연속 방문이며 각 방문 끝에 80ms sample tail을 적용한다.
- 건너뜀과 되돌아보기는 체류 판정을 통과한 이동에만 적용한다.
- 히트맵은 페이지 안에서 최대 단어 체류 시간을 1로 둔 상대 강도다.
- raw replay는 재생에만 사용하고 Frontend는 체류·건너뜀·되돌아보기를 다시 계산하지 않는다.
- 원시 좌표는 Admin 응답에 포함하지 않는다.

## 수용 기준

- 훈련 정답·오답 문항 모두에서 문항·학습자 답·정답을 확인한다.
- 같은 `testId`의 3문항을 `questionNo`로 개별 선택하고 각 문항의 gaze를 조회한다.
- 정확도·속도 탭에는 선택 지표의 source record만 표시한다.
- source record, trend와 보고서의 값·단위·계산 버전이 일치한다.
- 이야기 도움말이 응답의 `calculationVersion`과 판정 metadata를 그대로 설명한다.
- 다른 교수자의 학생 또는 다른 학생의 실행 ID로 조회하면 접근을 거부한다.

## API 관계

- `get_admin_training_by_studentId_by_curriculumId_training_log`
- `get_admin_test_by_studentId_curriculums`
- `get_admin_test_by_studentId_curriculums_by_testCurriculumId`
- `get_admin_test_by_studentId_by_testId_questions_by_questionNo_gaze_analysis`
- `get_admin_student_by_studentId_accuracy_records`
- `get_admin_student_by_studentId_reading_speed_records`
- `get_admin_student_by_studentId_accuracy_trend`
- `get_admin_student_by_studentId_reading_speed_trend`
- `get_admin_story_by_studentId_by_storyId_gaze_analysis`
