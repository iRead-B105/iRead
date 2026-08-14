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
- 완료 훈련의 `finishedAt` 기준 서로 다른 학습일이 1일 이상이면 생성한다.
- 학습일이 0일이면 `REPORT_INSUFFICIENT_LEARNING_DAYS`와 `requiredDays=1`, `actualDays`를 반환한다.
- 분석 결과는 `reports.snapshot_data`에 저장한다.
- 신규 snapshot은 `snapshotVersion=teacher-report-v2`, `calculationVersion=reading-metrics-v1`을 포함한다.
- 정확도와 읽기 속도는 [교수자 학습 기록 조회](teacher-learning-records.md)의 source record와 같은 원본·단위·집계식을 사용한다.
- 1학습일 보고서도 핵심 성과와 한 시점의 성장 값을 표시한다.
- 비교 가능한 시점이 2개 미만이면 현재 값은 유지하고 `growthComparisonStatus`와 `automaticAnalysis.status`를 `INSUFFICIENT_DATA`로 저장한다.
- 비교 가능한 시점이 2개 이상이면 최초·최신 유효 값의 정확한 차이와 `INCREASED`, `DECREASED`, `UNCHANGED` 방향을 재현 가능하게 저장한다.
- `[TBD]` 제품 임계값이 필요한 영역별 향상·지속 어려움 판정은 임계값 승인 전 임의 생성하지 않는다.
- 교수자 의견은 `reports.teacher_memo`에 저장한다.
- `reports.created_at`을 한국시간(Asia/Seoul) 기준의 실제 보고서 생성일시로 표시한다.
- 초안·게시 상태, 게시 버전과 게시 일시를 별도로 저장하지 않는다.
- 공유 토큰, 공유 만료·폐기 상태와 외부 공유 링크를 제공하지 않는다.

## 제외 범위

- 보호자 외부 공유
- 게시·재게시
- 보고서 생성 작업 상태 조회
