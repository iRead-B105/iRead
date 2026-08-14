---
type: Implementation Guide
title: "이야기 읽기 리플레이 판정 기준"
tags: [story, gaze, replay, teacher, learner]
timestamp: 2026-08-04T13:30:00+09:00
---

# 이야기 읽기 리플레이 판정 기준

## 적용 범위

- 학습자 앱의 이야기 읽기 진행
- 교사 화면의 페이지별 읽기 리플레이와 체류·건너뜀·되돌아보기 요약
- 아이트래커 입력과 마우스 cursor fallback 입력

두 입력 방식은 같은 원시 시선 샘플 형식으로 저장한다. Backend가 버전이 있는 동일 판정 규칙을 적용해 `wordMetrics`를 만들고, 교사 화면은 그 결과를 표시한다.

## 학습자 앱: 읽음과 페이지 이동

- 단어 영역에 시선 또는 커서가 **한 번이라도 도달하면 읽음**으로 처리한다.
- 읽기는 문장 내 정순으로만 진행된다. 다음에 읽어야 할 단어에 도달해야 읽기 진행도가 증가한다.
- 모든 단어가 읽음이 되면 다음 페이지 이동을 활성화한다.
- 다음 페이지로 이동할 때 현재 페이지의 시선 세션을 종료하고 원시 샘플을 전송한다.

## Backend: 리플레이 판정

페이지별 원시 시선 샘플을 동일 단어 연속 응시 구간으로 묶어 방문당 하나의 판정 event를 만든다. `연속`은 읽기 순서가 아니라 같은 `storyLineId + pageNo + tokenIndex`를 계속 응시한다는 뜻이다. 다음 조건 중 하나가 발생하면 기존 방문을 끝낸다.

- 다른 token 또는 단어 밖을 가리키는 sample이 들어온다.
- 같은 token의 다음 sample이더라도 직전 sample과의 공백이 250ms를 초과한다.

250ms는 짧은 되돌아보기 횟수가 아니라 약 80ms 주기로 수집되는 sample의 순간 누락을 허용하는 `maxSampleGapMs`다. 다른 token을 사이에 두고 같은 단어로 돌아오면 250ms 이내라도 새 방문이다. 각 방문 시간은 `마지막 sample 시각 - 첫 sample 시각 + 80ms`로 계산한다.

| 상태 | 조건 |
| --- | --- |
| 읽음 | 단어에 짧게라도 도달한 모든 방문 |
| 체류 | 페이지 전체 읽기 시간과 글자 수를 이용해 계산한 단어별 기대 시간보다 해당 방문 시간이 긴 경우 |
| 건너뜀 | 아직 읽어야 할 다음 단어보다 뒤의 단어에 **체류**한 경우. 사이에 실제로 건너뛴 token을 기록한다. |
| 되돌아보기 | 이미 정순 읽기가 진행된 앞 단어에 **체류**한 경우 |

짧은 순서 이탈은 읽음으로만 남기며 건너뜀·되돌아보기로 과대 판정하지 않는다. 반대로 순서가 맞는 단어의 긴 방문은 체류로만 표시한다. 건너뜀 event가 발생하면 `nextExpectedTokenIndex`부터 도착 token 직전까지를 `skippedTokenIndexes`로 남기고 다음 기대 위치를 도착 token 다음으로 옮긴다. 건너뛴 token을 나중에 읽으면 최종 `wordMetrics.skipped`는 `false`로 바꾸되 과거 건너뜀 event는 삭제하지 않는다.

`wordMetrics.visitCount`는 체류 여부와 관계없이 분리된 모든 방문 수다. `dwellDurationMs`는 기대 시간보다 긴 방문의 시간만 합산하고 `regressionCount`는 체류 조건을 통과한 되돌아보기 event 수를 센다. `firstSeenMs`는 페이지의 첫 유효 token sample을 0ms로 둔 최초 방문 시작 상대 시간이다.

Backend는 판정 결과를 다음 두 수준으로 반환한다.

| 결과 | 용도 | 필수 정보 |
| --- | --- | --- |
| `wordMetrics[]` | 최종 단어 집계와 히트맵 | `storyLineId`, `pageNo`, `tokenIndex`, `text`, `dwellDurationMs`, `visitCount`, `skipped`, `regressionCount`, `firstSeenMs` |
| `replay.events[]` | 시간 순서 이동 경로 재생 | `pageNo`, `eventIndex`, `eventAtMs`, `fromTokenIndex`, `toTokenIndex`, `movementType`, `dwellQualified`, `dwellDurationMs`, `skippedTokenIndexes` |

`movementType`은 `READ`, `SKIP`, `REGRESSION` 중 하나다. `fromTokenIndex`는 페이지 첫 event에서 `null`일 수 있다. `eventAtMs`는 `firstSeenMs`와 마찬가지로 페이지 첫 유효 token sample 기준 상대 시간이다. `SKIP`은 도착 token이 아니라 `skippedTokenIndexes`의 중간 token을 건너뛴 사건이며, `REGRESSION`은 체류 조건을 통과한 앞 방향 이동이다.

최초 계약 버전은 `story-gaze-word-v1`이며 `analysisMeta`에 다음 값을 함께 반환한다.

| 필드 | 값 |
| --- | --- |
| `calculationSource` | `BACKEND` |
| `calculationVersion` | `story-gaze-word-v1` |
| `heatmapScale` | `PAGE_RELATIVE_MAX` |
| `dwellThresholdMethod` | `PAGE_CHARACTER_AVERAGE` |
| `sampleTailMs` | `80` |
| `maxSampleGapMs` | `250` |
| `firstSeenReference` | `PAGE_FIRST_VALID_SAMPLE` |
| `skipRequiresDwell` | `true` |
| `regressionRequiresDwell` | `true` |

교사 화면은 `wordMetrics`를 히트맵과 체류·건너뜀·되돌아보기 목록의 기준으로 사용한다. `replay.events`는 이동 순서 재생에만 사용하며 Frontend는 raw replay로 운영 판정을 다시 계산하지 않는다. Backend `wordMetrics` 또는 `replay.events`가 없으면 page metric을 단어 수로 나누는 추정값을 만들지 않고 해당 표현을 `NO_DATA`로 표시한다. Admin replay에는 raw `x`, `y` 좌표를 포함하지 않는다.

## 교사 화면: 재생과 히트맵

- 재생 간격은 이번 버전에서 event당 700ms로 유지한다. 실제 sample 시간 간격 재현은 별도 버전으로 분리한다.
- 재생 중에는 현재 단어와 최근 이동 경로만 표시하고 히트맵은 숨긴다.
- 일반 이동은 실선, 건너뜀은 점선, 되돌아보기는 역방향 화살표로 색 이외의 형태도 구분한다.
- 마지막 event에서 자동 반복하지 않고 `wordMetrics` 기반 페이지 상대 히트맵으로 전환한다.
- 히트맵 색 농도는 `단어 dwellDurationMs / 페이지 최대 dwellDurationMs`이며 건너뜀·되돌아보기 수치를 더하지 않는다.
- 체류 기록이 없는 단어는 색을 칠하지 않고, 건너뜀은 중립색 표식, 되돌아보기는 별도 테두리와 횟수로 표시한다.
- 완료 후 전체 이동 경로 중첩은 선택 기능으로 제공한다. `다시 보기`에서만 히트맵을 숨기고 첫 event로 돌아간다.

## 분석 상태 표시

페이지마다 별도 시선 세션을 사용한다. 빈 신규 세션이 실패하더라도, 같은 이야기에서 완료된 페이지 분석이 하나라도 있으면 교사 화면은 기존 리플레이를 계속 표시한다.
