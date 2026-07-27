---
type: Feature Specification
title: AI 이야기 분기
description: 아동의 음성을 STT로 변환하고 현재 진행률을 고려해 다음 이야기 장면을 생성하는 기능입니다.
tags: [feature, story, stt, ai, progress]
timestamp: 2026-07-24T00:00:00+09:00
---
# 기능 명세: AI 이야기 분기

- 상태: accepted
- 관련 기능: `ST-BRANCH-01`~`ST-BRANCH-05`

## 기대 결과

아동이 분기 질문에 음성으로 답하면 시스템이 STT 텍스트와 현재 이야기 진행률을 AI에 전달하고, 진행률에 적합한 다음 장면을 생성해 보여준다.

## 수용 기준

- 미리 정의한 선택지 카드는 제공하지 않는다.
- 분기점에서 아동의 음성을 STT로 복원하고 최종 텍스트를 `story_choices.content`에 저장한다.
- 한 분기 대사에는 최종 선택 한 건만 저장하고 STT 중간 실패와 재시도 결과는 저장하지 않는다.
- Backend가 `stories.progress`를 조회해 AI 요청의 `currentProgress`로 전달한다.
- 클라이언트는 진행률을 요청값으로 입력하지 않는다.
- AI의 `nextProgress`는 현재값 이상 `100` 이하이어야 한다.
- AI 생성 성공 후 선택 텍스트, 다음 장면·대사와 진행률 갱신을 하나의 DB 트랜잭션으로 처리한다.
- `nextProgress`가 `100`이면 이야기 상태를 `COMPLETED`로 변경한다.
- 같은 `story_line_id`의 재시도는 AI를 다시 호출하거나 저장 결과를 덮어쓰지 않고 최초 확정 결과를 `200 OK`로 반환한다.
- 최초 처리 응답의 `replayed`는 `false`, 기존 결과를 반환한 재시도 응답의 `replayed`는 `true`다.
- 동시 요청이 UNIQUE 제약에서 경합하면 저장에 성공한 최초 결과를 조회해 반환한다.

## 데이터

- `stories.progress`
- `stories.status`
- `story_scenes`
- `story_lines.has_choices`
- `story_lines.content`
- `story_choices.content`

데이터 모델은 [MySQL 데이터 모델](../../architecture/data-model.md)을 따른다.
