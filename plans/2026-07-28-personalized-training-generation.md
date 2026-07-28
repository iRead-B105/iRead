---
type: Execution Plan
title: "맞춤 훈련 데이터 생성 파이프라인"
description: "학생별 읽기 취약도를 집계하고 33개 훈련 타입의 후보를 생성·검증하여 다음 커리큘럼에 배정하는 Backend 구현 계획입니다."
tags: [plan, backend, training, personalization, mysql, batch, mock-ai]
timestamp: 2026-07-28T00:00:00+09:00
---
# 맞춤 훈련 데이터 생성 파이프라인

- 상태: active
- 작성일: 2026-07-28
- 수정일: 2026-07-28
- 대상: `services/backend`

## 기대 결과

현재 커리큘럼을 완료한 학생의 단어별 정답·발음·시선·읽기 시간 근거로 특징별 취약도를 갱신하고, 다음 커리큘럼에 배정할 약 5개 훈련 목록을 즉시 편성한다. 교사가 목록을 편집한 뒤 매일 03:00 배치가 각 훈련에 5개 문항을 생성한다. Backend가 형태·자모·G2P·음운 규칙과 타입별 형식을 검증하고, 커리큘럼의 모든 훈련이 통과한 경우에만 `training_datas.generated_data`를 저장하고 목록을 잠근다.

## 범위

### 포함

- 최종 `contracts/database/erd.png`에 있는 `reading_features`, `student_feature_profiles`를 Flyway V1·계약 SQL·Backend 엔티티에 반영한다.
- 33개 훈련 타입과 타입별 프롬프트·출력 템플릿을 `training_templates.prompt` JSON으로 관리한다.
- AI 훈련 후보 생성, 발음 분석과 시선 분석의 결정적 Mock adapter를 구현한다.
- KOMORAN 3.3.9 형태소 분석, 한글 자모 분해, G2P와 주요 음운 규칙 엔진을 Backend에 구현한다.
- 수행 결과 집계, 특징별 취약도, 다음 커리큘럼 목록 편성, 교사 편집, 03:00 생성 배치를 구현한다.
- 기능·OpenAPI·MySQL·JSON 계약과 관련 테스트를 함께 갱신한다.

### 제외

- AI server의 실제 LLM·STT·발음 분석 모델 구현
- 음성 파일과 `sounds` 테이블의 영구 저장
- 원시 시선 좌표를 Backend에서 직접 분석하는 기능
- `word_attempt_logs.question_no`, `word_attempt_logs.token_index` 컬럼 추가
- 운영 환경의 분산 스케줄러, 작업 큐와 다중 인스턴스 리더 선출

## 확정된 계약

### 데이터베이스

- `contracts/database/erd.png`를 물리 스키마 기준으로 사용하고 신규 V2가 아닌 단일 `V1__baseline_schema.sql`을 수정한다.
- `word_attempt_logs`와 `student_feature_profiles`에는 ERD에 없는 컬럼을 추가하지 않는다.
- 문항·토큰과 단어 로그는 `trainings.result.wordAttempts[]`의 `questionNo`, `tokenIndex`, `wordAttemptLogId`, `isFinal`로 연결한다.
- ERD에 별도 컬럼이 없는 `expectedPronunciation`, `observedPronunciation`, `pronunciationScore`, `pronunciationConfidence`, `errorType`, `wordReadTimeMs`, `analysisVersion`도 같은 결과 항목에 저장한다.
- 같은 위치의 여러 시도 중 `isFinal=true`인 마지막 확정 시도만 프로필 근거로 사용한다.
- 프로필 상태는 저장하지 않고 취약도에서 `NORMAL`, `WATCH`, `WEAK`, `CRITICAL`을 계산한다.
- 분석 버전 `WEAKNESS_V1`은 Backend 상수와 `generated_data.profileSnapshot.analysisVersion`에 기록한다.
- DB 발음 점수와 취약도는 정수 `0~1000`, 외부 API와 생성 JSON은 발음 `0~100`, 취약도 `0~1`을 사용한다.

### 인덱스

- `questionNo`, `sequenceNo`는 1부터 시작한다.
- `targetIndex`, `wordIndex`, `tokenIndex`, `answerIndex`, `deleteIndex`, `replaceIndex`, `answerOrder` 등 배열 위치는 0부터 시작한다.

### AI 후보와 최종 데이터

AI 후보는 다음 공통 입력을 사용한다.

- `trainingType`
- `count=5`
- 학생 프로필에서 계산한 `difficulty`
- `additionalPrompt`
- `outputTemplate`
- 집계된 목표 특징과 제외 특징

AI 후보 응답은 유효한 JSON `{type, data[]}` 하나다. Backend는 후보를 그대로 저장하지 않고 다음 최종 구조로 변환한다.

```json
{
  "schemaVersion": 2,
  "generationMetadata": {},
  "profileSnapshot": {},
  "questions": [
    {
      "questionNo": 1,
      "type": "SENTENCE_READING",
      "content": {},
      "answer": {},
      "analysisTargets": []
    }
  ],
  "validationResult": {}
}
```

- `analysisTargets`는 목표, 문장 토큰, 선택지와 카드를 포함하는 모든 화면 텍스트를 `targetIndex`, `role`, `text`, `expectedPronunciation`, `featureCodes`, `featureOccurrences`로 정규화한다.
- 정답 근거는 정답 목표와 학생이 실제 선택한 항목에만 반영한다.
- 시선 근거는 실제 응시한 모든 항목에 반영한다.
- 읽어야 하는 항목을 건너뛴 경우에만 건너뛰기를 실패 근거로 반영한다.
- AI 요청에는 이름·생년월일·연락처·원본 시선 좌표·`studentId`를 포함하지 않는다.

### 훈련 타입

| 영역 | `trainingType` |
| --- | --- |
| 글자 따라 보기 | `VOWEL_TRACE`, `CONSONANT_TRACE`, `SYLLABLE_TRACE` |
| 소리 듣고 고르기 | `CONSONANT_SOUND_CHOICE`, `VOWEL_SOUND_CHOICE`, `CONSONANT_VOWEL_CLASSIFICATION`, `SYLLABLE_INITIAL_CHOICE`, `WORD_INITIAL_CHOICE`, `SAME_INITIAL_WORD_CHOICE`, `FINAL_CONSONANT_CHOICE`, `WORD_FINAL_SOUND_CHOICE`, `FINAL_CONSONANT_COMPARISON`, `SIMILAR_SOUND_CHOICE` |
| 글자 만들기 | `PHONEME_BLEND`, `SYLLABLE_BLEND`, `BASIC_SYLLABLE_BUILD`, `FINAL_SYLLABLE_BUILD`, `DOUBLE_FINAL_BUILD` |
| 글자 자르기 | `FINAL_CONSONANT_DELETE`, `SYLLABLE_DELETE` |
| 글자 대치 | `SYLLABLE_REPLACE` |
| 글 해독 | `WORD_READING`, `NONWORD_READING`, `DIFFICULT_WORD_PREVIEW`, `SENTENCE_READING`, `SHORT_PASSAGE_READING` |
| 문장 완성 및 이해 | `SENTENCE_ASSEMBLY`, `FILL_IN_THE_BLANK`, `IMAGE_SENTENCE_MATCH` |
| 유창하게 읽기 | `SENTENCE_REPEAT`, `WORD_CHAIN_READING`, `PHRASE_READING`, `REPEATED_SENTENCE_READING`, `SHORT_STORY_READING` |

각 `training_templates.prompt` JSON은 다음 값을 포함한다.

- `trainingType`
- `additionalPrompt`
- `outputTemplate`
- `supportedFeatureCategories`
- `supportedScopes`

공통 프롬프트는 출력 필드·자료형 준수, `data` 길이, JSON 전용 응답, 인덱스 규칙, 정답 위치, 중복 방지, 아동 안전 어휘, 한글 정확성, 임의 ID·URL·경로 금지와 자체 점검을 강제한다.

### 분석과 취약도

- 읽기 특징 사전은 초성 19개, 중성 21개, 종성 27개와 받침 없음, 기본 음절 구조, 자모 결합·단어 길이, KOMORAN 주요 품사, 단어·문장 범위를 포함한다.
- 음운 규칙은 비음화, 연음, 구개음화, 유음화, 된소리되기, 격음화와 받침 대표음을 지원한다.
- 취약도 `WEAKNESS_V1`은 정답 오류 0.40, 발음 오류 0.30, 시선 부담 0.20, 읽기 지연·건너뛰기 0.10 가중치를 사용한다.
- 부담 기준은 응시 시간 1,200ms, 응시 횟수 3회, 회귀 2회, 단어 읽기 2,500ms다.
- 상태 구간은 `NORMAL < 0.4`, `WATCH < 0.6`, `WEAK < 0.8`, 그 이상은 `CRITICAL`이다.
- 신뢰도는 `min(1, evidenceCount / 10) × 평균 분석 신뢰도`다. 음성 분석이 없는 근거는 음성 신뢰도 평균에서 제외한다.
- 난이도는 정답률 구간을 `1~5`로 변환하고 발음 또는 시선 부담이 있으면 1단계 낮춘다.

### 커리큘럼 수명주기

1. 현재 커리큘럼의 약 5개 훈련을 모두 완료한다.
2. Backend가 프로필을 즉시 갱신한다.
3. 취약 특징과 템플릿 호환 범위로 다음 목록을 직접 보완 3개, 확장 1개, 복습·유창성 1개로 편성한다.
4. 교사는 데이터 생성 전 목록·순서·훈련 유형을 편집한다.
5. 매일 03:00 `Asia/Seoul` 배치가 목록별 문항을 생성한다.
6. 각 훈련은 통과 문항을 유지하고 부족분만 최대 3회 재생성한다.
7. 커리큘럼의 모든 훈련이 통과하면 결과를 한 번에 저장하고 목록을 잠근다.
8. 하나라도 실패하면 결과를 저장하거나 잠그지 않고 다음 배치 대상으로 유지한다.

## 작업

### 1. 계약과 기준선

- [x] **BE-013** 기능 명세, Backend–AI 내부 OpenAPI, App·Admin OpenAPI와 `generated_data` V2 계약을 먼저 확정한다.
- [ ] **BE-014** 최종 ERD의 두 신규 테이블을 Flyway V1, `contracts/database/schema.sql`, 엔티티와 ERD 파생 문서에 동기화한다.
- [ ] **BE-015** 읽기 특징과 33개 템플릿을 기존 행을 덮어쓰지 않는 멱등 초기화 코드로 등록한다.

### 2. 생성 데이터와 언어 분석

- [ ] **BE-016** 공통 봉투, 33개 타입별 `content`·`answer`, `analysisTargets` DTO와 검증기를 구현한다.
- [ ] **BE-017** KOMORAN adapter, 자모 분석기, G2P와 7개 음운 규칙 엔진을 구현하고 분석 버전을 고정한다.
- [ ] **BE-018** 모든 타입에 대해 동일 입력에 동일 후보를 반환하는 Mock provider를 구현한다.
- [ ] **BE-019** 부분 통과 유지, 부족분 재요청, 중복 제거, 최종 문항 수 검증과 원자 저장을 구현한다.

### 3. 수행 근거와 프로필

- [ ] **BE-020** multipart 음성을 일시 수신하고 저장하지 않은 채 발음 분석 Mock adapter로 전달한다.
- [ ] **BE-021** 최종 단어 시도 ID, 문항·토큰 위치와 발음 상세 결과를 `trainings.result`에 연결하고 마지막 확정 시도만 선택한다.
- [ ] **BE-026** 시선 추적 서버의 단어 단위 결과 adapter와 Mock 응답을 구현한다.
- [ ] **BE-022** 특징별 근거 변환, 취약도·신뢰도·상태·난이도 계산과 프로필 upsert를 구현한다.

### 4. 다음 커리큘럼과 배치

- [ ] **BE-023** 특징 category·scope와 템플릿 호환 정보를 이용해 다음 커리큘럼 목록을 중복 없이 편성한다.
- [ ] **BE-024** 생성 전 교사 편집과 생성 성공 후 수정 금지 규칙을 Admin API와 도메인 상태에 반영한다.
- [ ] **BE-025** 매일 03:00 실행, 중복 실행 방지, 전체 성공 커밋과 실패 재시도를 포함한 배치를 구현한다.

### 5. 검증

- [ ] **BE-027** 아래 필수 검증을 자동화하고 모두 성공한 뒤 관련 백로그만 `done`으로 변경한다.

## 검증

- 빈 MySQL 8.4에서 Flyway V1 적용과 Hibernate schema validation
- `python tools/validate_contracts.py`
- `python tools/validate_harness.py`
- `git diff --check`
- Backend 전체 테스트
- 33개 `trainingType`별 정상·필수 필드 누락·배열 길이·인덱스·정답 위치 검증
- 자모 전체와 7개 음운 규칙의 양성·음성·경계 사례
- 낮은 음성 신뢰도, 시선 부담, 마지막 확정 시도와 점수 단위 변환 검증
- 현재 커리큘럼 완료부터 프로필·다음 목록·교사 편집·03:00 생성·잠금까지 통합 테스트
- 후보 일부 실패·3회 소진·5개 중 한 훈련 실패 시 전체 미저장 검증
- AI 요청의 이름·생년월일·연락처·학생 식별자·원본 시선 좌표 부재 검증
- multipart 임시 파일이 성공·실패 모두에서 남지 않는지 검증

## 미결 사항

- 없음

## 중요한 위험

- KOMORAN 3.3.9는 JitPack 저장소 추가가 필요하므로 Java 21·Gradle 9.5.1 호환성과 의존성 검사를 먼저 수행한다.
- 최종 ERD에는 문항·토큰 연결 컬럼이 없으므로 `trainings.result`가 유실되거나 형식이 깨지면 단어 로그를 특징 근거로 복원할 수 없다.
- 단일 Flyway V1 수정은 공용 환경에 기존 V1이 적용되지 않았다는 결정에 의존한다. 적용된 환경이 발견되면 V2 전환 계획이 필요하다.
- 단일 인스턴스 MVP 이후 서버를 수평 확장하면 03:00 배치의 분산 중복 실행 방지 수단이 추가로 필요하다.
