---
type: Feature Specification
title: 학습 보고서
description: 기간별 학습 데이터를 동기 분석해 저장하고 조회하는 보고서 기능입니다.
tags: [feature, report, analytics]
timestamp: 2026-07-24T00:00:00+09:00
---
# 기능 명세: 학습 보고서

- 상태: accepted

## 기대 결과

교수자가 학습자와 기간을 선택하면 요청 안에서 보고서를 생성·저장하고 생성된 보고서를 상세 조회할 수 있다.

## 수용 기준

- 보고서는 비동기 작업 없이 동기 생성한다.
- 분석 결과는 `reports.snapshot_data`에 저장한다.
- 교수자 의견은 `reports.teacher_memo`에 저장한다.
- `reports.created_at`을 보고서 생성일로 표시한다.
- 초안·게시 상태, 게시 버전과 게시 일시를 별도로 저장하지 않는다.
- 공유 토큰, 공유 만료·폐기 상태와 외부 공유 링크를 제공하지 않는다.

## 제외 범위

- 보호자 외부 공유
- 게시·재게시
- 보고서 생성 작업 상태 조회
