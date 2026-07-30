# App 학습 JSON 계약

비음성 훈련·검사 문항은 [공통 제출 스키마](app-learning-submission.schema.json)를 사용한다. 음성 문항은 녹음 API의 `multipart/form-data` 계약을 사용하며 이 스키마에 Base64 음성을 넣지 않는다.

## 문항 조회 형식

훈련과 검사는 [공통 문항 스키마](app-learning-question.schema.json)의 `questionType`, `responseType`, `content`를 사용한다. 세션과 진행률을 포함한 전체 응답 데이터는 [훈련 문항 스키마](training-question.schema.json)와 [검사 문항 스키마](test-question.schema.json)를 따른다.

```json
{
  "trainingId": 31,
  "questionNumber": 2,
  "totalQuestions": 5,
  "question": {
    "questionType": "CONSONANT_SOUND_CHOICE",
    "responseType": "SINGLE_CHOICE",
    "content": {
      "audioText": "ㄱ",
      "choices": ["ㄱ", "ㄴ", "ㄷ"]
    }
  }
}
```

- `questionType`은 생성·저장된 34개 훈련 타입이다. 검사는 연결된 `training_template_id`의 같은 타입을 사용한다.
- `responseType`은 App이 사용할 입력 컴포넌트와 제출 API를 결정한다.
- `content`에는 표시와 입력 수집에 필요한 필드만 포함한다.
- `answer`, `answerIndex`, `answerOrder`, 기대 발음, 분석 대상과 특징 코드는 Backend 내부 문항에만 보관한다.
- App은 `questionType`을 다시 분류하지 않고 Backend가 제공한 `responseType`을 사용한다.

### 34개 타입 매핑

| `responseType` | `questionType` |
| --- | --- |
| `TRACE` | `VOWEL_TRACE`, `CONSONANT_TRACE`, `SYLLABLE_TRACE` |
| `SINGLE_CHOICE` | `CONSONANT_SOUND_CHOICE`, `VOWEL_SOUND_CHOICE`, `CONSONANT_VOWEL_CLASSIFICATION`, `SYLLABLE_INITIAL_CHOICE`, `WORD_INITIAL_CHOICE`, `SAME_INITIAL_WORD_CHOICE`, `FINAL_CONSONANT_CHOICE`, `WORD_FINAL_SOUND_CHOICE`, `FINAL_CONSONANT_COMPARISON`, `SIMILAR_SOUND_CHOICE`, `FINAL_CONSONANT_DELETE`, `SYLLABLE_DELETE`, `SYLLABLE_REPLACE`, `IMAGE_SENTENCE_MATCH` |
| `ORDERING` | `PHONEME_BLEND`, `SYLLABLE_BLEND`, `SENTENCE_ASSEMBLY` |
| `COMPONENT_BUILD` | `BASIC_SYLLABLE_BUILD`, `FINAL_SYLLABLE_BUILD`, `DOUBLE_FINAL_BUILD` |
| `AUDIO` | `WORD_READING`, `NONWORD_READING`, `DIFFICULT_WORD_PREVIEW`, `SENTENCE_READING`, `SHORT_PASSAGE_READING`, `SENTENCE_REPEAT`, `WORD_CHAIN_READING`, `PHRASE_READING`, `REPEATED_SENTENCE_READING`, `SHORT_STORY_READING` |
| 동적 | `FILL_IN_THE_BLANK`: `CHOICE→SINGLE_CHOICE`, `TEXT→TEXT_INPUT`, `VOICE→AUDIO`, `HANDWRITING→TRACE` |

## 공통 제출 형식

```json
{
  "submissionId": "1c7f3e06-03e0-4b06-91a1-4fa128b9ae71",
  "responseType": "SINGLE_CHOICE",
  "response": {
    "selectedIndex": 2
  }
}
```

- `submissionId`는 App이 제출 직전에 생성하고 같은 네트워크 요청을 재전송할 때 재사용한다.
- `responseType`은 문항 조회 응답에서 Backend가 제공한 유형과 같아야 한다.
- App은 정답, `wordId`, `isCorrect`, 점수와 기대 발음을 보내지 않는다.
- Backend는 경로의 학생·훈련·문항과 진행 중인 검사, 저장된 생성 문항을 기준으로 제출을 검증하고 평가한다.
- Backend는 처리한 `submissionId`와 응답을 기존 `trainings.result.submissions[]` 또는 `tests.result.submissions[]`에 저장한다. 따라서 이 계약만으로 ERD 컬럼을 추가하지 않는다.

검사 제출 경로에는 `testId`가 없으므로 요청 본문에서 다음과 같이 공통 제출 객체를 감싼다.

```json
{
  "testId": 31,
  "submission": {
    "submissionId": "1c7f3e06-03e0-4b06-91a1-4fa128b9ae71",
    "responseType": "ORDERING",
    "response": {
      "orderedIndexes": [2, 0, 1]
    }
  }
}
```

## 응답 유형

| `responseType` | App이 보내는 원시 입력 | 대표 문항 |
| --- | --- | --- |
| `TRACE` | 캔버스 크기와 시간 순서가 있는 획 좌표 | 글자 따라 보기, 직접 쓰기 |
| `SINGLE_CHOICE` | 선택한 보기의 0 기반 인덱스 | 듣고 고르기, 삭제·대치, 선택형 빈칸 |
| `ORDERING` | 사용자가 확정한 보기 인덱스 순서 | 음소·음절 합성, 문장 조립 |
| `COMPONENT_BUILD` | 초성·중성·종성 슬롯별 선택 인덱스 | 기본·받침·겹받침 글자 만들기 |
| `TEXT_INPUT` | 사용자가 직접 입력한 문자열 | 텍스트형 빈칸 |

문항에 없는 인덱스, 중복 슬롯, 문항과 다른 `responseType`은 Backend가 `400`으로 거절한다.

## 훈련 피드백

[훈련 피드백 스키마](training-feedback.schema.json)는 평가에 성공한 시도 번호, 정답 여부, 오류 위치와 재시도 가능 여부를 반환한다. `hint`는 오답 후 재시도에 사용하고 `correctResponse`는 3회차 오답에서만 제공한다.

## 검사 진행률

[검사 진행률 스키마](test-progress.schema.json)는 저장 수락 여부와 진행률만 반환한다. 정답 여부, 점수, 인식 결과와 특징 분석은 아동 App 응답에 포함하지 않는다.

## 훈련·검사 완료

- 훈련 완료 요청은 경로의 `trainingId`만 사용하며 요청 본문을 보내지 않는다.
- 검사 완료 요청은 `testId`만 보낸다.
- App은 누적 `result`, 정확도와 완료 시각을 보내지 않는다.
- Backend는 저장된 최종 제출을 검증하고 서버 시각으로 완료 처리한다.
- [훈련 완료 스키마](training-completion.schema.json)와 [검사 완료 스키마](test-completion.schema.json)는 완료 화면에 필요한 상태, 메시지 키와 다음 행동만 반환한다.
- 검사 문항별 완료 API는 제거하고 [검사 진행률 스키마](test-progress.schema.json)를 반환하는 제출 API에 통합한다.
- 정확도, 정오답과 특징 분석은 교수자 API에서만 조회한다.
