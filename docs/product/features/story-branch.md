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

- 선택지 카드와 선택 상태를 저장하지 않는다.
- Backend가 `stories.progress`를 조회해 AI 요청의 `currentProgress`로 전달한다.
- 클라이언트는 진행률을 요청값으로 입력하지 않는다.
- AI의 `nextProgress`는 현재값 이상 `100` 이하이어야 한다.
- 다음 장면 저장과 진행률 갱신은 하나의 트랜잭션으로 처리한다.
- `nextProgress`가 `100`이면 이야기 상태를 `COMPLETED`로 변경한다.
- 동일 상태의 중복 생성 요청은 충돌로 처리한다.

## 데이터

- `stories.progress`
- `stories.status`
- `story_lines.requires_branch_input`
- `story_lines.content`

데이터 모델은 [MySQL 데이터 모델](../../architecture/data-model.md)을 따른다.
