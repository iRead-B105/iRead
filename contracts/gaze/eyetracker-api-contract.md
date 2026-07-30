# Eye Tracker API 연동 초안

- 상태: draft
- 최종 검토일: 2026-07-28
- 관련 이슈: `S15P11B105-72`
- 기준 원본: `contracts/openapi/app-api.yaml`, `contracts/database/schema.sql`

## 목적

이 문서는 Tobii Eye Tracker 기반 시선 추적 결과를 아동 앱, 시선 추적 프로토타입, Backend가 어떤 단위로 주고받을지 정리하는 계약 초안이다.

현재 단계에서는 OpenAPI 원본과 데이터베이스 migration을 변경하지 않는다. Backend·Frontend·Eyetracking 담당자 합의 전까지 이 문서는 연동 방향과 payload 예시를 검토하기 위한 기준으로 사용한다.

## 역할 분리

| 영역 | 책임 |
| --- | --- |
| 아동 앱 Frontend | 학습 화면 렌더링, 단어·문장 DOM 식별자 제공, gaze 결과를 API payload로 변환 |
| 시선 추적 프로토타입 | Tobii 기기 연결, native gaze 수집, 보정, `valid`·`presence`·좌표 튐·blink cooldown 필터링 |
| Backend | gaze session 저장, 분석 결과 저장, 관리자 조회·보고서 반영 |
| Database | `gaze_sessions`, `gaze_analysis_results`, `word_attempt_logs` 중심으로 저장 |

## 전체 흐름

1. 아동 앱이 이야기·훈련·테스트 화면에 진입한다.
2. 아동 앱이 로컬 시선 추적 프로토타입에 장치 상태를 확인한다.
3. 필요한 경우 아동 앱이 보정 안내 또는 보정 화면을 표시한다.
4. Backend에 gaze session 시작을 요청한다.
5. 시선 추적 프로토타입이 Tobii gaze frame을 수집하고 보정·필터링한다.
6. 아동 앱이 화면의 단어·문장 영역과 gaze 좌표를 비교해 응시 결과를 계산한다.
7. 콘텐츠 종료 시 Backend에 gaze session 종료와 분석 결과 저장을 요청한다.
8. 관리자 앱과 보고서는 저장된 gaze analysis 결과를 조회한다.

## 사용할 API 후보

| 용도 | Method | Path | 현재 명세 상태 | 비고 |
| --- | --- | --- | --- | --- |
| 장치 상태 확인 | `GET` | `/api/app/gaze/device/status` | No | 로컬 시선 추적 서버 상태와 Backend 응답 책임 분리 필요 |
| 보정 안내 조회 | `GET` | `/api/app/gaze/calibration-guide` | No | 실제 보정은 로컬 시선 추적 프로토타입에서 수행 |
| session 시작 | `POST` | `/api/app/gaze/sessions` | No, 해소 규칙 있음 | `testId`, `trainingId`, `storyId` 중 `contentType`과 일치하는 식별자 하나만 전달 |
| session 종료 | `PATCH` | `/api/app/gaze/sessions/{gazeSessionId}/end` | No, 해소 규칙 있음 | `data`는 초당 5~10프레임으로 수집한 원시 시선 데이터 또는 요약 JSON |
| session 실패 | `PATCH` | `/api/app/gaze/sessions/{gazeSessionId}/failed` | No, 보류 | 장치 끊김, 보정 실패, 샘플 부족 등 |
| 분석 결과 저장 | `POST` | `/api/app/gaze/sessions/{gazeSessionId}/analysis-results` | No, 해소 규칙 있음 | 검사·훈련·이야기 공통 분석 결과 저장. 이야기 문장별 분석은 `sentenceMetrics`로 전달 |
| 이야기 시선 분석 | `POST` | `/api/app/story/{studentId}/{storyId}/gaze-analysis` | 공통 분석 API로 merge | 별도 endpoint로 유지하지 않고 `analysis-results`로 통합 |

## Backend 분석 기준

Backend는 Frontend가 전달한 단어 단위 gaze 결과를 단어의 언어학적 분류와 매핑해 이후 교안 생성에 활용한다.

예를 들어 `사과를 먹는다`에서 `먹는다`에 체류 또는 역행이 발생하면 Backend는 해당 단어가 가진 받침, 이중모음, 구개음화 등 분류 정보를 기준으로 약점 점수를 누적한다. 이후 교안 생성 시 누적 점수가 높은 분류의 비중을 높인다.

Frontend와 시선 추적 프로토타입은 언어학적 분류를 직접 계산하지 않는다. Frontend는 화면에서 어떤 단어에 읽음·체류·역행·건너뜀이 발생했는지만 단어 단위로 전달하고, Backend가 `words`, `word_categories`, `reading_features` 등 저장 데이터를 이용해 분류별 점수로 변환한다.

## 데이터베이스 매핑

| 저장 대상 | 테이블 | 주요 컬럼 | Frontend/Eyetracking 입력 |
| --- | --- | --- | --- |
| 시선 추적 실행 단위 | `gaze_sessions` | `student_id`, `test_id`, `training_id`, `story_id`, `content_type`, `started_at`, `ended_at`, `data`, `status`, `calibration_status` | 콘텐츠 ID, 보정 상태, 세션 시작·종료 시각, 5~10fps 샘플 또는 요약 JSON |
| 세션 분석 요약 | `gaze_analysis_results` | `gaze_session_id`, `total_visited_duration`, `total_visited_count`, `reverse_read_count`, `avg_visited_duration` | 세션 전체 체류 시간, 응시 횟수, 되돌아보기 횟수 |
| 단어별 읽기 근거 | `word_attempt_logs` | `word_id`, `story_line_id`, `training_id`, `test_id`, `surface_text`, `has_audio_data`, `fixation_duration_ms`, `fixation_count`, `gaze_start_offset_ms`, `gaze_end_offset_ms`, `is_skipped`, `regression_count` | 단어 DOM hit test 결과, dwell 시간, skip 여부, regression 횟수. 시선 데이터 존재 여부는 관련 값의 존재로 판정한다. |

## Frontend에서 계산할 값

Frontend는 원시 좌표 전체를 Backend로 전송하지 않고, 학습 분석에 필요한 결과값을 계산한 뒤 전송한다.

| 값 | 설명 |
| --- | --- |
| `fixationDurationMs` | 단어 또는 문장 영역을 응시한 누적 시간 |
| `fixationCount` | 동일 영역에 gaze가 진입한 횟수 |
| `gazeStartOffsetMs` | gaze session 시작 이후 해당 영역 첫 응시 시각 |
| `gazeEndOffsetMs` | gaze session 시작 이후 해당 영역 마지막 응시 시각 |
| `isRead` | 단어를 1초 이상 응시해 읽음 처리되었는지 여부 |
| `isFixated` | 읽음 처리 후 추가로 1초 이상 더 머물러 체류로 간주되었는지 여부 |
| `isSkipped` | 순서상 이전 단어를 읽지 않고 다음 단어를 먼저 1초 이상 응시했는지 여부 |
| `isRegressed` | 이미 지나간 이전 단어를 다시 1초 이상 응시했는지 여부 |
| `regressionCount` | 이미 지난 영역으로 되돌아간 횟수 |
| `validSampleCount` | `valid=true`, `presence=true`, `gazeUsable=true`인 샘플 수 |
| `invalidSampleCount` | blink, presence lost, outlier 등으로 제외한 샘플 수 |

## 단어 단위 판정 기준

읽음·체류·역행·건너뜀은 Frontend가 단어 DOM hit test 결과를 기준으로 계산한다.

| 판정 | 기준 |
| --- | --- |
| 읽음 | 한 단어를 1초 이상 응시하면 읽음 처리 |
| 체류 | 읽음 처리 이후 같은 단어에 추가로 1초 이상 머물면 체류로 간주 |
| 역행 | 순서대로 읽은 뒤 이전 단어를 다시 1초 이상 응시하면 역행으로 간주 |
| 역행 후 체류 | 역행한 이전 단어에 추가로 1초 이상 머물면 해당 단어에 체류도 함께 기록 |
| 건너뜀 | 순서상 앞 단어를 읽지 않고 다음 단어를 먼저 1초 이상 응시하면 건너뜀으로 간주 |
| 건너뜀 후 체류 | 건너뛴 다음 단어에 추가로 1초 이상 머물면 해당 단어에 체류도 함께 기록 |

## 좌표 샘플 저장 기준

원시 Tobii 좌표를 60~90fps로 모두 저장하지 않는다.

- Backend 전송용 sample은 5~10fps로 제한한다.
- `data.samples`는 교수자 페이지의 아이트래킹 리플레이 확인용으로만 사용한다.
- 학습 분석과 교안 생성은 좌표가 아니라 `wordAttempts`의 단어 단위 판정 결과를 기준으로 한다.
- `data.samples`는 디버깅과 리플레이 재현에 필요한 최소 정보만 포함한다.
- 좌표는 화면 크기에 독립적인 normalized 좌표(`0~1`)를 우선 사용한다.
- 개인정보와 민감한 생체 데이터 처리 범위는 `[TBD]`로 남긴다.

## Frontend DOM 요구사항

시선 분석 대상 텍스트는 단어 또는 문장 단위 DOM 식별자를 가져야 한다.

```html
<span
  data-word-id="23"
  data-story-line-id="5"
  data-word-index="0"
>
  개미는
</span>
```

최소 요구 필드:

| 필드 | 필수 여부 | 설명 |
| --- | --- | --- |
| `wordId` | `[TBD]` | Backend `words.id`를 Frontend가 받을 수 있는지 확인 필요 |
| `storyLineId` | 이야기 읽기에서 필수 | Backend `story_lines.id` |
| `wordIndex` | 필수 | 화면에 렌더링된 단어 순서 |
| `surfaceText` | 필수 | 화면에 표시된 실제 단어 |
| `rect` | 필수 | hit test에 사용할 DOM 위치 |

## 샘플 파일

| 파일 | 용도 |
| --- | --- |
| [gaze-session-start.json](samples/gaze-session-start.json) | session 시작 요청 예시 |
| [gaze-session-end.json](samples/gaze-session-end.json) | session 종료 요청 예시 |
| [gaze-analysis-results.json](samples/gaze-analysis-results.json) | 공통 세션 분석 결과와 이야기 문장·단어별 분석 payload 통합 예시 |

## 미결 사항

- [TBD] `wordId`를 Frontend가 직접 받을지, `surfaceText` 기반으로 Backend가 매핑할지 결정
- [TBD] 단어별 gaze 결과를 `word_attempt_logs`로 직접 저장할 API를 별도로 둘지 결정
- [TBD] `gaze_sessions.data`에 저장할 sample 수, 보관 기간, 개인정보 처리 범위
- [TBD] `gaze_analysis_results`를 Frontend 계산값으로 저장할지 Backend가 재계산할지 결정
- [TBD] 시선 추적 실패 시 학습 흐름을 계속 진행할지, 대체 입력으로 전환할지 결정
