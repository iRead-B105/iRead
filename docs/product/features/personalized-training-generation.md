---
type: Feature Specification
title: "맞춤 훈련 데이터 생성"
description: "학습자의 단어별 수행 근거를 읽기 특징 프로필로 집계하고 다음 커리큘럼의 훈련 데이터를 생성·검증하는 기능 명세입니다."
tags: [feature, training, personalization, reading, backend]
timestamp: 2026-07-28T00:00:00+09:00
---
# 맞춤 훈련 데이터 생성

- 상태: accepted
- 작성일: 2026-07-28
- 관련 실행 계획: [맞춤 훈련 데이터 생성 파이프라인](../../../plans/2026-07-28-personalized-training-generation.md)

## 문제와 기대 결과

기존 훈련의 정답·발음·시선·읽기 시간만으로는 어떤 자모·음절 구조·음운 규칙이 반복해서 읽기 부담을 만드는지 일관되게 추적하기 어렵다. AI가 생성한 문장을 검증 없이 사용하면 목표 특징이 없거나 금지 특징이 섞일 수 있다.

Backend는 마지막 확정 수행 결과를 읽기 특징별로 집계하고, 취약 특징과 호환되는 다음 훈련 목록을 편성한다. AI server의 후보는 형태·자모·G2P·음운 규칙과 타입별 형식을 통과한 경우에만 최종 훈련 데이터로 저장한다.

## 범위

### 포함 범위

- 34개 `trainingType`의 후보 생성과 타입별 출력 검증
- 초성·중성·종성·음절 구조·형태소·단어·문장·주요 음운 규칙 특징
- 학생별 읽기 특징 프로필과 `WEAKNESS_V1` 취약도
- 커리큘럼 전체 완료 직후 다음 훈련 목록 5개 편성
- 생성 전 교수자 편집과 생성 성공 후 잠금
- 매일 03:00 `Asia/Seoul` 기준 문항 생성
- AI 훈련 후보·발음 분석과 시선 분석의 Mock adapter

### 제외 범위

- 실제 LLM·STT·발음 분석 모델 구현
- 음성 파일 영구 저장과 `sounds` 테이블
- 원시 시선 좌표의 Backend 직접 분석
- 운영 다중 인스턴스용 분산 배치 잠금

## 사용자 여정

1. 학습자가 현재 커리큘럼의 훈련 약 5개를 모두 완료한다.
2. Backend가 `training_datas.generated_data`, `trainings.result`, 마지막 확정 `word_attempt_logs`를 결합해 특징별 프로필을 갱신한다.
3. Backend가 직접 보완 3개, 확장 1개, 복습·유창성 1개로 다음 커리큘럼 목록을 편성한다.
4. 교수자는 03:00 데이터 생성 전까지 훈련 유형과 순서를 편집한다.
5. 03:00 배치가 각 훈련에 후보 문항 5개를 요청하고 Backend가 분석·검증한다.
6. 부족한 문항은 통과 문항을 유지한 채 최대 3회 보충 생성한다.
7. 목록의 모든 훈련이 성공하면 `training_datas`를 한 번에 저장하고 편집을 잠근다.
8. 하나라도 실패하면 전체를 저장하거나 잠그지 않고 다음 배치 대상으로 유지한다.

## 요구사항과 수용 기준

- `PTG-001`: Backend는 34개 `trainingType`을 각각 별도 `training_templates` 행으로 관리한다.
- `PTG-002`: `training_templates.prompt` JSON은 `trainingType`, `additionalPrompt`, `outputTemplate`, `supportedFeatureCategories`, `supportedScopes`를 포함한다.
- `PTG-003`: AI 생성 요청은 `requestId`, `schemaVersion`, `trainingType`, `count`, `difficulty`, 목표·제외 특징, 타입별 프롬프트와 출력 템플릿만 포함한다.
- `PTG-004`: AI 생성 요청에는 `studentId`, 이름, 생년월일, 연락처, 원본 음성, 원시 시선 좌표를 포함하지 않는다.
- `PTG-005`: AI 후보는 `{type,data}` 형식이며 `data`에 요청한 `count=5` 항목을 포함한다.
- `PTG-006`: `questionNo`와 `sequenceNo`는 1부터 시작하고 배열 위치를 가리키는 인덱스는 0부터 시작한다.
- `PTG-007`: Backend는 모든 화면 텍스트를 `analysisTargets`로 정규화하고 자모·형태·G2P·음운 규칙 특징을 부착한다.
- `PTG-008`: 정답 근거는 정답 목표와 실제 선택 항목에만, 시선 근거는 실제 응시한 모든 항목에 반영한다.
- `PTG-009`: AI 후보는 목표 특징, 제외 특징, 길이, 형식과 정답 일치를 모두 통과해야 한다.
- `PTG-010`: 최종 `generated_data`는 `schemaVersion`, `generationMetadata`, `profileSnapshot`, `questions`, `validationResult`를 포함한다.
- `PTG-011`: 문항은 공통 `questionNo`, `type`, `content`, `answer`, `analysisTargets`, `targetFeatureCodes`를 포함하고 읽기 문항은 `text`, `expectedPronunciation`, `words`를 추가한다.
- `PTG-012`: 학생용 문항 응답에는 서버 평가용 `answer`, 프로필 스냅샷과 내부 검증 정보를 노출하지 않는다.
- `PTG-013`: 같은 문항·토큰의 여러 시도 중 `trainings.result`에서 `isFinal=true`로 연결한 마지막 시도만 프로필 근거로 사용한다.
- `PTG-014`: 문항·토큰 위치와 발음 상세는 ERD에 컬럼을 추가하지 않고 `trainings.result.wordAttempts`에 저장한다.
- `PTG-015`: 음성은 multipart로 일시 수신해 발음 분석 adapter에 전달하고 성공·실패와 관계없이 영구 저장하지 않는다.
- `PTG-016`: 프로필 상태는 저장하지 않고 취약도에서 계산하며 분석 버전은 Backend 상수와 생성 스냅샷에 기록한다.
- `PTG-017`: DB 점수는 `0~1000`, API와 생성 JSON은 발음 `0~100`, 취약도 `0~1` 단위를 사용한다.
- `PTG-018`: 목록의 모든 훈련이 검증에 성공한 경우에만 데이터를 저장하고 `NOT_READY`에서 `NOT_STARTED`로 전환한다.

## 서비스와 데이터 영향

- 책임 서비스: Backend
- 후보 생성·발음 분석: AI server 계약, MVP는 Backend의 결정적 Mock provider
- 시선 분석: eyetracking server 계약, MVP는 결정적 Mock adapter
- 데이터 기준: `reading_features`, `student_feature_profiles`, `training_templates`, `trainings`, `training_datas`, `word_attempt_logs`, `gaze_sessions`, `gaze_analysis_results`
- 원본 음성: 요청 처리 중에만 유지하고 DB·파일 시스템에 보관하지 않는다.
- Redis: MVP 필수 범위에서 사용하지 않는다.

## 취약도와 난이도

- 취약도 `WEAKNESS_V1`: 정답 오류 0.40, 발음 오류 0.30, 시선 부담 0.20, 읽기 지연·건너뛰기 0.10
- 부담 기준: 응시 시간 1,200ms, 응시 횟수 3회, 회귀 2회, 단어 읽기 2,500ms
- 상태: `NORMAL < 0.4`, `WATCH < 0.6`, `WEAK < 0.8`, 그 이상 `CRITICAL`
- 신뢰도: `min(1, evidenceCount / 10) × 평균 분석 신뢰도`
- 난이도: 정답률 구간을 `1~5`로 변환하고 발음 또는 시선 부담이 있으면 1단계 낮춘다.

## 비기능 요구사항

- 같은 생성 대상과 멱등성 키는 중복 훈련 데이터를 만들지 않는다.
- AI·시선 외부 호출 중 DB 트랜잭션과 행 잠금을 장시간 유지하지 않는다.
- 후보 원문, 음성 본문, 개인정보와 전체 요청 본문을 로그에 기록하지 않는다.
- Mock provider는 같은 입력에 같은 결과를 반환한다.
- 커리큘럼 단위 저장은 전체 성공 또는 전체 미저장을 보장한다.

## 검증

- 34개 타입의 정상·누락·중복·인덱스·정답 위치 검증
- 자모 전체와 주요 음운 규칙 7종의 양성·음성 사례
- 마지막 확정 시도, 낮은 음성 신뢰도와 시선 부담의 프로필 반영
- 부분 통과·최대 재시도·커리큘럼 전체 미저장
- 학생용 문항 응답의 정답·내부 메타데이터 비노출
- AI 요청의 학생 식별자와 직접 개인정보 부재
- 성공·실패 후 임시 음성 파일 부재

## 배포와 롤백

- 빈 MySQL 기준 단일 Flyway V1을 사용한다.
- 다른 환경에 기존 V1이 적용되어 있으면 직접 적용하지 않고 별도 baseline·변환 migration을 작성한다.
- 생성 배치는 설정으로 비활성화할 수 있어야 하며 비활성화해도 기존 훈련 조회·수행은 유지한다.
